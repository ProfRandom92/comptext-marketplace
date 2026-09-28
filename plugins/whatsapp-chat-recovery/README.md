# WhatsApp Chat Recovery

Privacy-first, read-only recovery guidance and forensic triage for WhatsApp data that the operator owns or is authorized to examine.

## Features

- Inventory Android `msgstore*.crypt*` backups without decrypting them.
- Detect common multilingual WhatsApp text-export names and inspect ZIP member metadata without extraction.
- Inventory copied Chromium/WhatsApp Web IndexedDB and LevelDB components, hashes, and exact identifier hits.
- Scan binary fragments for CRC32C-valid LevelDB physical log records; report offsets, types, lengths, and exact UTF-8 hit counts without emitting payload bytes.
- Preserve limitations: a valid physical record does not prove WhatsApp semantics or reconstruct a complete write batch; no hits do not prove absence when data is partial or split.

## Safety

Use only data you own or are authorized to examine. Preserve originals and work from copies. Do not request account credentials, keys, or verification codes in chat. The plugin does not bypass encryption or promise recovery. Native WhatsApp backups must be restored through WhatsApp's supported flow.

## Test

From this directory, run:

```bash
python -m unittest discover -s tests -v
```

The tests use synthetic bytes only.
