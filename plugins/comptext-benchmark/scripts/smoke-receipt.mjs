import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const lab = process.argv[2] ?? '/root/comptext/apps/comptext-benchmark-lab';
const run = spawnSync(process.execPath, ['scripts/smoke.mjs'], {
  cwd: lab, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']
});
if (run.status !== 0) {
  process.stderr.write(run.stderr || run.stdout || 'smoke failed\n');
  process.exit(run.status ?? 1);
}

const dir = path.join(lab, '.data/smoke/smoke-orion-001');
const result = path.join(dir, 'result.json');
const receipt = path.join(dir, 'proof-summary.json');
const compiler = fileURLToPath(new URL('./proof-summary.mjs', import.meta.url));
const proof = spawnSync(process.execPath, [compiler, result, receipt], {
  encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']
});
if (proof.status !== 0) {
  process.stderr.write(proof.stderr || 'receipt compile failed\n');
  process.exit(proof.status ?? 1);
}
process.stdout.write(proof.stdout);