import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const forbidden = [
  "export_gate_blocked",
  "ocr_low_confidence",
  "job_id",
  "confidence threshold",
];

function files(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const path = join(dir, entry);
    const stat = statSync(path);
    if (stat.isDirectory() && !["node_modules", ".next"].includes(entry)) out.push(...files(path));
    if (stat.isFile() && /\.(tsx|ts|jsx|js)$/.test(entry)) out.push(path);
  }
  return out;
}

let failed = false;
for (const file of files(join(root, "apps", "web"))) {
  const text = readFileSync(file, "utf8");
  for (const word of forbidden) {
    if (text.includes(word)) {
      console.error(`Forbidden technical copy "${word}" in ${file}`);
      failed = true;
    }
  }
}

if (failed) process.exit(1);
console.log("UI copy check passed");
