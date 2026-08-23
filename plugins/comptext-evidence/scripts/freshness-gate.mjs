import fs from 'node:fs';
import crypto from 'node:crypto';

const input = process.argv[2];
if (!input) { console.error('usage: node freshness-gate.mjs <trace.jsonl>'); process.exit(2); }
const raw = fs.readFileSync(input, 'utf8');
const lines = raw.split(/\r?\n/).filter(line => line.trim().length > 0);
let previousSeq = -1, lastMutation = null, lastVerification = null;
let verificationPending = true, hasVerification = false, latestClaim = null;
const currentReason = () => !hasVerification ? 'VERIFICATION_MISSING' : verificationPending ? 'VERIFICATION_STALE' : 'VERIFICATION_FRESH';
for (const line of lines) {
  const event = JSON.parse(line);
  if (!Number.isInteger(event.seq) || event.seq <= previousSeq) throw new Error('trace seq must be strictly increasing integers');
  previousSeq = event.seq;
  if (event.type === 'mutation' && event.success === true) { lastMutation = event.seq; verificationPending = true; }
  else if (event.type === 'verification' && event.success === true) { lastVerification = event.seq; hasVerification = true; verificationPending = false; }
  else if (event.type === 'completion_claim') latestClaim = {seq:event.seq, allowed:hasVerification && !verificationPending, reason:currentReason()};
}
const receipt = {
  schema:'comptext-evidence-freshness/v1', trace_digest:`sha256:${crypto.createHash('sha256').update(raw).digest('hex')}`,
  event_count:lines.length, last_successful_mutation_seq:lastMutation, last_successful_verification_seq:lastVerification,
  verification_pending:verificationPending, next_completion_allowed:hasVerification && !verificationPending,
  reason:currentReason(), latest_completion_claim:latestClaim
};
process.stdout.write(`${JSON.stringify(receipt)}\n`);
