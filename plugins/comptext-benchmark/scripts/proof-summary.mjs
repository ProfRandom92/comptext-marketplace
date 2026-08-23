import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const input = process.argv[2];
const output = process.argv[3];
if (!input) {
  console.error('usage: node proof-summary.mjs <result.json> [proof-summary.json]');
  process.exit(2);
}

const raw = fs.readFileSync(input);
const result = JSON.parse(raw);
const c = result.comparison ?? {};
const b = c.baseline ?? {};
const x = c.comptext ?? {};
const d = c.deltas ?? {};
const q = ['task_success','semantic_fidelity','constraint_survival','negation_survival','contradiction_count','hallucination_or_overclaim_count'];
const e = ['input_tokens','output_tokens','effective_context_tokens','latency_ms','retries','tool_calls'];
const pick = (obj, keys) => Object.fromEntries(keys.filter(k => k in obj).map(k => [k, obj[k]]));
const proof = {
  schema: 'comptext-proof-summary/v1',
  run_id: result.run_id,
  status: result.status,
  manifest_digest: result.manifest_digest,
  result_digest: `sha256:${crypto.createHash('sha256').update(raw).digest('hex')}`,
  runner: result.manifest?.runner ?? result.arm_results?.[0]?.runner ?? null,
  model: result.manifest?.model ?? null,
  arms: (result.arm_results ?? []).map(a => ({id: a.arm_id,status: a.status,evidence: (a.evidence ?? []).map(v => v.ref).filter(Boolean)})),
  quality: { raw: pick(b,q), comptext: pick(x,q), delta: pick(d,q) },
  efficiency: {raw: pick(b,e), comptext: pick(x,e), delta: pick(d,e), token_reduction_ratio: c.efficiency?.token_reduction_ratio ?? null},
  regressions: c.regression_flags ?? {},
  verdict: c.overall ?? null,
  artifacts: { result: input, receipt: output ?? null }
};
const text = `${JSON.stringify(proof)}\n`;
if (output) {fs.mkdirSync(path.dirname(output), { recursive: true }); fs.writeFileSync(output, text, { flag: 'w' });}
process.stdout.write(text);
