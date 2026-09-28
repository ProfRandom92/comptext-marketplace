# Forensic references

Checked 2026-09-28.

- Google dfIndexedDB: https://github.com/google/dfindexeddb
  - Parses Chromium IndexedDB/LevelDB, `.ldb`, `.log`, and MANIFEST/descriptor structures.
- CCL Chromium Reader: https://github.com/cclgroupltd/ccl_chrome_indexeddb
  - Chromium/LevelDB/IndexedDB/V8/Blink forensic reader; surfaces old/deleted record versions in raw LevelDB traversal.
- SecurityRonin chromium-storage-forensic: https://github.com/SecurityRonin/chromium-storage-forensic
  - Read-only raw Chromium storage readers; surfaces tombstones and superseded LevelDB versions.
- SecurityRonin whatsapp-desktop-forensic: https://github.com/SecurityRonin/whatsapp-desktop-forensic
  - WhatsApp Web/Electron `model-storage` parser for typed chats/messages/contacts/media and deleted-message recovery from tombstones; encrypted bodies are surfaced, not fabricated.
- Akbal et al., Browser Forensic Investigations of WhatsApp Web Utilizing IndexedDB Persistent Storage, Future Internet 12(11):184 (2020): https://doi.org/10.3390/fi12110184

- Google LevelDB log record format: https://github.com/google/leveldb/blob/main/doc/log_format.md
