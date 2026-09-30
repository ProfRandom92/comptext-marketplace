import test from "node:test";
import assert from "node:assert/strict";
import { planRecovery, reviewAudit } from "../src/core.js";

test("blocks unauthorized recovery", () => {
  const result = planRecovery({ platform: "android", availableSource: "backup", authorized: false, workingCopy: false });
  assert.equal(result.status, "blocked");
  assert.match(result.nextAction, /authorization/i);
});

test("prefers supported Android transfer", () => {
  const result = planRecovery({ platform: "android", availableSource: "old_device", authorized: true, workingCopy: true });
  assert.equal(result.status, "ready");
  assert.match(result.route, /device-to-device/);
});

test("summarizes audit without message content", () => {
  const result = reviewAudit({ read_only: true, files: [
    { path: "copy/000001.log", kind: "whatsapp_chromium_leveldb_component", exact_identifier_hits: { "1@lid": { count: 2 } } },
    { path: "export.zip", kind: "zip_archive", unsafe_member_paths: ["../escape.txt"] },
  ] });
  assert.equal(result.filesReviewed, 2);
  assert.equal(result.exactHitFiles, 1);
  assert.deepEqual(result.kinds, { whatsapp_chromium_leveldb_component: 1, zip_archive: 1 });
  assert.equal(result.issues[0].issue, "unsafe_zip_paths");
});
