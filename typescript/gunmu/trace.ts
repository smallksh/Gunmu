/**
 * 追踪所有 Nothing 的产生位置。
 * 默认关闭，零开销。
 */

interface TraceState {
  enabled: boolean;
  records: Array<{ reason: string; origin: string }>;
}

const state: TraceState = {
  enabled: false,
  records: [],
};

export function enable(): void {
  state.enabled = true;
}

export function disable(): void {
  state.enabled = false;
}

export function clear(): void {
  state.records = [];
}

export function recordNothing(reason: string, origin: string): void {
  if (!state.enabled) {
    return;
  }
  state.records.push({ reason, origin });
}

export function records(): ReadonlyArray<{ reason: string; origin: string }> {
  return [...state.records];
}

export function summary(): {
  total: number;
  byReason: Record<string, number>;
  records: ReadonlyArray<{ reason: string; origin: string }>;
} {
  const byReason: Record<string, number> = {};
  for (const r of state.records) {
    byReason[r.reason] = (byReason[r.reason] ?? 0) + 1;
  }
  return {
    total: state.records.length,
    byReason,
    records: [...state.records],
  };
}

export function report(): string {
  const s = summary();
  if (s.total === 0) {
    return "没有滚木。";
  }
  const lines: string[] = [`共 ${s.total} 个滚木：`];
  for (const [reason, count] of Object.entries(s.byReason)) {
    lines.push(`  [${count}] ${reason}`);
  }
  lines.push("");
  lines.push("产生位置：");
  for (const r of s.records) {
    lines.push(`  ${r.origin}  ->  ${r.reason}`);
  }
  return lines.join("\n");
}