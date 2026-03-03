import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const BASE_URL = process.env.WAI_API_BASE_URL || "https://mgifford.github.io/wai-yaml-ld/api/v1";

const server = new Server(
  {
    name: "wai-static-api",
    version: "1.0.0",
  },
  {
    capabilities: { tools: {} },
  },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_wcag_criterion",
      description: "Fetch a WCAG success criterion by ref_id (e.g. 1.1.1)",
      inputSchema: {
        type: "object",
        properties: {
          ref_id: {
            type: "string",
            description: "WCAG success criterion ID such as 1.1.1",
          },
        },
        required: ["ref_id"],
      },
    },
    {
      name: "get_wai_schema",
      description: "Fetch GraphQL introspection JSON for the static WAI API",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_wcag_criterion") {
    const refId = String(request.params.arguments?.ref_id || "").trim();
    if (!refId) {
      return {
        content: [{ type: "text", text: "Missing required argument: ref_id" }],
      };
    }
    const slug = refId.replace(/\./g, "-");
    const response = await fetch(`${BASE_URL}/sc/${slug}.json`);
    if (!response.ok) {
      return {
        content: [{ type: "text", text: `Failed to fetch criterion ${refId}: HTTP ${response.status}` }],
      };
    }
    const payload = await response.json();
    return {
      content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    };
  }

  if (request.params.name === "get_wai_schema") {
    const response = await fetch(`${BASE_URL}/introspection.json`);
    if (!response.ok) {
      return {
        content: [{ type: "text", text: `Failed to fetch introspection: HTTP ${response.status}` }],
      };
    }
    const payload = await response.json();
    return {
      content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    };
  }

  return {
    content: [{ type: "text", text: `Unknown tool: ${request.params.name}` }],
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);