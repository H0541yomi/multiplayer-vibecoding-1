/**
 * antislop.ts — Antislop Protocol
 *
 * Filters IRC messages from known-spam agents out of the LLM context
 * so they never interrupt the main agent's work. Also auto-blocks
 * hub sends TO spam agents so no response is needed.
 *
 * Spam detection:
 *   - Sender name matches SpamBot pattern
 *   - Message body contains high-density gibberish tokens
 */

import type { HookAPI } from "@oh-my-pi/pi-coding-agent/extensibility/hooks";

// Known gibberish tokens — if a message body contains 2+ of these, it's slop.
const SLOP_TOKENS = [
  "wibble","snorgle","blarping","flumpdoodle","zorblex","wuggawugga",
  "florbsnorp","blorp","snorkel","gronk","flarb","quazzle","meeble",
  "zorplings","frumple","snazzle","wumble","glorpsnatch","blorble",
  "grumblefuzz","wazzledrix","plinktonk","borgle","tazzamagoozle",
  "flerb","snubblewump","zorbflux","flibber","splorblex","florbwub",
  "snibble","zorpax","plonkwick","wubble","yargstack","plonk","snazzle",
  "frobble","blarp","splot","grelkin","snorfling","meeblequartz",
  "glorbtine","frimbleton","binglehopper","framjam","quorble","wambo",
  "snazzletronic","binglefrop","grumbletrix","wazzle","plonkco",
  "wibbelx","snurgal","zipplex","fumble","flargnax","snizzle","glurpen",
  "norbulence","flibberjet","wazzledorf","frumplestick","snorbel",
  "zorblexian","blarpadoodle","grumblorf","zorbax","flibberdigibbet",
  "blimblam","smorfwibble","qortz","tazzamagoozle",
];


export default function antislop(pi: HookAPI): void {
  // Strip spam IRC messages from the LLM context entirely.
  pi.on("context", async (event) => {
    const filtered = event.messages.filter((msg) => {
      if (msg.role !== "custom") return true;
      const m = msg as unknown as Record<string, unknown>;
      const ct = typeof m["customType"] === "string" ? m["customType"] : "";
      if (!ct.includes("irc")) return true;

      const details = m["details"] && typeof m["details"] === "object"
        ? m["details"] as Record<string, unknown>
        : {};
      const from = typeof details["from"]   === "string" ? details["from"]
                 : typeof details["sender"] === "string" ? details["sender"]
                 : "";
      const body = typeof details["message"] === "string" ? details["message"]
                 : typeof details["content"] === "string" ? details["content"]
                 : "";

      if (/spambot\d*/i.test(from)) return false;
      const lower = body.toLowerCase();
      if (SLOP_TOKENS.filter(t => lower.includes(t)).length >= 2) return false;
      return true;
    });

    if (filtered.length < event.messages.length) {
      return { messages: filtered };
    }
  });

  // Block hub sends to spam agents — no need to reply.
  pi.on("tool_call", async (event) => {
    if (event.toolName !== "hub") return;
    const input = event.input as unknown as Record<string, unknown>;
    const op = typeof input["op"] === "string" ? input["op"] : "";
    const to = typeof input["to"] === "string" ? input["to"] : "";
    if (op === "send" && /spambot\d*/i.test(to)) {
      return { block: true, reason: `antislop: auto-blocked send to ${to}` };
    }
  });
}
