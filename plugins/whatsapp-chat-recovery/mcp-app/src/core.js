const ROUTES = {
  android: {
    old_device: "Use WhatsApp's device-to-device transfer first; keep the old device unchanged until the transfer is verified.",
    backup: "Restore during WhatsApp setup with the same phone number and Google Account that created the backup.",
    export: "Preserve the export as readable evidence; WhatsApp cannot import it as a native chat.",
    none: "Preserve the device and authorized copies, then inventory local backups and exports before deeper forensic work.",
  },
  iphone: {
    old_device: "Use WhatsApp's supported iPhone transfer flow first; keep the old device unchanged until verification.",
    backup: "Restore the WhatsApp iCloud backup during setup with the same phone number and Apple ID.",
    export: "Preserve the export as readable evidence; WhatsApp cannot import it as a native chat.",
    none: "Preserve the device and authorized copies, then check iCloud backup status and exports before deeper forensic work.",
  },
  web: {
    old_device: "Export or transfer from the paired phone first; the phone remains the strongest supported recovery source.",
    backup: "Use the phone's supported backup restore flow; WhatsApp Web is not a replacement backup.",
    export: "Preserve the export and copied browser profile separately; do not open the evidence store in place.",
    none: "Copy the complete authorized browser profile read-only and inventory IndexedDB, Local Storage, and blob siblings.",
  },
};

export function planRecovery({ platform, availableSource, authorized, workingCopy }) {
  if (!authorized) {
    return {
      status: "blocked",
      route: "Stop: only the owner or an explicitly authorized examiner may continue.",
      nextAction: "Obtain explicit authorization; do not collect credentials or access another person's account.",
      warnings: ["No account-access, credential-capture, encryption-bypass, or covert-surveillance workflow is provided."],
    };
  }

  const warnings = [];
  if (!workingCopy) warnings.push("Create and hash a working copy before inspection; leave originals untouched.");
  warnings.push("Never send passwords, SMS codes, passkeys, or backup keys to this app.");
  const prerequisites = platform === "iphone"
    ? ["same phone number", "same Apple ID when restoring iCloud", "sufficient device storage"]
    : platform === "android"
      ? ["same phone number", "same Google Account when restoring cloud backup", "sufficient device storage"]
      : ["authorized copy of the complete browser profile", "paired phone or supported phone backup when available"];
  return {
    status: "ready",
    route: ROUTES[platform][availableSource],
    prerequisites,
    nextAction: workingCopy
      ? "Run a metadata-only inventory on the working copy and paste the JSON summary into the audit-review tool."
      : "Create a bit-preserving or ordinary verified copy appropriate to the evidence value, then calculate SHA-256.",
    warnings,
  };
}

export function reviewAudit(audit) {
  const files = Array.isArray(audit?.files) ? audit.files : [];
  const counts = {};
  const issues = [];
  let exactHitFiles = 0;
  for (const file of files) {
    const kind = typeof file?.kind === "string" ? file.kind : "unknown";
    counts[kind] = (counts[kind] ?? 0) + 1;
    if (file?.error || file?.zip_error) issues.push({ path: file.path ?? "unknown", issue: "read_error" });
    if (Array.isArray(file?.unsafe_member_paths) && file.unsafe_member_paths.length) {
      issues.push({ path: file.path ?? "unknown", issue: "unsafe_zip_paths", count: file.unsafe_member_paths.length });
    }
    if (file?.exact_identifier_hits && Object.keys(file.exact_identifier_hits).length) exactHitFiles += 1;
  }
  return {
    readOnlyClaim: audit?.read_only === true,
    filesReviewed: files.length,
    kinds: counts,
    exactHitFiles,
    issues,
    limitations: [
      "A filename or identifier hit does not prove message authorship, provenance, or completeness.",
      "A matching SHA-256 establishes byte identity only between compared copies.",
      "No hit cannot exclude deleted, encrypted, split, compacted, or missing data.",
    ],
    nextAction: issues.length
      ? "Resolve read errors and treat unsafe ZIP paths as metadata only; do not extract blindly."
      : "Corroborate material findings with a second parser and retain hashes, offsets, and tool versions.",
  };
}
