export function classifyIntent(message: string) {
  const normalized = message.toLowerCase();
  if (normalized.includes("eksport")) return "why_blocked";
  if (normalized.includes("kilde")) return "source_help";
  if (normalized.includes("hva")) return "what_next";
  return "unknown";
}

export function topicFingerprint(intent: string, objectType = "case") {
  return `${objectType}.${intent}`;
}
