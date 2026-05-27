export function factSourceStatus(sourceRefIds: string[]) {
  return sourceRefIds.length > 0 ? "documented" : "missing_source";
}

export function canExportSection(sourceRefIds: string[]) {
  return sourceRefIds.length > 0;
}
