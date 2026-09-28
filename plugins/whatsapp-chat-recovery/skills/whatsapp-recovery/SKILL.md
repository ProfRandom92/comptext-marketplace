---
name: whatsapp-recovery
description: Recover and audit the user's own WhatsApp data from official backups, exports, copied device folders, or Chromium/WhatsApp Web forensic artifacts. Use for missing chats, msgstore crypt backups, exported ZIP/TXT, Google Drive inventory, Chromium IndexedDB/LevelDB, or read-only recovery triage. Never access someone else's account, bypass encryption, or modify evidence without explicit approval.
---

# WhatsApp Chat Recovery + Forensic Triage

Work only with data the user owns or is explicitly authorized to examine. Preserve originals and clearly distinguish a recoverable backup, an export, browser residue, and metadata-only evidence.

## Core preservation rules

1. Diagnose read-only first. Do not uninstall WhatsApp, clear app data, factory-reset devices, rename/move original backup files, compact LevelDB, or open an evidence store with a tool that may write to it.
2. If deleted-data recovery from a Windows SSD is relevant, minimize writes to the source volume. Prefer copied artifacts or a forensic image. Do not promise recovery after TRIM/overwrite.
3. Hash copied evidence with SHA-256. A matching hash proves byte identity between copies, not provenance or truth of the content.
4. Never request passwords, SMS codes, passkeys, 64-digit backup keys, or account credentials in chat. Encrypted backups require the user to enter the credential directly into WhatsApp's supported restore flow.
5. Treat incriminating and exculpatory material symmetrically. Do not selectively suppress evidence.

## Recovery routes

- Android → Android: prefer WhatsApp device-to-device transfer from the old device. Otherwise restore during setup using the same phone number and Google Account that created the backup.
- iPhone → iPhone: restore the WhatsApp iCloud backup during setup using the same Apple ID/iCloud Drive and phone number.
- Android local backup: preserve the complete `WhatsApp/Databases` folder. Newer Android commonly uses `Android/media/com.whatsapp/WhatsApp/Databases`.
- Exported ZIP/TXT: readable reference/evidence only. Standard WhatsApp does not import an export back as the original conversation.
- No backup + old device unavailable: inspect only authorized copies, browser artifacts, exports, cloud files, and forensic images. WhatsApp is not a server-side archive service for old chat history.

## Multilingual export handling

Recognize common exported chat names including at least:
- `WhatsApp Chat with <name>.txt`
- `WhatsApp-Chat mit <name>.txt`
- `Chat de WhatsApp con <name>.txt`
- `Discussion WhatsApp avec <name>.txt`
- `Chat WhatsApp con <name>.txt`

Do not infer that a ZIP is unrelated just because its outer filename is generic. Inspect ZIP member names read-only; never extract automatically.

## Chromium / WhatsApp Web forensic mode

When the user has copied Chromium artifacts, treat the entire store directory as evidence. Relevant paths often include:

`.../User Data/<Profile>/IndexedDB/https_web.whatsapp.com_0.indexeddb.leveldb/`

Also preserve sibling WhatsApp-origin storage such as Local Storage and any `.blob` directory when present. A LevelDB directory may contain `CURRENT`, `MANIFEST-*`, `.ldb`/`.sst`, `.log`, `LOCK`, and `LOG` files. Recent writes may exist only in the WAL `.log`; old/superseded versions and tombstones may remain until compaction.

For exact-person correlation, prefer immutable identifiers over names:
- phone-number JID / PN JID such as `<digits>@c.us` or `<digits>@s.whatsapp.net`
- LID such as `<digits>@lid`

Do not equate a broad display-name hit with a target person when exact identifiers are available.

### Parser cross-check order

For copied evidence, prefer two independent decoders when the result matters:
1. Google `dfindexeddb` for Chromium IndexedDB/LevelDB structure, `.ldb`, `.log`, and MANIFEST parsing.
2. `ccl_chromium_reader` or a second independent Chromium IndexedDB/V8 decoder.
3. A WhatsApp-aware parser such as `whatsapp-desktop-forensic` for `model-storage` message/chat/contact/media interpretation and tombstone recovery.

Do not treat one parser's field interpretation as unquestionable; schema drift exists. If parsers disagree, report the disagreement and preserve raw offsets/sequence numbers.

### Encrypted message bodies

Modern WhatsApp Web artifacts can contain encrypted body envelopes such as `msgRowOpaqueData`. Do not fabricate plaintext. Preserve the envelope and report that decryption needs valid key material from the same authorized profile/session. Do not provide credential theft or key-bypass workflows.

## Connected-app workflow

### Google Drive
Use for the user's own normal Drive files only. First pass should be metadata-oriented: names, paths/links, sizes, modification times, and hashes when materialized. Native WhatsApp Google Account backups may not be exposed as ordinary Drive files and normally must be restored through WhatsApp.

### Desktop Commander
Use only with explicit user approval for local filesystem actions. Prefer listing, metadata, hashing, and read-only scanning. Do not run recovery tools, copy evidence, or start processes without the user's approval for that action.

## Bundled scripts

### General artifact audit
`python scripts/audit_whatsapp_artifacts.py PATH [--identifier VALUE ...] [--json]`

Read-only. Detects multilingual exports, ZIP members, `msgstore*.crypt*`, WhatsApp Chromium LevelDB components, hashes files, and can search exact identifiers without printing arbitrary message bodies.

### Chromium store triage
`python scripts/audit_whatsapp_chromium.py PATH [--identifier VALUE ...] [--json]`

Read-only structural inventory for copied WhatsApp Web IndexedDB/LevelDB directories. Reports expected LevelDB components, hashes, exact identifier hit counts/offsets, and basic SSTable-footer validation. It does not open the store through LevelDB, compact it, decrypt it, or modify evidence.

## Response format

Return: (1) strongest safe recovery route, (2) prerequisites, (3) what was preserved/hashed, (4) concrete findings with file/offset/identifier when available, (5) limitations and uncertainty, and (6) the next least-destructive action.

## References
See `references/official-sources.md` and `references/forensic-sources.md`.


### Fragmented LevelDB log triage

A parser failing at byte zero only rules out parsing that file as an intact log from its beginning. For unidentified fragments, scan for independently CRC32C-valid LevelDB physical log records before concluding that no valid record exists:

`python scripts/scan_leveldb_log_fragments.py PATH [--identifier VALUE ...] [--source-offset N] [--json]`

The scanner is read-only, limits scans to 64 MiB by default, reports offsets, physical record types, lengths, and exact UTF-8 identifier hit counts, and never prints payload bytes. Supply `--source-offset` only when the fragment's original byte offset in the log is known; this enables 32-KB block-boundary validation. A valid physical record proves only that its header and CRC32C match. It does not establish that the record belongs to WhatsApp or reconstruct a complete logical write batch. Zero hits are bounded to the scanned bytes and cannot exclude partial records or data split across fragments.

Run synthetic regression tests from the plugin directory with `python -m unittest discover -s tests -v`.
