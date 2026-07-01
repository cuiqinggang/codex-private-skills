import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const scriptRoot = path.resolve(path.dirname(scriptPath), '..');
const args = process.argv.slice(2);
const selfTest = args.includes('--self-test');
const jsonOut = args.includes('--json');
const taskArg = args.find((arg) => arg.startsWith('--task-text='));
const evidenceArg = args.find((arg) => arg.startsWith('--evidence='));
const timelineArg = args.find((arg) => arg.startsWith('--timeline='));

const runtimeKeywords = [
  '2H',
  '4H',
  '8H',
  'two-hour',
  'four-hour',
  'eight-hour',
  'long-task',
  'endurance',
  'runtime',
  'runtime-enforced',
  'continuous runtime',
  '长任务',
  '两小时',
  '四小时',
  '八小时',
  '耐力运行'
];

function detectRuntime(text) {
  const source = String(text || '');
  return runtimeKeywords.some((kw) => source.toLowerCase().includes(kw.toLowerCase()));
}

function inferMinimum(text, evidence = {}) {
  const source = String(text || '');
  if (Number.isFinite(evidence.minimum_runtime_minutes) && evidence.minimum_runtime_minutes > 0) {
    return evidence.minimum_runtime_minutes;
  }
  if (/8H|eight-hour|八小时/i.test(source)) return 480;
  if (/4H|four-hour|四小时/i.test(source)) return 240;
  if (/2H|two-hour|两小时/i.test(source)) return 120;
  if (/30min|30 min|30分钟/i.test(source)) return 30;
  return Number(evidence.declared_runtime_minutes || 0);
}

function requiredCheckpoints(minimum) {
  if (minimum >= 480) return 32;
  if (minimum >= 240) return 16;
  if (minimum >= 120) return 8;
  if (minimum >= 30) return 2;
  return 0;
}

function validateEvidence({ taskText = '', evidence = null, timelineExists = false, patchInstall = false }) {
  const runtimeRequired = detectRuntime(taskText) || (!patchInstall && evidence && Number(evidence.minimum_runtime_minutes || 0) > 0);
  const checks = [];
  const fail = (code, message) => checks.push({ passed: false, code, message });
  const pass = (code, message) => checks.push({ passed: true, code, message });

  if (!runtimeRequired) {
    pass('PATCH_INSTALL_PASS', 'No runtime keyword detected; patch install can finish quickly.');
    return {
      pass: true,
      final_status_allowed: true,
      status_code: 'PATCH_INSTALL_PASS',
      runtime_required: false,
      checks
    };
  }

  if (!evidence) {
    fail('RUNTIME_GATE_FAIL_EVIDENCE_MISSING', 'runtime-evidence.json is required for runtime-enforced tasks.');
    return {
      pass: false,
      final_status_allowed: false,
      status_code: 'RUNTIME_GATE_FAIL_EVIDENCE_MISSING',
      runtime_required: true,
      checks
    };
  }

  const minimum = inferMinimum(taskText, evidence);
  const elapsed = Number(evidence.elapsed_minutes || 0);
  const checkpointCount = Number(evidence.checkpoint_count ?? (Array.isArray(evidence.checkpoints) ? evidence.checkpoints.length : 0));
  const checkpointMin = requiredCheckpoints(minimum);

  if (!evidence.started_at || !evidence.ended_at) {
    fail('RUNTIME_GATE_FAIL_EVIDENCE_MISSING', 'started_at and ended_at are required.');
  } else {
    pass('RUNTIME_GATE_TIMESTAMPS_PRESENT', 'started_at and ended_at are present.');
  }

  if (elapsed < minimum) {
    fail('RUNTIME_GATE_FAIL_ELAPSED_TOO_SHORT', `elapsed_minutes ${elapsed} < minimum_runtime_minutes ${minimum}.`);
  } else {
    pass('RUNTIME_GATE_ELAPSED_OK', `elapsed_minutes ${elapsed} >= ${minimum}.`);
  }

  if (minimum >= 120 && elapsed < 10) {
    fail('2H_RUNTIME_PASS_FORBIDDEN', 'Runtime task completed in under 10 minutes.');
  }

  if (checkpointCount < checkpointMin) {
    fail('RUNTIME_GATE_FAIL_CHECKPOINTS_TOO_FEW', `checkpoint_count ${checkpointCount} < required ${checkpointMin}.`);
  } else {
    pass('RUNTIME_GATE_CHECKPOINTS_OK', `checkpoint_count ${checkpointCount} >= ${checkpointMin}.`);
  }

  const checkpoints = Array.isArray(evidence.checkpoints) ? evidence.checkpoints : [];
  if (checkpointMin > 0 && checkpoints.length > 0) {
    const requiredFields = [
      'timestamp',
      'elapsed_minutes',
      'phase_name',
      'files_read',
      'files_written',
      'samples_processed',
      'accepted_count',
      'rejected_count',
      'needs_human_count',
      'current_risks',
      'next_action'
    ];
    for (const [index, checkpoint] of checkpoints.entries()) {
      for (const field of requiredFields) {
        if (!(field in checkpoint)) {
          fail('RUNTIME_GATE_FAIL_CHECKPOINT_FIELDS_MISSING', `checkpoint ${index} missing ${field}.`);
        }
      }
    }
  }

  const finalCheckpointExists = checkpoints.some((cp) => Number(cp.elapsed_minutes || 0) >= minimum) || checkpointCount > checkpointMin;
  if (!finalCheckpointExists) {
    fail('RUNTIME_GATE_FAIL_FINAL_CHECKPOINT_MISSING', 'final checkpoint is missing.');
  } else {
    pass('RUNTIME_GATE_FINAL_CHECKPOINT_OK', 'final checkpoint exists.');
  }

  if (!timelineExists) {
    fail('RUNTIME_GATE_FAIL_TIMELINE_MISSING', 'checkpoint-timeline.html is required.');
  } else {
    pass('RUNTIME_GATE_TIMELINE_OK', 'checkpoint-timeline.html exists.');
  }

  const hardFailures = checks.filter((check) => !check.passed);
  const passed = hardFailures.length === 0 && evidence.runtime_gate_passed === true && evidence.final_status_allowed === true;
  if (!evidence.runtime_gate_passed) {
    fail('RUNTIME_GATE_FAIL_FLAG_FALSE', 'runtime_gate_passed must be true.');
  }
  if (!evidence.final_status_allowed) {
    fail('RUNTIME_GATE_FAIL_FINAL_STATUS_NOT_ALLOWED', 'final_status_allowed must be true.');
  }

  const finalFailures = checks.filter((check) => !check.passed);
  return {
    pass: finalFailures.length === 0,
    final_status_allowed: finalFailures.length === 0,
    status_code: finalFailures.length === 0 ? 'RUNTIME_GATE_PASS' : finalFailures[0].code,
    runtime_required: true,
    minimum_runtime_minutes: minimum,
    elapsed_minutes: elapsed,
    checkpoint_count: checkpointCount,
    required_checkpoint_count: checkpointMin,
    checks
  };
}

function runSelfTest() {
  const checkpoints = (count, finalElapsed = 120) => Array.from({ length: count }, (_, i) => ({
    timestamp: `2026-06-14T00:${String(i).padStart(2, '0')}:00Z`,
    elapsed_minutes: i === count - 1 ? finalElapsed : i * 15,
    phase_name: `checkpoint-${i}`,
    files_read: [],
    files_written: [],
    samples_processed: i,
    accepted_count: i,
    rejected_count: 1,
    needs_human_count: 1,
    current_risks: [],
    next_action: 'continue'
  }));

  const cases = [
    {
      name: '2h_6min_should_fail',
      expectPass: false,
      result: validateEvidence({
        taskText: '2H task',
        timelineExists: true,
        evidence: {
          task_id: 'case1',
          declared_runtime_minutes: 120,
          minimum_runtime_minutes: 120,
          started_at: 'a',
          ended_at: 'b',
          elapsed_minutes: 6,
          checkpoint_count: 1,
          checkpoint_interval_minutes: 15,
          runtime_gate_passed: false,
          formal_files_modified: [],
          final_status_allowed: false,
          checkpoints: checkpoints(1, 6)
        }
      })
    },
    {
      name: '2h_121min_should_pass',
      expectPass: true,
      result: validateEvidence({
        taskText: '2H task',
        timelineExists: true,
        evidence: {
          task_id: 'case2',
          declared_runtime_minutes: 120,
          minimum_runtime_minutes: 120,
          started_at: 'a',
          ended_at: 'b',
          elapsed_minutes: 121,
          checkpoint_count: 9,
          checkpoint_interval_minutes: 15,
          runtime_gate_passed: true,
          formal_files_modified: [],
          final_status_allowed: true,
          checkpoints: checkpoints(9, 121)
        }
      })
    },
    {
      name: 'patch_6min_allowed',
      expectPass: true,
      result: validateEvidence({
        taskText: 'patch install task',
        timelineExists: false,
        patchInstall: true,
        evidence: null
      })
    },
    {
      name: '4h_120min_should_fail',
      expectPass: false,
      result: validateEvidence({
        taskText: '4H task',
        timelineExists: true,
        evidence: {
          task_id: 'case4',
          declared_runtime_minutes: 240,
          minimum_runtime_minutes: 240,
          started_at: 'a',
          ended_at: 'b',
          elapsed_minutes: 120,
          checkpoint_count: 16,
          checkpoint_interval_minutes: 15,
          runtime_gate_passed: false,
          formal_files_modified: [],
          final_status_allowed: false,
          checkpoints: checkpoints(16, 120)
        }
      })
    }
  ];

  const runtime_gate_cases = Object.fromEntries(
    cases.map((item) => [item.name, item.result.pass === item.expectPass ? 'PASS' : 'FAIL'])
  );
  const pass = Object.values(runtime_gate_cases).every((value) => value === 'PASS');
  return {
    pass,
    status_code: pass ? 'VERIFICATION_PASS' : 'VERIFICATION_FAIL',
    runtime_gate_cases,
    cases
  };
}

function loadJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

let result;
if (selfTest) {
  result = runSelfTest();
} else {
  const taskText = taskArg ? taskArg.slice('--task-text='.length) : '';
  const evidenceFile = evidenceArg ? evidenceArg.slice('--evidence='.length) : '';
  const timelineFile = timelineArg ? timelineArg.slice('--timeline='.length) : '';
  const evidence = evidenceFile && fs.existsSync(evidenceFile) ? loadJson(evidenceFile) : null;
  const timelineExists = timelineFile ? fs.existsSync(timelineFile) : false;
  result = validateEvidence({ taskText, evidence, timelineExists });
}

if (jsonOut) {
  console.log(JSON.stringify(result, null, 2));
} else if (result.pass) {
  console.log('VERIFICATION_PASS');
  if (result.runtime_gate_cases) {
    console.log('runtime_gate_cases:');
    for (const [name, status] of Object.entries(result.runtime_gate_cases)) {
      console.log(`- ${name}: ${status}`);
    }
  } else {
    console.log(result.status_code);
  }
} else {
  console.log('VERIFICATION_FAIL');
  console.log(result.status_code);
}

if (!result.pass) process.exit(1);

