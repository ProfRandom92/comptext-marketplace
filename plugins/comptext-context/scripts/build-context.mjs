import fs from 'node:fs';
import { canonicalText, sha256Canonical } from './canonical-json.mjs';

const [sourcePath, contractPath] = process.argv.slice(2);
if (!sourcePath || !contractPath) { console.error('usage: node build-context-ir.mjs <source-summary.json> <contract.json>'); process.exit(2); }
const source = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
const digestPattern = /^sha256:[0-9a-f]{64}$/;
if (!digestPattern.test(source.source_digest ?? '')) throw new Error('invalid source_digest');
if (!Array.isArray(source.field_paths)) throw new Error('field_paths must be an array');
if (!Array.isArray(contract.required_field_paths) || contract.required_field_paths.length === 0) throw new Error('required_field_paths must be non-empty');
const uniqSorted = values => [...new Set(values)].sort();
const orderedUnique = values => [...new Set(values)];
const sortEdges = values => [...values].sort((a,b) => `${a.source}\0${a.target}`.localeCompare(`${b.source}\0${b.target}`));
const required = uniqSorted(contract.required_field_paths);
const available = new Set(source.field_paths);
const satisfied = required.filter(path => available.has(path));
const missing = required.filter(path => !available.has(path));
const preimage = {
  schema: 'comptext-context/v1', source_digest: source.source_digest, strategy: contract.strategy,
  required_field_paths: required, satisfied_field_paths: satisfied, missing_field_paths: missing,
  constraints: uniqSorted(contract.constraints ?? []), required_order: orderedUnique(contract.required_order ?? []),
  dependency_edges: sortEdges(contract.dependency_edges ?? []), blockers: sortEdges(contract.blockers ?? []),
  recovery_paths: sortEdges(contract.recovery_paths ?? []),
  validation: {valid: missing.length === 0, failure_labels: missing.length ? ['MISSING_REQUIRED_FIELD'] : []},
  non_claims: uniqSorted(contract.non_claims ?? [])
};
const context = {...preimage, context_id: sha256Canonical(preimage)};
process.stdout.write(`${canonicalText(context)}\n`);
