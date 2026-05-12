import type { TaskNode } from '@/lib/types/protocol';

/** True iff `candidate` is a transitive dependency of `descendant`. False when equal. */
export function isAncestor(taskMap: Map<string, TaskNode>, descendant: string, candidate: string): boolean {
  if (candidate === descendant) return false;
  const seen = new Set<string>();
  const stack: string[] = [descendant];
  while (stack.length) {
    const name = stack.pop()!;
    for (const dep of taskMap.get(name)?.dependencies ?? []) {
      if (dep === candidate) return true;
      if (!seen.has(dep)) {
        seen.add(dep);
        stack.push(dep);
      }
    }
  }
  return false;
}
