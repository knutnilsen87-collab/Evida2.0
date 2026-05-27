import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const appRoot = join(root, "apps", "web", "app");
const requiredRoutes = [
  "page.tsx",
  "cases/page.tsx",
  "cases/new/page.tsx",
  "cases/[caseId]/page.tsx",
  "cases/[caseId]/documents/page.tsx",
  "cases/[caseId]/facts/page.tsx",
  "cases/[caseId]/drafts/page.tsx",
  "cases/[caseId]/drafts/[draftId]/page.tsx",
  "cases/[caseId]/export-preview/page.tsx",
  "cases/[caseId]/audit/page.tsx",
  "settings/page.tsx"
];

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const path = join(dir, entry);
    const stat = statSync(path);
    if (stat.isDirectory()) out.push(...walk(path));
    if (stat.isFile() && /\.(tsx|ts)$/.test(entry)) out.push(path);
  }
  return out;
}

for (const route of requiredRoutes) {
  const path = join(appRoot, route);
  if (!existsSync(path)) {
    throw new Error(`Missing required route: ${route}`);
  }
}

for (const file of walk(appRoot)) {
  const text = readFileSync(file, "utf8");
  if (!text.includes("export default") && file.endsWith("page.tsx")) {
    throw new Error(`Page has no default export: ${file}`);
  }
  for (const match of text.matchAll(/from\s+"(\.{1,2}\/[^"]+)"/g)) {
    const base = resolve(dirname(file), match[1]);
    const candidates = [`${base}.ts`, `${base}.tsx`, join(base, "index.ts"), join(base, "index.tsx")];
    if (!candidates.some(existsSync)) {
      throw new Error(`Broken relative import in ${file}: ${match[1]}`);
    }
  }
}

console.log("Web smoke build passed");
