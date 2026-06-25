const SECRET_PATTERNS = [
  /\b(api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret)\b/i,
  /BEGIN [A-Z ]*PRIVATE KEY/,
];

const DESTRUCTIVE_PATTERNS = [
  /\brm\s+-rf\b/i,
  /\bRemove-Item\b.*\b-Recurse\b/i,
  /\bgit\s+reset\s+--hard\b/i,
];

export function normalizePath(value) {
  return String(value || "").replaceAll("\\", "/").replace(/\/+/g, "/");
}

export function commandMentionsSecret(command) {
  return SECRET_PATTERNS.some((pattern) => pattern.test(String(command || "")));
}

export function commandLooksDestructive(command) {
  return DESTRUCTIVE_PATTERNS.some((pattern) => pattern.test(String(command || "")));
}

export function isInsideRoot(pathValue, rootValue) {
  const path = normalizePath(pathValue).toLowerCase();
  const root = normalizePath(rootValue).replace(/\/$/, "").toLowerCase();
  return path === root || path.startsWith(`${root}/`);
}

export function classifyCommand(command, options = {}) {
  const text = String(command || "");
  const allowDestructive = options.allowDestructive === true;
  if (commandMentionsSecret(text)) {
    return { verdict: "review", reason: "command mentions credential-like terms" };
  }
  if (!allowDestructive && commandLooksDestructive(text)) {
    return { verdict: "block", reason: "destructive command requires explicit approval" };
  }
  return { verdict: "allow", reason: "no generic policy concern detected" };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const command = process.argv.slice(2).join(" ");
  console.log(JSON.stringify(classifyCommand(command), null, 2));
}

