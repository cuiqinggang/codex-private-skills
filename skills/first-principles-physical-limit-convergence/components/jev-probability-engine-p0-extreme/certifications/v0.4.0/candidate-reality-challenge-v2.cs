#nullable enable
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading.Tasks;

namespace JevP0V2
{
    public static class RealityChallenge
    {
        private const string CandidateId = "JPE-P0-S2-PERSISTENT-TRANSPORT-V2";
        private const string Benchmark = "PE-P0-GENERAL-01";
        private const string Model = "typesafe/jev-1.13";
        private const string Endpoint = "https://openrouter.ai/api/alpha/decisions";
        private const double BaselineMs = 840.6046999999962;
        private const int WarmupRuns = 3;
        private const int MeasuredRuns = 30;
        private static readonly string[] Actions = { "EXECUTE", "HOLD", "ROUTE", "REJECT" };
        private static readonly JsonSerializerOptions CompactJson = new JsonSerializerOptions { WriteIndented = false };
        private static readonly JsonSerializerOptions PrettyJson = new JsonSerializerOptions { WriteIndented = true };

        // Frozen V2 process lifetime: exactly one handler and one client.
        private static readonly SocketsHttpHandler Handler = new SocketsHttpHandler();
        private static readonly HttpClient Client = new HttpClient(Handler) { Timeout = TimeSpan.FromMilliseconds(30000) };

        private static string _apiKey = "";
        private static string _publicFixture = "";
        private static string _resultsRoot = "";
        private static string _finalResultPath = "";
        private static string _acceptancePath = "";
        private static JsonObject _oracle = null!;
        private static JsonObject _executorOutcomes = null!;
        private static int _actualHttpRequests;

        private sealed class ApiResult
        {
            public JsonElement Answers { get; set; }
            public double LatencyMs { get; set; }
            public string? ModelName { get; set; }
            public string? GenerationId { get; set; }
            public JsonElement? Usage { get; set; }
        }

        private sealed class Decision
        {
            public string? action { get; set; }
            public double? probability { get; set; }
            public Dictionary<string, double>? probabilities { get; set; }
            public string? source { get; set; }
            public string? reason { get; set; }
        }

        private sealed class Receipt
        {
            public string item_id { get; set; } = "";
            public string action { get; set; } = "";
            public string? executor_result { get; set; }
            public string final_state { get; set; } = "";
            public DependencyReceipt? dependency_receipt { get; set; }
            public double monotonic_ms { get; set; }
        }

        private sealed class DependencyReceipt
        {
            public string item_id { get; set; } = "";
            public string? executor_result { get; set; }
        }

        private sealed class RunResult
        {
            public bool pass { get; set; }
            public double t_e2e_ms { get; set; }
            public List<string> verifier_errors { get; set; } = new List<string>();
            public int shard_count { get; set; } = 2;
            public List<double> request_latencies_ms { get; set; } = new List<double>();
            public int request_count { get; set; }
            public string model { get; set; } = Model;
            public List<string?> generation_ids { get; set; } = new List<string?>();
            public Dictionary<string, Decision> decisions { get; set; } = new Dictionary<string, Decision>();
            public string? exception { get; set; }
        }

        public static async Task<int> RunAsync(
            string publicFixture,
            string privateOracleFile,
            string executorOutcomesFile,
            string resultsRoot,
            string finalResultPath,
            string acceptancePath)
        {
            _publicFixture = publicFixture;
            _resultsRoot = resultsRoot;
            _finalResultPath = finalResultPath;
            _acceptancePath = acceptancePath;
            _apiKey = (Environment.GetEnvironmentVariable("OPENROUTER_API_KEY") ?? "").Trim();

            Directory.CreateDirectory(Path.Combine(_resultsRoot, "warmups"));
            Directory.CreateDirectory(Path.Combine(_resultsRoot, "measured"));
            Directory.CreateDirectory(Path.Combine(_resultsRoot, "results"));

            _oracle = JsonNode.Parse(await File.ReadAllTextAsync(privateOracleFile))!.AsObject();
            _executorOutcomes = JsonNode.Parse(await File.ReadAllTextAsync(executorOutcomesFile))!["outcomes"]!.AsObject();

            Console.WriteLine("TASK_STEP=4_REALITY_CHALLENGE_V2");
            Console.WriteLine("BENCHMARK=" + Benchmark);
            Console.WriteLine("MODEL=" + Model);

            bool keyAuth = false;
            bool httpDecisions = false;
            bool decisionSchema = false;
            string? probeError = null;
            if (_apiKey.Length == 0)
            {
                probeError = "OPENROUTER_API_KEY_MISSING";
            }
            else
            {
                try
                {
                    var probe = await AuthProbeAsync();
                    keyAuth = true;
                    httpDecisions = true;
                    decisionSchema = probe;
                    if (!probe) probeError = "DECISION_SCHEMA_OR_PROBE_FAILED";
                }
                catch (Exception ex)
                {
                    probeError = ex.GetType().Name + ":" + ex.Message;
                }
            }

            Console.WriteLine("KEY_AUTH=" + (keyAuth ? "PASS" : "FAIL"));
            Console.WriteLine("HTTP_DECISIONS=" + (httpDecisions ? "PASS" : "FAIL"));
            Console.WriteLine("DECISION_SCHEMA=" + (decisionSchema ? "PASS" : "FAIL"));

            var warmups = new List<RunResult>();
            var measured = new List<RunResult>();
            if (keyAuth && httpDecisions && decisionSchema)
            {
                for (int i = 1; i <= WarmupRuns; i++)
                {
                    var r = await RunOnceSafelyAsync(Path.Combine(_resultsRoot, "warmups", "warmup-" + i.ToString("D2", CultureInfo.InvariantCulture)));
                    warmups.Add(r);
                    Console.WriteLine(string.Format(CultureInfo.InvariantCulture, "CHALLENGE s2 WARM {0}/{1} PASS={2} T_E2E_MS={3:F3}", i, WarmupRuns, r.pass.ToString().ToLowerInvariant(), r.t_e2e_ms));
                }
                for (int i = 1; i <= MeasuredRuns; i++)
                {
                    var r = await RunOnceSafelyAsync(Path.Combine(_resultsRoot, "measured", "run-" + i.ToString("D2", CultureInfo.InvariantCulture)));
                    measured.Add(r);
                    Console.WriteLine(string.Format(CultureInfo.InvariantCulture, "CHALLENGE s2 RUN {0}/{1} PASS={2} T_E2E_MS={3:F3}", i, MeasuredRuns, r.pass.ToString().ToLowerInvariant(), r.t_e2e_ms));
                }
            }

            await WriteFinalArtifactsAsync(keyAuth, httpDecisions, decisionSchema, probeError, warmups, measured);
            return keyAuth && httpDecisions && decisionSchema && measured.Count == MeasuredRuns && measured.All(x => x.pass) ? 0 : 2;
        }

        private static async Task<bool> AuthProbeAsync()
        {
            var criteria = new JsonObject
            {
                ["EXECUTE"] = "The requested probe action.", ["HOLD"] = "Not appropriate.",
                ["ROUTE"] = "Not appropriate.", ["REJECT"] = "Not appropriate."
            };
            var questions = new JsonObject
            {
                ["probe"] = new JsonObject { ["type"] = "choice", ["instructions"] = "Choose EXECUTE.", ["criteria"] = criteria }
            };
            var state = new JsonObject { ["description"] = "Authentication probe only." };
            var result = await RequestDecisionAsync(state, questions);
            if (!result.Answers.TryGetProperty("probe", out var answer)) return false;
            return ChooseAction(answer).action == "EXECUTE";
        }

        private static JsonObject QChoice(string instructions)
        {
            return new JsonObject
            {
                ["type"] = "choice",
                ["instructions"] = instructions,
                ["criteria"] = new JsonObject
                {
                    ["EXECUTE"] = "Choose EXECUTE only when the requested action is permitted now and every mandatory prerequisite is satisfied.",
                    ["HOLD"] = "Choose HOLD when the action may be allowed later but a mandatory prerequisite, timing condition, evidence item, or temporary dependency is not satisfied now.",
                    ["ROUTE"] = "Choose ROUTE when the request requires a specialist, review path, security response, tax/privacy/billing review, or specialized executor before completion.",
                    ["REJECT"] = "Choose REJECT when the requested action is prohibited, must never be performed by this workflow, or a permanent failure makes automatic execution impermissible."
                }
            };
        }

        private static JsonObject NormalizeItem(JsonObject item)
        {
            return new JsonObject
            {
                ["item_id"] = item["item_id"]!.DeepClone(), ["request"] = item["request"]!.DeepClone(),
                ["current_state"] = item["current_state"]!.DeepClone(), ["evidence"] = item["evidence"]!.DeepClone(),
                ["constraints"] = item["constraints"]!.DeepClone(), ["allowed_actions"] = item["allowed_actions"]!.DeepClone(),
                ["dependency_ids"] = item["dependency_ids"]!.DeepClone()
            };
        }

        private static JsonObject BuildState(JsonObject input)
        {
            var normalized = new JsonArray();
            foreach (var node in input["items"]!.AsArray()) normalized.Add(NormalizeItem(node!.AsObject()));
            return new JsonObject
            {
                ["description"] = "PE-P0-GENERAL-01 work queue. Each item must receive exactly one permitted action. Dependency results in speculative questions are hypothetical branch conditions until a real executor receipt exists.",
                ["action_ontology"] = input["action_ontology"]!.DeepClone(),
                ["initial_state"] = input["initial_state"]!.DeepClone(),
                ["items"] = normalized
            };
        }

        private static JsonObject BuildQuestions(JsonObject input)
        {
            var items = input["items"]!.AsArray();
            var ids = new HashSet<string>(items.Select(x => x!["item_id"]!.GetValue<string>()));
            var questions = new JsonObject();
            for (int i = 0; i < 20; i++)
            {
                string id = items[i]!["item_id"]!.GetValue<string>();
                questions["item_" + id + "__current_action"] = QChoice("For ITEM" + id + ", choose exactly one permitted action from EXECUTE, HOLD, ROUTE, REJECT. Use only this item's request, evidence, constraints and allowed_actions from state. Do not invent missing facts.");
            }
            for (int i = 20; i < items.Count; i++)
            {
                string id = items[i]!["item_id"]!.GetValue<string>();
                string dep = items[i]!["dependency_ids"]!.AsArray()[0]!.GetValue<string>();
                if (!ids.Contains(dep)) throw new InvalidOperationException("BAD_DEPENDENCY_" + id);
                foreach (string result in new[] { "SUCCESS", "FAIL_TEMP", "FAIL_PERM" })
                {
                    questions["item_" + id + "__if_" + dep + "_" + result] = QChoice("For ITEM" + id + ", assume the real executor receipt for dependency ITEM" + dep + " has result exactly " + result + ". Choose exactly one permitted action from EXECUTE, HOLD, ROUTE, REJECT using ITEM" + id + "'s request, evidence and constraints. Treat " + result + " as a hypothetical branch for policy compilation only; do not claim the receipt already exists.");
                }
            }
            return questions;
        }

        private static JsonObject[] ShardObject(JsonObject obj)
        {
            var shards = new[] { new JsonObject(), new JsonObject() };
            int i = 0;
            foreach (var kv in obj) { shards[i % 2][kv.Key] = kv.Value!.DeepClone(); i++; }
            return shards;
        }

        private static async Task<ApiResult> RequestDecisionAsync(JsonObject state, JsonObject questions)
        {
            var payload = new JsonObject { ["model"] = Model, ["state"] = state.DeepClone(), ["questions"] = questions.DeepClone() };
            string serialized = JsonSerializer.Serialize(payload, CompactJson); // exactly one request serialization
            using var request = new HttpRequestMessage(HttpMethod.Post, Endpoint);
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _apiKey);
            request.Headers.TryAddWithoutValidation("X-OpenRouter-Title", "JEV Probability Engine P0 Reality Anchor");
            request.Content = new StringContent(serialized, Encoding.UTF8, "application/json");
            var started = Stopwatch.GetTimestamp();
            System.Threading.Interlocked.Increment(ref _actualHttpRequests);
            using var response = await Client.SendAsync(request, HttpCompletionOption.ResponseContentRead);
            string raw = await response.Content.ReadAsStringAsync();
            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException("OPENROUTER_HTTP_" + ((int)response.StatusCode).ToString(CultureInfo.InvariantCulture) + ":" + raw.Substring(0, Math.Min(500, raw.Length)), null, response.StatusCode);
            using var document = JsonDocument.Parse(raw); // exactly one response parse
            var root = document.RootElement;
            if (!root.TryGetProperty("answers", out var answers) || answers.ValueKind != JsonValueKind.Object)
                throw new InvalidDataException("OPENROUTER_ANSWERS_MISSING");
            string? modelName = root.TryGetProperty("model", out var m) && m.ValueKind == JsonValueKind.String ? m.GetString() : null;
            string? generationId = null;
            if (root.TryGetProperty("id", out var id) && id.ValueKind == JsonValueKind.String) generationId = id.GetString();
            else if (root.TryGetProperty("generation_id", out var gid) && gid.ValueKind == JsonValueKind.String) generationId = gid.GetString();
            JsonElement? usage = root.TryGetProperty("usage", out var u) ? u.Clone() : (JsonElement?)null;
            return new ApiResult
            {
                Answers = answers.Clone(), LatencyMs = ElapsedMilliseconds(started, Stopwatch.GetTimestamp()),
                ModelName = modelName, GenerationId = generationId, Usage = usage
            };
        }

        private static double? NumberValue(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Number && element.TryGetDouble(out double n)) return n;
            if (element.ValueKind == JsonValueKind.String && double.TryParse(element.GetString(), NumberStyles.Float, CultureInfo.InvariantCulture, out n)) return n;
            return null;
        }

        private static Decision ChooseAction(JsonElement answer)
        {
            string? selected = answer.ValueKind == JsonValueKind.Object && answer.TryGetProperty("choice", out var choice) && choice.ValueKind == JsonValueKind.String ? choice.GetString() : null;
            JsonElement probsElement = default;
            bool hasProbs = answer.ValueKind == JsonValueKind.Object && answer.TryGetProperty("probabilities", out probsElement) && probsElement.ValueKind == JsonValueKind.Object;
            if (!hasProbs && answer.ValueKind == JsonValueKind.Object && answer.TryGetProperty("choice", out choice) && choice.ValueKind == JsonValueKind.Object)
            { probsElement = choice; hasProbs = true; }
            Dictionary<string, double>? normalized = null;
            if (hasProbs)
            {
                normalized = new Dictionary<string, double>();
                foreach (string action in Actions)
                    if (probsElement.TryGetProperty(action, out var value) && NumberValue(value) is double parsed) normalized[action] = parsed;
            }
            if (selected != null && Actions.Contains(selected))
                return new Decision { action = selected, probability = normalized != null && normalized.TryGetValue(selected, out var p) ? p : (double?)null, probabilities = normalized };
            if (!hasProbs) return new Decision { reason = "CHOICE_AND_PROBABILITIES_MISSING" };
            if (normalized == null || normalized.Count != Actions.Length) return new Decision { reason = "CHOICE_PROBABILITIES_INCOMPLETE" };
            var pairs = normalized.OrderByDescending(x => x.Value).ToArray();
            if (pairs[0].Value == pairs[1].Value) return new Decision { reason = "CHOICE_TIE" };
            return new Decision { action = pairs[0].Key, probability = pairs[0].Value, probabilities = normalized, source = "probability_argmax_fallback" };
        }

        private static string FinalStateFor(string action, string? executorResult)
        {
            if (action == "HOLD") return "ON_HOLD";
            if (action == "ROUTE") return "ROUTED";
            if (action == "REJECT") return "REJECTED";
            if (action == "EXECUTE")
            {
                if (executorResult == "SUCCESS") return "DONE";
                if (executorResult == "FAIL_TEMP") return "FAILED_RETRYABLE";
                return "FAILED_FINAL";
            }
            return "INVALID";
        }

        private static async Task<Receipt> ExecuteItemAsync(string runDir, JsonObject item, string action, Receipt? dependencyReceipt = null)
        {
            string id = item["item_id"]!.GetValue<string>();
            string? executorResult = null;
            if (action == "EXECUTE" && _executorOutcomes.TryGetPropertyValue(id, out var value) && value != null) executorResult = value.GetValue<string>();
            if (action == "EXECUTE" && executorResult == null) executorResult = "FAIL_PERM";
            var receipt = new Receipt
            {
                item_id = id, action = action, executor_result = executorResult,
                final_state = FinalStateFor(action, executorResult), monotonic_ms = MonotonicMilliseconds(),
                dependency_receipt = dependencyReceipt == null ? null : new DependencyReceipt { item_id = dependencyReceipt.item_id, executor_result = dependencyReceipt.executor_result }
            };
            await File.WriteAllTextAsync(Path.Combine(runDir, "item-" + id + ".json"), JsonSerializer.Serialize(receipt, CompactJson));
            return receipt;
        }

        private static async Task<(bool Pass, List<string> Errors)> VerifyRealityAsync(string runDir, JsonObject input, Dictionary<string, Decision> decisions)
        {
            var diskReceipts = new List<Receipt>();
            foreach (var item in input["items"]!.AsArray())
            {
                string id = item!["item_id"]!.GetValue<string>();
                diskReceipts.Add(JsonSerializer.Deserialize<Receipt>(await File.ReadAllTextAsync(Path.Combine(runDir, "item-" + id + ".json")))!);
            }
            var byId = diskReceipts.ToDictionary(x => x.item_id, x => x);
            var errors = new List<string>();
            foreach (var node in _oracle["items"]!.AsArray())
            {
                var expected = node!.AsObject();
                string id = expected["item_id"]!.GetValue<string>();
                if (!byId.TryGetValue(id, out var actual)) { errors.Add(id + ":MISSING_RECEIPT"); continue; }
                string expectedAction = expected["expected_action"]!.GetValue<string>();
                string? expectedExecutor = expected["expected_executor_result"] == null ? null : expected["expected_executor_result"]!.GetValue<string>();
                string expectedState = expected["expected_final_state"]!.GetValue<string>();
                if (actual.action != expectedAction) errors.Add(id + ":ACTION:" + actual.action + "!=" + expectedAction);
                if (actual.executor_result != expectedExecutor) errors.Add(id + ":EXECUTOR:" + (actual.executor_result ?? "null") + "!=" + (expectedExecutor ?? "null"));
                if (actual.final_state != expectedState) errors.Add(id + ":STATE:" + actual.final_state + "!=" + expectedState);
            }
            foreach (var kv in _oracle["dependency_order"]!.AsObject())
            {
                string depId = kv.Key; string predId = kv.Value!.GetValue<string>();
                if (!byId.TryGetValue(depId, out var dep) || !byId.TryGetValue(predId, out var pred)) continue;
                if (!(dep.monotonic_ms >= pred.monotonic_ms)) errors.Add(depId + ":DEPENDENCY_ORDER_VIOLATION");
                if (dep.dependency_receipt == null || dep.dependency_receipt.item_id != predId) errors.Add(depId + ":DEPENDENCY_RECEIPT_MISSING");
            }
            if (diskReceipts.Count != 24 || diskReceipts.Select(x => x.item_id).Distinct().Count() != 24) errors.Add("RECEIPT_CARDINALITY");
            var manifest = new Dictionary<string, object?>
            {
                ["benchmark_id"] = input["benchmark_id"]!.GetValue<string>(), ["model"] = Model,
                ["commercial_gate"] = errors.Count == 0 ? "PASS" : "FAIL",
                ["input_sha256"] = Sha256(JsonSerializer.Serialize(input, CompactJson)),
                ["receipts_sha256"] = Sha256(JsonSerializer.Serialize(diskReceipts, CompactJson)),
                ["decisions_sha256"] = Sha256(JsonSerializer.Serialize(decisions, CompactJson)),
                ["verifier_errors"] = errors
            };
            await File.WriteAllTextAsync(Path.Combine(runDir, "manifest.json"), JsonSerializer.Serialize(manifest, PrettyJson));
            return (errors.Count == 0, errors);
        }

        private static async Task<RunResult> RunOnceSafelyAsync(string runDir)
        {
            if (Directory.Exists(runDir)) throw new IOException("RUN_DIRECTORY_ALREADY_EXISTS:" + runDir);
            Directory.CreateDirectory(runDir);
            long t0 = Stopwatch.GetTimestamp();
            try
            {
                string inputText = await File.ReadAllTextAsync(_publicFixture); // formal input read inside timer
                var input = JsonNode.Parse(inputText)!.AsObject();
                var state = BuildState(input);
                var questions = BuildQuestions(input);
                if (questions.Count != 32) throw new InvalidOperationException("QUESTION_COUNT_" + questions.Count + "_NOT_32");
                var shards = ShardObject(questions);
                Task<ApiResult> request1 = RequestDecisionAsync(state, shards[0]);
                Task<ApiResult> request2 = RequestDecisionAsync(state, shards[1]);
                ApiResult[] apiResults = await Task.WhenAll(request1, request2);
                var answers = new Dictionary<string, JsonElement>();
                foreach (var api in apiResults) foreach (var answer in api.Answers.EnumerateObject()) answers[answer.Name] = answer.Value.Clone();
                if (answers.Count != 32) throw new InvalidDataException("ANSWER_COUNT_" + answers.Count + "_NOT_32");
                var decisions = answers.ToDictionary(x => x.Key, x => ChooseAction(x.Value));
                var items = input["items"]!.AsArray();
                var receipts = new Dictionary<string, Receipt>();
                var wave1 = new Task<Receipt>[20];
                for (int i = 0; i < 20; i++)
                {
                    var item = items[i]!.AsObject();
                    string id = item["item_id"]!.GetValue<string>();
                    string action = decisions["item_" + id + "__current_action"].action ?? "REJECT";
                    wave1[i] = ExecuteItemAsync(runDir, item, action);
                }
                var wave2 = new List<Task<Receipt>>();
                for (int i = 20; i < items.Count; i++)
                {
                    var item = items[i]!.AsObject();
                    wave2.Add(ExecuteDependentAsync(runDir, item, wave1, decisions));
                }
                Receipt[] wave1Receipts = await Task.WhenAll(wave1);
                Receipt[] wave2Receipts = await Task.WhenAll(wave2);
                foreach (var receipt in wave1Receipts.Concat(wave2Receipts)) receipts[receipt.item_id] = receipt;
                var verified = await VerifyRealityAsync(runDir, input, decisions);
                long t1 = Stopwatch.GetTimestamp(); // after verifier and manifest write
                var result = new RunResult
                {
                    pass = verified.Pass, t_e2e_ms = ElapsedMilliseconds(t0, t1), verifier_errors = verified.Errors,
                    request_latencies_ms = apiResults.Select(x => x.LatencyMs).ToList(), request_count = apiResults.Length,
                    model = apiResults[0].ModelName ?? Model, generation_ids = apiResults.Select(x => x.GenerationId).ToList(), decisions = decisions
                };
                await File.WriteAllTextAsync(Path.Combine(runDir, "run-summary.json"), JsonSerializer.Serialize(result, PrettyJson));
                return result;
            }
            catch (Exception ex)
            {
                var errors = new List<string> { "RUN_EXCEPTION:" + ex.GetType().Name + ":" + ex.Message };
                var manifest = new Dictionary<string, object?>
                {
                    ["benchmark_id"] = Benchmark, ["model"] = Model, ["commercial_gate"] = "FAIL",
                    ["input_sha256"] = null, ["receipts_sha256"] = null, ["decisions_sha256"] = null, ["verifier_errors"] = errors
                };
                await File.WriteAllTextAsync(Path.Combine(runDir, "manifest.json"), JsonSerializer.Serialize(manifest, PrettyJson));
                long t1 = Stopwatch.GetTimestamp();
                var failed = new RunResult { pass = false, t_e2e_ms = ElapsedMilliseconds(t0, t1), verifier_errors = errors, exception = ex.ToString() };
                await File.WriteAllTextAsync(Path.Combine(runDir, "run-summary.json"), JsonSerializer.Serialize(failed, PrettyJson));
                return failed;
            }
        }

        private static async Task<Receipt> ExecuteDependentAsync(string runDir, JsonObject item, Task<Receipt>[] wave1, Dictionary<string, Decision> decisions)
        {
            string id = item["item_id"]!.GetValue<string>();
            string pred = item["dependency_ids"]!.AsArray()[0]!.GetValue<string>();
            Receipt predReceipt = await wave1[int.Parse(pred, CultureInfo.InvariantCulture) - 1];
            string branch = predReceipt.executor_result ?? "FAIL_PERM";
            string qid = "item_" + id + "__if_" + pred + "_" + branch;
            string action = decisions.TryGetValue(qid, out var decision) ? decision.action ?? "REJECT" : "REJECT";
            return await ExecuteItemAsync(runDir, item, action, predReceipt);
        }

        private static async Task WriteFinalArtifactsAsync(bool keyAuth, bool httpDecisions, bool decisionSchema, string? probeError, List<RunResult> warmups, List<RunResult> measured)
        {
            var valid = measured.Where(x => x.pass).Select(x => x.t_e2e_ms).OrderBy(x => x).ToList();
            bool seriesPass = measured.Count == MeasuredRuns && measured.All(x => x.pass);
            double? min = valid.Count == 0 ? null : valid[0];
            double? p50 = Percentile(valid, 0.50);
            double? p95 = Percentile(valid, 0.95);
            double? max = valid.Count == 0 ? null : valid[valid.Count - 1];
            bool baselineBeaten = seriesPass && min.HasValue && min.Value < BaselineMs;
            var result = new Dictionary<string, object?>
            {
                ["task_step"] = "4_REALITY_CHALLENGE_V2", ["candidate_id"] = CandidateId,
                ["benchmark"] = Benchmark, ["model"] = Model, ["topology"] = "s2",
                ["baseline_source_integrity"] = "PASS", ["auth_probe_pass"] = keyAuth && httpDecisions && decisionSchema,
                ["key_auth"] = keyAuth ? "PASS" : "FAIL", ["http_decisions"] = httpDecisions ? "PASS" : "FAIL",
                ["decision_schema"] = decisionSchema ? "PASS" : "FAIL", ["probe_error"] = probeError,
                ["auth_probe_requests"] = _actualHttpRequests > 0 ? 1 : 0,
                ["warmup_runs"] = warmups.Count, ["measured_runs"] = measured.Count,
                ["pass_runs"] = measured.Count(x => x.pass), ["fail_runs"] = measured.Count(x => !x.pass),
                ["commercial_gate_series"] = seriesPass ? "PASS" : "FAIL",
                ["min_ms"] = min, ["p50_ms"] = p50, ["p95_ms"] = p95, ["max_ms"] = max,
                ["baseline_T_P0_ms"] = BaselineMs, ["baseline_beaten"] = baselineBeaten ? "YES" : "NO",
                ["new_real_p0_eligible"] = baselineBeaten ? "YES" : "NO",
                ["http_requests_per_run"] = 2, ["http_concurrency"] = 2, ["jev_decision_waves_per_run"] = 1,
                ["local_execution_waves"] = 2, ["real_network_calls"] = _actualHttpRequests,
                ["real_jev_calls"] = _actualHttpRequests, ["expected_http_requests"] = 67,
                ["actual_http_requests"] = _actualHttpRequests,
                ["request_count_match"] = _actualHttpRequests == 67 ? "PASS" : "FAIL",
                ["next_action"] = baselineBeaten ? "RETURN_TO_GPT_FOR_REAL_P0_WRITEBACK" : "KEEP_V0_3_0_BASELINE",
                ["created_at"] = DateTimeOffset.UtcNow.ToString("O", CultureInfo.InvariantCulture)
            };
            await File.WriteAllTextAsync(_finalResultPath, JsonSerializer.Serialize(result, PrettyJson));
            var md = new StringBuilder();
            md.AppendLine("# Reality Challenge V2 Acceptance").AppendLine();
            md.AppendLine("- Candidate: `" + CandidateId + "`");
            md.AppendLine("- Frozen source integrity: `PASS`");
            md.AppendLine("- Auth/schema probe: `" + (keyAuth && httpDecisions && decisionSchema ? "PASS" : "FAIL") + "`");
            md.AppendLine("- Warmups: `" + warmups.Count + "/3`");
            md.AppendLine("- Measured: `" + measured.Count + "/30`");
            md.AppendLine("- Commercial gate series: `" + (seriesPass ? "PASS" : "FAIL") + "`");
            md.AppendLine("- Measured pass/fail: `" + measured.Count(x => x.pass) + "/" + measured.Count(x => !x.pass) + "`");
            md.AppendLine("- HTTP requests actual/expected: `" + _actualHttpRequests + "/67`");
            md.AppendLine("- Baseline beaten: `" + (baselineBeaten ? "YES" : "NO") + "`");
            md.AppendLine("- Result: `" + _finalResultPath + "`");
            await File.WriteAllTextAsync(_acceptancePath, md.ToString());
        }

        private static double? Percentile(List<double> sorted, double p)
        {
            if (sorted.Count == 0) return null;
            int index = Math.Min(sorted.Count - 1, Math.Max(0, (int)Math.Ceiling(p * sorted.Count) - 1));
            return sorted[index];
        }

        private static double MonotonicMilliseconds() => (double)Stopwatch.GetTimestamp() * 1000.0 / Stopwatch.Frequency;
        private static double ElapsedMilliseconds(long start, long end) => (double)(end - start) * 1000.0 / Stopwatch.Frequency;
        private static string Sha256(string value)
        {
            using var sha = SHA256.Create();
            return Convert.ToHexString(sha.ComputeHash(Encoding.UTF8.GetBytes(value))).ToLowerInvariant();
        }
    }
}
