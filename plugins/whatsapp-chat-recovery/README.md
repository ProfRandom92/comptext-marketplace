# WhatsApp Chat Recovery

Privacy-first, read-only recovery guidance and forensic triage for WhatsApp data that the operator owns or is authorized to examine.

## Features

- Inventory Android `msgstore*.crypt*` backups without decrypting them.
- Detect common multilingual WhatsApp text-export names and inspect ZIP member metadata without extraction.
- Inventory copied Chromium/WhatsApp Web IndexedDB and LevelDB components, hashes, and exact identifier hits.
- Scan binary fragments for CRC32C-valid LevelDB physical log records; report offsets, types, lengths, and exact UTF-8 hit counts without emitting payload bytes.
- Preserve limitations: a valid physical record does not prove WhatsApp semantics or reconstruct a complete write batch; no hits do not prove absence when data is partial or split.
- Offer an OpenAI MCP app that turns device/source facts into a least-destructive recovery plan and renders a compact in-chat result.
- Review only the bounded JSON summary from the local artifact auditor, keeping raw message content and credentials out of MCP requests.

## OpenAI MCP app

The app in [`mcp-app/`](mcp-app/) deliberately separates **local evidence acquisition** from **remote decision support**:

1. Run the bundled Python auditor on an authorized working copy. It emits metadata, hashes, counts, and offsets but no arbitrary message bodies.
2. Connect the deployed `/mcp` endpoint to ChatGPT and use `plan_whatsapp_recovery` for route selection.
3. If useful, pass the auditor's JSON output—not the source files—to `review_whatsapp_audit` for a bounded summary and next action.

This split avoids pretending that a hosted MCP server can read a path on the user's computer, reduces sensitive data transfer, and keeps evidence tooling read-only. The app never asks for passwords, SMS codes, passkeys, 64-digit backup keys, or message bodies.

### Run locally

Requires Node.js 20 or newer:

```bash
cd mcp-app
npm install
npm test
npm start
```

The Streamable HTTP endpoint is `http://localhost:8787/mcp`; `GET /health` is available for deployment checks. To use it as a ChatGPT app, deploy the directory behind a public HTTPS URL, keep `/mcp` reachable, and add that URL as the app's MCP server in the ChatGPT developer interface. Add authentication before introducing any user-specific server-side storage; the included server is intentionally stateless and stores nothing.

The widget consumes only MCP `structuredContent`. Tool descriptors declare read-only, non-destructive behavior, and the resource CSP permits no network or external-resource domains.

## Safety

Use only data you own or are authorized to examine. Preserve originals and work from copies. Do not request account credentials, keys, or verification codes in chat. The plugin does not bypass encryption or promise recovery. Native WhatsApp backups must be restored through WhatsApp's supported flow.

## Test

From the plugin directory, run:

```bash
python -m unittest discover -s skills/whatsapp-recovery/tests -v
```

The tests use synthetic bytes only.
