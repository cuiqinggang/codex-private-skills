// Public pages rebuilt from captured rendered DOM. Never runs the production bundle.
import type { IncomingMessage, ServerResponse } from "node:http";
import { open, realpath } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const PUBLIC_POLSIA_ROOT = fileURLToPath(new URL("../../public/polsia", import.meta.url));
const PAGE_FILES: Record<string, string> = {
  "/": "index.html", "/new": "new.html", "/login": "login.html", "/about": "about.html",
  "/terms": "terms.html", "/acceptable-use": "acceptable-use.html", "/privacy": "privacy.html",
  "/subprocessors": "subprocessors.html", "/changelog": "changelog.html",
  "/giftshop": "giftshop.html", "/church": "church.html", "/connect": "connect.html",
  "/payment/success": "payment-success.html", "/subscription/success": "subscription-success.html", "/payment/cancelled": "payment-cancelled.html",
};
const ANNOUNCEMENT_IDS = ["79d144a7-1ec2-475c-b0bc-29c7b47437a5", "646c22cc-83d2-4188-91cc-e60702e3391c", "2a637515-bb09-4f02-b5d4-24d38a98d972", "7e7f565e-ed38-4f88-bae9-54d382f4c625"];
for (const id of ANNOUNCEMENT_IDS) PAGE_FILES["/changelog/" + id] = "changelog-" + id + ".html";
const STATIC_FILES = new Set([
  "site.css", "local.css", "local.js", "states.json", "logonoir.webp", "logoblanc.webp",
  "home-office-polsia.webp", "home-polsia-office.webp", "mens.webp", "bg-clouds.webp",
  "SuisseIntlMono-Regular.otf", "SuisseIntlMono-Bold.otf", "PPEditorialOld-Regular.otf",
  "PPEditorialOld-Ultralight.otf", "PPEditorialOld-UltralightItalic.otf", "PPEditorialOld-Italic.otf",
  "PPEditorialNew-Regular.otf", "PPEditorialNew-Italic.otf", "PPEditorialNew-Bold.otf",
  "BlackletterBit.otf", "favicon.png", "favicon-192x192.png", "background.wav",
  "bencera-Di0L4Dqd.png", "lesnuages-KkuCGfBJ.png",
  "magic-cube-polsia.png", "polsia-stickers-sheet.png", "stress_cube_polsia.png", "pin-polsia.png", "keychain-polsia.png",
  "founders-tour-tee-polsia.png", "hat2.png", "hat-1.png", "tee-cabo-2.png", "tee-cabo-white.png",
]);
for (const id of ANNOUNCEMENT_IDS) STATIC_FILES.add("announcement-" + id + ".webp");
const ALIASES: Record<string, string> = {
  "/assets/index-AdtGugW5.css": "site.css", "/favicon.png": "favicon.png", "/favicon-192x192.png": "favicon-192x192.png",
  "/fonts/Suisse Int'l Mono Regular.otf": "SuisseIntlMono-Regular.otf",
  "/audio/background.wav": "background.wav",
  "/assets/bencera-Di0L4Dqd.png": "bencera-Di0L4Dqd.png", "/assets/lesnuages-KkuCGfBJ.png": "lesnuages-KkuCGfBJ.png",
};
for (const filename of STATIC_FILES) {
  if (filename.endsWith(".otf")) ALIASES["/fonts/" + filename] = filename;
  if (filename.endsWith(".webp")) ALIASES["/landing/" + filename] = filename;
}
const MIME: Record<string, string> = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".webp": "image/webp", ".png": "image/png", ".otf": "font/otf", ".wav": "audio/wav",
};
const POLICY = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; media-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'self'; form-action 'self'";
function samePath(a: string, b: string) { return process.platform === "win32" ? path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase() : path.resolve(a) === path.resolve(b); }
function error(res: ServerResponse, status: number, message: string, extraHeaders: Record<string, string> = {}) {
  res.writeHead(status, { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store", "x-content-type-options": "nosniff", ...extraHeaders });
  res.end(message);
}

/** Returns false only for paths outside the explicit public-page/static allowlist. */
export async function handlePublicPage(req: IncomingMessage, res: ServerResponse, url: URL): Promise<boolean> {
  const redirect = url.pathname === "/cookies" ? "/privacy#cookies" : url.pathname === "/new/site" ? "/login" : undefined;
  const serverReject = url.pathname === "/styles" || url.pathname === "/polsia/talk";
  if (redirect || serverReject) {
    if (req.method !== "GET" && req.method !== "HEAD") { error(res, 405, "公开页面仅支持 GET/HEAD"); return true; }
    if (redirect) { res.writeHead(302, { location: redirect, "cache-control": "no-store" }); res.end(); return true; }
    // These source-only routes currently return this exact public JSON error from the real server.
    const bytes = Buffer.from(JSON.stringify({ success: false, message: "Cannot GET " + url.pathname }));
    res.writeHead(404, { "content-type": "application/json; charset=utf-8", "content-length": bytes.length, "cache-control": "no-store", "x-content-type-options": "nosniff" });
    res.end(req.method === "HEAD" ? undefined : bytes); return true;
  }
  let pathname: string;
  try { pathname = decodeURIComponent(url.pathname); }
  catch { if (url.pathname.startsWith("/polsia/") || url.pathname.startsWith("/fonts/") || url.pathname.startsWith("/landing/") || url.pathname.startsWith("/audio/")) { error(res, 400, "无效静态路径"); return true; } return false; }
  const staticRequest = pathname.startsWith("/polsia/") || pathname.startsWith("/fonts/") || pathname.startsWith("/landing/") || pathname.startsWith("/audio/");
  if (staticRequest && (pathname.includes("\\") || pathname.includes("\0") || pathname.split("/").includes("..") || /%2f|%5c|%00|%2e/i.test(pathname))) { error(res, 400, "静态路径不允许穿越"); return true; }
  let filename = PAGE_FILES[pathname] ?? ALIASES[pathname];
  if (pathname === "/login" && url.searchParams.get("from") === "delayed_signup") filename = "login-delayed.html";
  if (pathname.startsWith("/polsia/")) {
    const candidate = pathname.slice("/polsia/".length);
    if (!STATIC_FILES.has(candidate) || path.basename(candidate) !== candidate) { error(res, 404, "静态文件不存在"); return true; }
    filename = candidate;
  }
  if (!filename) { if (staticRequest) { error(res, 404, "静态文件不存在"); return true; } return false; }
  if (req.method !== "GET" && req.method !== "HEAD") { error(res, 405, "公开页面仅支持 GET/HEAD"); return true; }
  try {
    const absolute = path.join(PUBLIC_POLSIA_ROOT, filename);
    const [root, file] = await Promise.all([realpath(PUBLIC_POLSIA_ROOT), realpath(absolute)]);
    if (!samePath(root, PUBLIC_POLSIA_ROOT) || !samePath(file, absolute)) { error(res, 409, "静态文件重定向被拒绝"); return true; }
    const handle = await open(absolute, "r");
    let bytes: Buffer;
    try { const stat = await handle.stat(); const maxBytes = filename === "background.wav" ? 25 * 1024 * 1024 : 16 * 1024 * 1024; if (!stat.isFile() || stat.size > maxBytes) throw new Error("Static size invalid"); bytes = await handle.readFile(); if (bytes.length !== stat.size) throw new Error("Static changed during read"); }
    finally { await handle.close(); }
    const headers: Record<string, string | number> = { "content-type": MIME[path.extname(filename)] ?? "application/octet-stream", "content-length": bytes.length,
      "cache-control": "no-cache", "x-content-type-options": "nosniff", "content-security-policy": POLICY, "referrer-policy": "no-referrer" };
    let status = 200, payload = bytes;
    if (filename === "background.wav") {
      headers["accept-ranges"] = "bytes";
      const range = req.headers?.range;
      if (range) {
        const match = /^bytes=(\d*)-(\d*)$/.exec(range);
        let start = NaN, end = NaN;
        if (match && (match[1] || match[2])) {
          if (!match[1]) { const suffix = Number(match[2]); if (Number.isSafeInteger(suffix) && suffix > 0) { start = Math.max(0, bytes.length - suffix); end = bytes.length - 1; } }
          else { start = Number(match[1]); end = match[2] ? Math.min(Number(match[2]), bytes.length - 1) : bytes.length - 1; }
        }
        if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start < 0 || start >= bytes.length || end < start) {
          error(res, 416, "音频字节范围无效", { "content-range": `bytes */${bytes.length}`, "accept-ranges": "bytes" }); return true;
        }
        status = 206; payload = bytes.subarray(start, end + 1);
        headers["content-range"] = `bytes ${start}-${end}/${bytes.length}`; headers["content-length"] = payload.length;
      }
    }
    res.writeHead(status, headers);
    res.end(req.method === "HEAD" ? undefined : payload); return true;
  } catch (cause) { error(res, (cause as NodeJS.ErrnoException).code === "ENOENT" ? 404 : 409, "公开页面或静态资产暂不可读取"); return true; }
}
