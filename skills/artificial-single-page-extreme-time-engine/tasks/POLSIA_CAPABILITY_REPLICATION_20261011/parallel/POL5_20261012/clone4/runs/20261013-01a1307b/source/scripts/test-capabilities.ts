import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { copyFile, mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { test } from "node:test";
import {
  CapabilityRequestError, createCapabilityService, getCapabilities,
  HISTORICAL_ASSET_ROOT, readCapabilityEvidence,
} from "../src/services/capabilities.ts";

function hasStatus(status: number) {
  return (error: unknown) => error instanceof CapabilityRequestError && error.statusCode === status;
}

test("all nine categories expose frozen evidence without claiming live integration", async () => {
  const catalog = await getCapabilities();
  assert.equal(catalog.capabilities.length, 9);
  assert.equal(new Set(catalog.capabilities.map((item) => item.id)).size, 9);
  assert.equal(catalog.functionalIntegrated, false);
  assert.equal(catalog.historicalReplay, "DISABLED");
  assert.equal(catalog.monitorOwnership, "EXTERNAL_OWNER_UNCHANGED");
  for (const item of catalog.capabilities) {
    assert.equal(item.availability, "OFFLINE_READONLY", item.id);
    assert.equal(item.functionalIntegrated, false);
    assert.ok(item.gaps.length > 0);
    for (const ref of item.evidence) {
      assert.equal(ref.status, "READABLE_PINNED", ref.relativePath);
      const doc = await readCapabilityEvidence(item.id, ref.id);
      const actual = await readFile(path.join(HISTORICAL_ASSET_ROOT, ref.relativePath));
      assert.equal(doc.content, new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(actual));
      assert.deepEqual(Buffer.from(doc.content, "utf-8"), actual);
      assert.equal(doc.sha256, createHash("sha256").update(actual).digest("hex").toUpperCase());
      assert.equal(doc.sha256, ref.expectedSha256);
      assert.equal(doc.operation, "READONLY_EVIDENCE_READ");
      assert.equal(doc.functionalIntegrated, false);
    }
  }
});

test("finance invocation reads the existing synthetic ledger and never reruns it", async () => {
  const doc = await readCapabilityEvidence("finance");
  assert.equal(doc.evidenceId, "ledger");
  assert.equal(doc.bytes, 839);
  assert.match(doc.content, /MATCHED/);
  assert.match(doc.content, /UNPAID/);
  assert.match(doc.content, /REVIEW_CURRENCY/);
  assert.equal(doc.sha256, "79E80E1A9C1F66E508A6B4EA86DBFB44CD33CAE9B5E22EAA2E3FB93006959756");
});

test("request IDs reject traversal, absolute paths, encoded paths and cross-category evidence", async () => {
  for (const id of ["../finance", "..\\finance", "C:\\Users\\A\\.env", "%2e%2e", "finance/ledger", "finance\u0000"]) {
    await assert.rejects(readCapabilityEvidence(id), hasStatus(400));
    await assert.rejects(readCapabilityEvidence("finance", id), hasStatus(400));
  }
  await assert.rejects(readCapabilityEvidence("missing"), hasStatus(404));
  await assert.rejects(readCapabilityEvidence("finance", "faq"), hasStatus(404));
  await assert.rejects(readCapabilityEvidence("finance", ".env"), hasStatus(400));
});

test("missing or modified source fails closed and cannot leak unrelated files", async () => {
  // Fixture stays in the integration workspace; historical sources are never modified.
  const parent = path.resolve(".pcl02");
  await mkdir(parent, { recursive: true });
  const root = await mkdtemp(path.join(parent, "integrity-"));
  const target = path.join(root, "nodes/CODEX-008/scenario/output/ledger.csv");
  await mkdir(path.dirname(target), { recursive: true });
  const fixture = createCapabilityService(root);
  await assert.rejects(fixture.readCapabilityEvidence("finance"), hasStatus(404));
  await copyFile(path.join(HISTORICAL_ASSET_ROOT, "nodes/CODEX-008/scenario/output/ledger.csv"), target);
  const valid = await fixture.readCapabilityEvidence("finance");
  const tampered = Buffer.from(await readFile(target));
  tampered[0] = tampered[0] === 65 ? 66 : 65; // same length, different content
  await writeFile(target, tampered);
  await assert.rejects(fixture.readCapabilityEvidence("finance"), hasStatus(409));
  const catalog = await fixture.getCapabilities();
  const finance = catalog.capabilities.find((item) => item.id === "finance")!;
  assert.equal(finance.availability, "EVIDENCE_UNAVAILABLE");
  assert.equal(finance.evidence[0]!.status, "INTEGRITY_ERROR");
  assert.equal(valid.integrity, "PINNED_SHA256_MATCH");
  await writeFile(path.join(root, ".env"), "DO_NOT_DISCLOSE_TEST_MARKER");
  await assert.rejects(fixture.readCapabilityEvidence("finance", "env"), hasStatus(404));
});
