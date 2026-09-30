import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import { planRecovery, reviewAudit } from "./core.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const widgetHtml = await fs.readFile(path.join(here, "../web/recovery-widget.html"), "utf8");
const WIDGET_URI = "ui://whatsapp-recovery/recovery-widget.html";

function result(title, data) {
  return {
    structuredContent: { title, ...data },
    content: [{ type: "text", text: `${title}: ${data.nextAction ?? data.route}` }],
    _meta: { "openai/outputTemplate": WIDGET_URI },
  };
}

function createServer() {
  const server = new McpServer({ name: "whatsapp-recovery", version: "0.1.0" });
  server.registerResource("recovery-widget", WIDGET_URI, {}, async () => ({
    contents: [{
      uri: WIDGET_URI,
      mimeType: "text/html+skybridge",
      text: widgetHtml,
      _meta: {
        "openai/widgetDescription": "Shows a privacy-first WhatsApp recovery route, prerequisites, warnings, and next action.",
        "openai/widgetPrefersBorder": true,
        "openai/widgetCSP": { connect_domains: [], resource_domains: [] },
      },
    }],
  }));

  server.registerTool("plan_whatsapp_recovery", {
    title: "Plan WhatsApp recovery",
    description: "Choose the least-destructive supported recovery route. Never accepts message bodies or credentials.",
    inputSchema: {
      platform: z.enum(["android", "iphone", "web"]),
      availableSource: z.enum(["old_device", "backup", "export", "none"]),
      authorized: z.boolean().describe("True only when the user owns the data or has explicit authorization."),
      workingCopy: z.boolean().describe("Whether inspection will use a preserved working copy."),
    },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    _meta: { "openai/outputTemplate": WIDGET_URI, "openai/toolInvocation/invoking": "Planning recovery…", "openai/toolInvocation/invoked": "Recovery plan ready" },
  }, async (input) => result("Recovery plan", planRecovery(input)));

  server.registerTool("review_whatsapp_audit", {
    title: "Review WhatsApp audit",
    description: "Summarize JSON produced by the bundled local metadata-only artifact auditor. Do not paste message bodies.",
    inputSchema: { audit: z.record(z.string(), z.unknown()) },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    _meta: { "openai/outputTemplate": WIDGET_URI, "openai/toolInvocation/invoking": "Reviewing audit…", "openai/toolInvocation/invoked": "Audit reviewed" },
  }, async ({ audit }) => result("Audit review", reviewAudit(audit)));
  return server;
}

const app = express();
app.use(express.json({ limit: "1mb" }));
app.get("/health", (_req, res) => res.json({ ok: true }));
app.post("/mcp", async (req, res) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on("close", () => { transport.close(); server.close(); });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

const port = Number(process.env.PORT ?? 8787);
app.listen(port, "0.0.0.0", () => console.log(`WhatsApp Recovery MCP app listening on :${port}/mcp`));
