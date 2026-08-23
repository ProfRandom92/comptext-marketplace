import crypto from 'node:crypto';
import fs from 'node:fs';

export function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, canonicalize(value[key])]))
  }
  return value;
}

export function canonicalText(value) { return JSON.stringify(canonicalize(value)); }
export function sha256Canonical(value) {
  return `sha256:${crypto.createHash('sha256').update(canonicalText(value)).digest('hex')}`;
}
if (process.argv[1] && process.argv[1].endsWith('canonical-json.mjs') && process.argv[2]) {
  const value = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  process.stdout.write(`${sha256Canonical(value)}\n${canonicalText(value)}\n`);
}
