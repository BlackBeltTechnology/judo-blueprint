// session-steer.mts <session-id-prefix> <text | @file>
// Sends a message to a running pi session with delivery "steer" (mid-turn, after the current step). Never followUp:
// commands to a session always go as steer. Reuses pi-dashboard's bus client and local-proof helper next to
// DASHBOARD_BUS (pi-dashboard's .pi/skills/pi-dashboard/scripts/dashboard-bus.ts).
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";

const bus = process.env.DASHBOARD_BUS;
if (!bus) { console.error("set DASHBOARD_BUS to pi-dashboard's dashboard-bus.ts"); process.exit(1); }
const [prefix, ...words] = process.argv.slice(2);
let text = words.join(" ");
if (text.startsWith("@")) text = readFileSync(text.slice(1), "utf8");
if (!prefix || !text.trim()) { console.error("usage: session-steer.mts <id-prefix> <text | @file>"); process.exit(1); }

const dir = dirname(bus);
const { BusClient } = await import(pathToFileURL(createRequire(bus).resolve("@blackbelt-technology/pi-dashboard-bus-client")).href);
const { dialHost, proofHeaders } = await import(pathToFileURL(join(dir, "local-proof.ts")).href);
const client = new BusClient({ host: dialHost(), proofHeaders });
await client.connect();
const s = client.read.sessions().find((x: { id: string }) => x.id.startsWith(prefix));
if (!s) { console.error(`no session id starts with "${prefix}"`); process.exit(1); }
client.prompt(s.id, text, { delivery: "steer" });
await new Promise((r) => setTimeout(r, 500));
console.log(`steered ${s.id.slice(0, 8)}`);
process.exit(0);
