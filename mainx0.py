#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import tempfile
import platform

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

# Cross-platform temp directory
_CUSTOM_TEMP = os.path.join(tempfile.gettempdir(), "ptemp")
try:
    os.makedirs(_CUSTOM_TEMP, exist_ok=True)
    os.environ["TEMP"] = _CUSTOM_TEMP
    os.environ["TMP"] = _CUSTOM_TEMP
    os.environ["TMPDIR"] = _CUSTOM_TEMP
    print(f"📁 TEMP: {_CUSTOM_TEMP}")
except Exception as e:
    print(f"⚠️ TEMP: {e}")

import asyncio
import random
import subprocess
import importlib


def ensure(pkg, import_name=None):
    name = import_name or pkg
    try:
        importlib.import_module(name)
    except ImportError:
        print(f"📦 Installing {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])


ensure("playwright")
ensure("playwright-stealth", "playwright_stealth")
ensure("psutil")

if os.name == "nt":
    os.system("")

import psutil
from playwright.async_api import async_playwright

try:
    from playwright_stealth import stealth_async
except ImportError:
    async def stealth_async(page):
        pass


def detect_os():
    return platform.system() or "Unknown"


def is_linux():
    return sys.platform.startswith("linux")


def ensure_msedge():
    """Install msedge binary + OS dependencies (Linux-only for install-deps)."""
    print(f"🌐 OS: {detect_os()} — ensuring Edge is installed...")

    # 1. OS-level dependencies (Linux only — Windows/macOS don't need this)
    if is_linux():
        try:
            print("   → installing system dependencies...")
            r = subprocess.run(
                [sys.executable, "-m", "playwright", "install-deps", "msedge"],
                capture_output=True, text=True, timeout=900,
                encoding="utf-8", errors="ignore",
            )
            if r.returncode == 0:
                print("   ✅ OS dependencies ready")
            else:
                print(f"   ⚠️ install-deps exit {r.returncode}")
                if r.stderr:
                    print(f"   {r.stderr[:300]}")
        except Exception as e:
            print(f"   ⚠️ install-deps: {type(e).__name__}: {e}")

    # 2. msedge binary (all OS)
    try:
        print("   → installing msedge binary...")
        r = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "msedge"],
            capture_output=True, text=True, timeout=900,
            encoding="utf-8", errors="ignore",
        )
        if r.returncode == 0:
            print("   ✅ msedge ready")
        else:
            print(f"   ⚠️ msedge install exit {r.returncode}")
            if r.stderr:
                print(f"   {r.stderr[:300]}")
    except Exception as e:
        print(f"   ⚠️ msedge install: {type(e).__name__}: {e}")


def boost_python_process():
    try:
        p = psutil.Process(os.getpid())
        if os.name == "nt":
            p.nice(psutil.HIGH_PRIORITY_CLASS)
        else:
            try:
                p.nice(-10)
            except Exception:
                p.nice(10)
        print("⚡ Python priority: HIGH")
    except Exception as e:
        print(f"⚠️ priority: {e}")


# ================= HARDCODED CONFIG =================
HARDCODED_SESSION_ID = '74242372744%3AicqhiwNI0bXE6h%3A14%3AAYnXC0by-o8hYZUIqNAA2SLw_4uN5uHjTU8m_iIpHg'
HARDCODED_PREFIX     = 'Hy'
HARDCODED_GC_NAME    = 'Hy'
HARDCODED_GC_LINK    = 'https://www.instagram.com/direct/t/1594907375294880/'
# ====================================================

TARGET_CYCLE_SEC = 0.15

REFRESH_AFTER_MIN = 80
REFRESH_AFTER_MAX = 100
INPUT_REFRESH_EVERY = 20

REDIRECT_CHECK_EVERY = 50
REDIRECT_WATCH_INTERVAL = 60

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
)

EMOJI_LIST_1 = ["🧊", "❄️", "💠", "🍀", "🪷️", "🪼", "🦠", "🧃", "🍷", "🥂"]

MSG_LINES = 3
NL_BETWEEN = "\n" * 40
NL_END = "\n" * 4
HARDCODED_MIDDLE = "Tmkc !!"

DEFAULT_PREFIX = "Hater"

INPUT_SELECTORS = [
    'div[contenteditable="true"][role="textbox"]',
    'div[contenteditable="true"][aria-label="Message"]',
    'textarea[placeholder="Message..."]',
    'div[aria-label*="Message"][contenteditable="true"]',
]

NOTIF_DISMISS_SELECTORS = [
    'button:has-text("Not Now")',
    'button:has-text("Abhi Nahi")',
    'button:has-text("Later")',
    'div[role="dialog"] [aria-label="Close"]',
    'svg[aria-label="Close"]',
]

NOTIF_ALLOW_SELECTORS = [
    'button:has-text("Allow")',
    'button:has-text("Anumati")',
]

GC_INFO_BTN   = '.x1i10hfl:nth-child(3) circle:nth-child(3)'
GC_CHANGE_BTN = 'div.xwhw2v2'
GC_NAME_INPUT = 'input.x11f1dot'
GC_SAVE_BTN   = 'div.xqui205:nth-child(3)'

SEL_SEND_BTN  = '.x9bdzbf > path'

PAGE_LOCK = None
LOGGED_OUT = False
BROWSER_LABEL = "msedge"


# ================= INIT SCRIPTS =================
STEALTH_SCRIPT = """
(() => {
    try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined, configurable: true }); } catch (e) {}
    try { Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'], configurable: true }); } catch (e) {}
    try { Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8, configurable: true }); } catch (e) {}
    try { Object.defineProperty(navigator, 'deviceMemory', { get: () => 8, configurable: true }); } catch (e) {}
    try { Object.defineProperty(navigator, 'platform', { get: () => 'Win32', configurable: true }); } catch (e) {}
    try {
        if (navigator.permissions && navigator.permissions.query) {
            const oq = navigator.permissions.query.bind(navigator.permissions);
            navigator.permissions.query = (p) => (p && p.name === 'notifications')
                ? Promise.resolve({ state: 'granted', onchange: null }) : oq(p);
        }
    } catch (e) {}
})();
"""

NOTIF_SUPPRESS_SCRIPT = """
(() => {
    const FN = function() { return {}; };
    FN.permission = 'granted';
    FN.requestPermission = () => Promise.resolve('granted');
    FN.prototype.close = function() {};
    FN.prototype.addEventListener = function() {};
    FN.prototype.removeEventListener = function() {};
    try { Object.defineProperty(window, 'Notification', { value: FN, writable: false, configurable: false }); } catch (e) {}
    try {
        if (navigator.serviceWorker && navigator.serviceWorker.register) {
            const o = navigator.serviceWorker.register.bind(navigator.serviceWorker);
            navigator.serviceWorker.register = function(...a) {
                return o(...a).then(r => { if (r && r.showNotification) r.showNotification = () => Promise.resolve(); return r; });
            };
        }
    } catch (e) {}
})();
"""

MSG_HIDE_SCRIPT = """
(() => {
    const style = document.createElement('style');
    style.textContent = `
        div[role="grid"],
        div[role="listbox"] {
            content-visibility: hidden !important;
            contain: strict !important;
        }
        div[role="grid"] > *,
        div[role="listbox"] > * {
            contain: strict !important;
        }
        [role="status"], [role="status"] *,
        [aria-live="polite"], [aria-live="polite"] *,
        [aria-live="assertive"], [aria-live="assertive"] * {
            visibility: hidden !important;
        }
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
            animation-duration: 0s !important;
            transition-duration: 0s !important;
            scroll-behavior: auto !important;
        }
    `;
    const attach = () => {
        try { (document.head || document.documentElement).appendChild(style); } catch(e) {}
    };
    if (document.head) attach();
    else document.addEventListener('DOMContentLoaded', attach);

    try {
        const OriginalWS = window.WebSocket;
        window.WebSocket = function(url, protocols) {
            const ws = new OriginalWS(url, protocols);
            try {
                ws.addEventListener('message', function(ev) {
                    ev.stopImmediatePropagation();
                }, true);
            } catch (e) {}
            return ws;
        };
        window.WebSocket.prototype = OriginalWS.prototype;
        window.WebSocket.CONNECTING = OriginalWS.CONNECTING;
        window.WebSocket.OPEN = OriginalWS.OPEN;
        window.WebSocket.CLOSING = OriginalWS.CLOSING;
        window.WebSocket.CLOSED = OriginalWS.CLOSED;
    } catch (e) {}

    const isMsgContainer = (el) => {
        if (!el || el.nodeType !== 1) return false;
        const role = el.getAttribute && el.getAttribute('role');
        return role === 'grid' || role === 'listbox';
    };

    const obs = new MutationObserver((mutations) => {
        for (const m of mutations) {
            for (const node of m.addedNodes) {
                if (node.nodeType !== 1) continue;
                try {
                    const parent = m.target;
                    if (parent && isMsgContainer(parent)) {
                        try { node.remove(); } catch (e) {}
                    }
                } catch (e) {}
            }
        }
    });

    const pruneContainer = (c) => {
        try {
            while (c.children.length > 0) {
                try { c.removeChild(c.firstElementChild); } catch(e) { break; }
            }
        } catch (e) {}
    };

    const clearCaches = async () => {
        try {
            if (window.caches) {
                const keys = await caches.keys();
                for (const k of keys) {
                    try { await caches.delete(k); } catch (e) {}
                }
            }
        } catch (e) {}
    };

    const periodic = () => {
        try {
            const cs = document.querySelectorAll('div[role="grid"], div[role="listbox"]');
            for (const c of cs) pruneContainer(c);
        } catch (e) {}
        try { performance.clearResourceTimings(); } catch (e) {}
        clearCaches();
    };

    setInterval(periodic, 500);

    setInterval(() => {
        try {
            const cs = document.querySelectorAll('div[role="grid"], div[role="listbox"]');
            for (const c of cs) {
                while (c.children.length > 0) {
                    try { c.removeChild(c.firstElementChild); } catch(e) { break; }
                }
            }
        } catch (e) {}
    }, 100);

    const start = () => {
        try {
            obs.observe(document.body, { childList: true, subtree: true });
            periodic();
        } catch (e) {}
    };
    if (document.body) start();
    else document.addEventListener('DOMContentLoaded', start);
})();
"""

PRELOAD_KILL_SCRIPT = """
(() => {
    try {
        const kill = () => {
            document.querySelectorAll('link[rel="preload"], link[rel="prefetch"], link[rel="preconnect"], link[rel="dns-prefetch"]')
                .forEach(l => { try { l.parentNode.removeChild(l); } catch(e) {} });
        };
        kill();
        document.addEventListener('DOMContentLoaded', kill);
        setTimeout(kill, 1000);
        setTimeout(kill, 3000);
    } catch (e) {}
})();
"""


# ================= STATE =================
stats = {
    "sent": 0,
    "failed": 0,
    "start": time.time(),
    "refreshes": 0,
    "since_refresh": 0,
    "refresh_target": 0,
    "input_refreshes": 0,
    "renames": 0,
    "click_sends": 0,
    "enter_sends": 0,
    "redirects": 0,
}

PREFIX = DEFAULT_PREFIX
TARGET_URL = "?"
NEW_GC_NAME = ""


def ts():
    return time.strftime("%H:%M:%S")


def build_message():
    e1 = random.choice(EMOJI_LIST_1)
    num = random.randint(1, 10**10)
    line = f"{PREFIX} {HARDCODED_MIDDLE} {e1} !!"
    body = NL_BETWEEN.join([line] * MSG_LINES)
    return f"{body}{NL_END}{num}"


# ================= POPUP / INPUT =================
async def _try_click_any(page, selectors, timeout_ms=800):
    for sel in selectors:
        try:
            el = await page.wait_for_selector(sel, timeout=timeout_ms)
            if el and await el.is_visible():
                try:
                    await el.click(timeout=1500)
                except Exception:
                    try:
                        await el.click(force=True, timeout=1500)
                    except Exception:
                        continue
                return True
        except Exception:
            continue
    return False


async def dismiss_notif_popup(page, max_rounds=3):
    for _ in range(max_rounds):
        clicked = await _try_click_any(page, NOTIF_DISMISS_SELECTORS, timeout_ms=1000)
        if not clicked:
            clicked = await _try_click_any(page, NOTIF_ALLOW_SELECTORS, timeout_ms=700)
        if clicked:
            await page.wait_for_timeout(random.randint(200, 500))
        else:
            break


async def find_input(page, timeout_ms=10000):
    for sel in INPUT_SELECTORS:
        try:
            loc = page.locator(sel)
            await loc.wait_for(state="visible", timeout=timeout_ms)
            return loc
        except Exception:
            continue
    return None


async def dump_page_debug(page, label="input_not_found"):
    """Save diagnostics when input isn't found — helps us see what page we're on."""
    print(f"\n🐛 DEBUG ({label}):")
    try:
        url = page.url
    except Exception:
        url = "?"
    print(f"   URL   : {url}")

    try:
        title = await page.title()
    except Exception:
        title = "?"
    print(f"   Title : {title}")

    try:
        body_text = await page.evaluate(
            "() => document.body ? document.body.innerText.substring(0, 300) : 'no body'"
        )
        body_text = str(body_text).replace("\n", " ")[:300]
        print(f"   Body  : {body_text}")
    except Exception as e:
        print(f"   Body  : <eval failed: {type(e).__name__}>")

    try:
        fname = f"./debug_{label}_{int(time.time())}.png"
        await page.screenshot(path=fname, full_page=False)
        print(f"   Screenshot saved: {fname}")
    except Exception as e:
        print(f"   Screenshot failed: {type(e).__name__}: {e}")

    print()


# ================= PROMPT =================
async def prompt_async(text):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, text)


# ================= CHROMIUM ARGS (platform-aware) =================
def get_chromium_args():
    """Platform-aware browser args. Removes --single-process on Windows/macOS
    (it breaks SPA rendering), keeps sandbox workarounds on Linux only."""
    args = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--mute-audio",
        "--disable-extensions",
        "--disable-default-apps",
        "--disable-sync",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-domain-reliability",
        "--disable-client-side-phishing-detection",
        "--disable-hang-monitor",
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-logging",
        "--log-level=3",
        "--metrics-recording-only",
        "--enable-features=NetworkService",
        "--disable-features=Translate,BackForwardCache,AcceptCHFrame,MediaRouter,OptimizationHints,CalculateNativeWinOcclusion",
        "--disk-cache-size=1",
        "--disable-application-cache",
    ]
    if is_linux():
        # Linux CI containers sometimes need this
        args.insert(0, "--disable-setuid-sandbox")
    return args


async def attach_scripts(page):
    await page.add_init_script(STEALTH_SCRIPT)
    await page.add_init_script(NOTIF_SUPPRESS_SCRIPT)
    await page.add_init_script(MSG_HIDE_SCRIPT)
    await page.add_init_script(PRELOAD_KILL_SCRIPT)
    try:
        await stealth_async(page)
    except Exception:
        pass


# ================= LAUNCH =================
async def launch_browser(pw, session_id):
    browser = await pw.chromium.launch(
        channel="msedge",
        headless=True,
        args=get_chromium_args(),
    )
    context = await browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="Asia/Kolkata",
        reduced_motion="reduce",
    )

    try:
        await context.add_cookies([{
            "name": "sessionid",
            "value": session_id,
            "domain": ".instagram.com",
            "path": "/",
            "secure": True,
            "httpOnly": True,
            "sameSite": "None",
        }])
    except Exception:
        try:
            await context.add_cookies([{
                "name": "sessionid",
                "value": session_id,
                "domain": ".instagram.com",
                "path": "/",
                "secure": True,
            }])
        except Exception as e:
            print(f"⚠️ cookie inject: {type(e).__name__}: {e}")

    try:
        await context.grant_permissions(
            ["notifications"], origin="https://www.instagram.com")
    except Exception:
        pass

    return browser, context


async def _cleanup_browser(browser, context):
    if context:
        try: await context.close()
        except Exception: pass
    if browser:
        try: await browser.close()
        except Exception: pass


# ================= RENAME GC =================
async def rename_group(page):
    if not NEW_GC_NAME:
        return False

    try:
        await page.wait_for_selector(GC_INFO_BTN, timeout=4000, state="visible")
        await page.click(GC_INFO_BTN, timeout=3000)
        await page.wait_for_timeout(700)
        await page.wait_for_selector(GC_CHANGE_BTN, timeout=4000, state="visible")
        await page.click(GC_CHANGE_BTN, timeout=3000)
        await page.wait_for_timeout(500)
        inp = await page.wait_for_selector(GC_NAME_INPUT, timeout=4000, state="visible")
        try: await inp.fill("")
        except Exception: pass
        await inp.type(NEW_GC_NAME, delay=15)
        await page.wait_for_timeout(300)
        await page.click(GC_SAVE_BTN, timeout=3000)
        await page.wait_for_timeout(500)
        stats["renames"] += 1
        return True
    except Exception as e:
        print(f"⚠️ rename: {type(e).__name__}")
        return False


# ================= SMOOTH SEND =================
async def put_text_and_send(page, input_el, msg):
    if input_el is None:
        return False, "fail"

    try:
        await input_el.click(timeout=200)
    except Exception:
        return False, "fail"

    try:
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
    except Exception:
        pass

    filled = False
    try:
        await page.keyboard.insert_text(msg)
        filled = True
    except Exception:
        pass

    if not filled:
        try:
            ok = await input_el.evaluate(
                """(el, text) => {
                    try {
                        el.focus();
                        const lines = text.split('\\n');
                        for (let i = 0; i < lines.length; i++) {
                            if (i > 0) document.execCommand('insertLineBreak', false, null);
                            if (lines[i]) document.execCommand('insertText', false, lines[i]);
                        }
                        return true;
                    } catch (e) { return false; }
                }""",
                msg,
            )
            if ok: filled = True
        except Exception:
            pass

    if not filled:
        return False, "fail"

    btn = page.locator(SEL_SEND_BTN)
    try:
        if await btn.is_visible(timeout=50):
            try:
                await btn.click(timeout=300)
                return True, "click"
            except Exception:
                pass
    except Exception:
        pass

    try:
        await page.keyboard.press("Enter")
        return True, "enter"
    except Exception:
        return False, "fail"


# ================= REDIRECT HANDLER =================
async def handle_redirect(page, source="send"):
    global LOGGED_OUT

    async with PAGE_LOCK:
        try:
            if page.is_closed(): return
            try: cur = page.url
            except Exception: return

            if "/accounts/login" in cur:
                LOGGED_OUT = True
                print(f"\n🚨 {source}: Login page detected. LOGGED OUT.")
                return

            if "direct/t/" in cur:
                return

            print(f"🔀 {source}: off GC → redirecting")
            try:
                await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
            except Exception:
                pass

            await asyncio.sleep(1.0)

            if page.is_closed(): return

            try: cur = page.url
            except Exception: cur = ""

            if "direct/t/" in cur:
                stats["redirects"] += 1
                try: await dismiss_notif_popup(page, max_rounds=1)
                except Exception: pass
            elif "/accounts/login" in cur:
                LOGGED_OUT = True
                print(f"\n🚨 {source}: Logged out after redirect.")
        except Exception:
            pass


# ================= GC MONITOR =================
async def gc_monitor(page):
    global LOGGED_OUT

    while True:
        try:
            await asyncio.sleep(REDIRECT_WATCH_INTERVAL)

            if LOGGED_OUT: return
            if not TARGET_URL or TARGET_URL == "?": continue

            try:
                if page.is_closed(): return
                cur = page.url
            except Exception:
                return

            if "/accounts/login" in cur:
                LOGGED_OUT = True
                print("\n🚨 MONITOR: Logged out (login page).")
                return

            if "direct/t/" in cur:
                continue

            await handle_redirect(page, source="monitor")

        except asyncio.CancelledError:
            return
        except Exception:
            pass


# ================= SEND LOOP =================
async def send_loop(page):
    global LOGGED_OUT

    print("\n🚀 Send loop started\n")

    input_el = await find_input(page, timeout_ms=20000)
    if not input_el:
        print("❌ Input not found")
        return

    stats["refresh_target"] = random.randint(REFRESH_AFTER_MIN, REFRESH_AFTER_MAX)
    try: await input_el.click()
    except Exception: pass

    msgs_since_input_refresh = 0
    msgs_since_redirect_check = 0

    while True:
        try:
            if page.is_closed():
                print("\n🚪 Browser closed — stopping")
                return

            if LOGGED_OUT:
                print("\n🚨 Logged out — stopping")
                return

            if stats["since_refresh"] >= stats["refresh_target"]:
                async with PAGE_LOCK:
                    renamed = await rename_group(page) if NEW_GC_NAME else False
                    try:
                        if renamed:
                            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
                        else:
                            await page.reload(wait_until="domcontentloaded", timeout=30000)
                    except Exception:
                        pass

                try: await asyncio.wait_for(dismiss_notif_popup(page, max_rounds=1), timeout=1.5)
                except Exception: pass

                new_input = None
                for _ in range(5):
                    new_input = await find_input(page, timeout_ms=1200)
                    if new_input: break
                    await page.wait_for_timeout(200)

                if new_input:
                    input_el = new_input
                    try: await input_el.click()
                    except Exception: pass
                    stats["refreshes"] += 1
                    stats["since_refresh"] = 0
                    stats["refresh_target"] = random.randint(REFRESH_AFTER_MIN, REFRESH_AFTER_MAX)
                    msgs_since_input_refresh = 0
                    msgs_since_redirect_check = 0
                else:
                    input_el = None
                    await asyncio.sleep(0.8)
                    continue

            if msgs_since_input_refresh >= INPUT_REFRESH_EVERY:
                ne = await find_input(page, timeout_ms=3000)
                if ne:
                    input_el = ne
                    stats["input_refreshes"] += 1
                msgs_since_input_refresh = 0

            if msgs_since_redirect_check >= REDIRECT_CHECK_EVERY:
                msgs_since_redirect_check = 0
                try: cur = page.url
                except Exception: cur = ""

                if "/accounts/login" in cur:
                    LOGGED_OUT = True
                    print("\n🚨 Send-loop: Logged out.")
                    return

                if "direct/t/" not in cur:
                    await handle_redirect(page, source="send-loop")
                    if LOGGED_OUT: return
                    input_el = await find_input(page, timeout_ms=5000)
                    if not input_el:
                        await asyncio.sleep(0.5)
                        continue

            if input_el is None:
                input_el = await find_input(page, timeout_ms=3000)
                if input_el is None:
                    stats["failed"] += 1
                    msgs_since_redirect_check += 1
                    print(f"❌ Failed #{stats['failed']} (no input)")
                    await asyncio.sleep(0.3)
                    continue

            t0 = time.time()
            msg = build_message()
            ok, method = await put_text_and_send(page, input_el, msg)
            elapsed = time.time() - t0

            msgs_since_redirect_check += 1

            if ok:
                stats["sent"] += 1
                stats["since_refresh"] += 1
                msgs_since_input_refresh += 1
                if method == "click": stats["click_sends"] += 1
                else: stats["enter_sends"] += 1
            else:
                stats["failed"] += 1
                print(f"❌ Failed #{stats['failed']} (fill/send)")
                input_el = await find_input(page, timeout_ms=3000)
                msgs_since_input_refresh = 0
                elapsed = TARGET_CYCLE_SEC

            remaining = TARGET_CYCLE_SEC - elapsed
            if remaining > 0:
                await asyncio.sleep(remaining)

        except asyncio.CancelledError:
            print("\n🛑 Send cancelled")
            return
        except Exception as e:
            stats["failed"] += 1
            msgs_since_redirect_check += 1
            print(f"❌ Failed #{stats['failed']} ({type(e).__name__})")
            await asyncio.sleep(0.5)
            input_el = await find_input(page, timeout_ms=3000)


# ================= DASHBOARD =================
async def dashboard():
    psutil.cpu_percent(interval=None)
    await asyncio.sleep(0.5)

    last_sent = 0
    last_t = time.time()

    while True:
        await asyncio.sleep(1.0)

        elapsed = time.time() - stats["start"]
        h = int(elapsed // 3600)
        m = int((elapsed % 3600) // 60)
        s = int(elapsed % 60)

        dt = max(time.time() - last_t, 0.001)
        instant = (stats["sent"] - last_sent) / dt
        last_sent = stats["sent"]
        last_t = time.time()
        avg = stats["sent"] / max(elapsed, 0.01)

        cpu = psutil.cpu_percent(interval=None)
        vm = psutil.virtual_memory()
        used_gb = (vm.total - vm.available) / (1024**3)
        total_gb = vm.total / (1024**3)

        try: proc_rss = psutil.Process(os.getpid()).memory_info().rss / (1024**3)
        except Exception: proc_rss = 0.0

        W = 68
        lines = []
        lines.append("═" * W)
        status_tag = "LOGGED OUT ⚠️" if LOGGED_OUT else "LIVE"
        lines.append(f"  SINGLE GC SENDER  —  {status_tag}".ljust(W))
        lines.append("═" * W)
        lines.append(f"  Browser        : {BROWSER_LABEL} (headless)")
        lines.append(f"  OS             : {detect_os()}")
        lines.append(f"  GC Name        : {NEW_GC_NAME[:40] if NEW_GC_NAME else '(skip)'}")
        lines.append(f"  Prefix         : {PREFIX[:40]}")
        lines.append(f"  Target URL     : {TARGET_URL[:44]}")
        lines.append(f"  Uptime         : {h:02d}h {m:02d}m {s:02d}s")
        lines.append("─" * W)
        lines.append(f"  Sent           : {stats['sent']}  "
                     f"(click={stats['click_sends']}  enter={stats['enter_sends']})")
        lines.append(f"  Failed         : {stats['failed']}")
        lines.append(f"  Msgs / sec     : {instant:.2f}  (avg {avg:.2f})")
        lines.append("─" * W)
        lines.append(f"  Since Refresh  : {stats['since_refresh']} / {stats['refresh_target']}")
        lines.append(f"  Page Refresh   : {stats['refreshes']}")
        lines.append(f"  Renames        : {stats['renames']}")
        lines.append(f"  Input Refresh  : {stats['input_refreshes']}")
        lines.append(f"  Redirects      : {stats['redirects']}")
        lines.append("─" * W)
        lines.append(f"  CPU            : {cpu:.1f}%")
        lines.append(f"  RAM            : {used_gb:.2f} / {total_gb:.2f} GB ({vm.percent}%)")
        lines.append(f"  Py RAM         : {proc_rss:.3f} GB")
        lines.append("─" * W)
        lines.append(f"  {ts()}   |   Ctrl+C to stop".ljust(W))
        lines.append("═" * W)

        sys.stdout.write("\033[H\033[J" + "\n".join(lines) + "\n")
        sys.stdout.flush()


# ================= BROWSER HEALTH MONITOR =================
async def browser_health_monitor(browser, page, restart_flag):
    disconnected = asyncio.Event()

    def on_disconnect(*args):
        if not restart_flag.is_set():
            print("\n🔌 Browser disconnected unexpectedly.")
            disconnected.set()

    try:
        browser.on("disconnected", on_disconnect)
    except Exception:
        pass

    while True:
        try:
            await asyncio.sleep(60)
            if restart_flag.is_set():
                return
            try:
                if page.is_closed() or browser is None or not browser.is_connected():
                    print("\n🔌 Browser lost (periodic check).")
                    disconnected.set()
            except Exception:
                disconnected.set()

            if disconnected.is_set():
                print("⏳ Waiting 60s before restart...")
                await asyncio.sleep(60)
                if restart_flag.is_set():
                    return
                print("🔄 Restarting browser...")
                restart_flag.set()
                return

        except asyncio.CancelledError:
            return
        except Exception:
            pass


# ================= MAIN =================
async def main():
    global PREFIX, TARGET_URL, NEW_GC_NAME, PAGE_LOCK

    if not HARDCODED_SESSION_ID:
        print("❌ HARDCODED_SESSION_ID is empty.")
        sys.exit(1)
    if not HARDCODED_PREFIX:
        print("❌ HARDCODED_PREFIX is empty.")
        sys.exit(1)
    if not HARDCODED_GC_LINK or "direct/t/" not in HARDCODED_GC_LINK:
        print("❌ HARDCODED_GC_LINK invalid (must contain direct/t/).")
        sys.exit(1)

    PAGE_LOCK = asyncio.Lock()

    boost_python_process()
    ensure_msedge()

    PREFIX = HARDCODED_PREFIX
    NEW_GC_NAME = HARDCODED_GC_NAME
    TARGET_URL = HARDCODED_GC_LINK

    print("🚀 IG DM Sender — Edge headless only")
    print(f"🖥️  OS: {detect_os()}")
    print(f"📌 GC Name: {NEW_GC_NAME or '(skip)'}")
    print(f"🏷️  Prefix : {PREFIX}")
    print(f"🔗 GC Link: {TARGET_URL[:60]}")

    pw = await async_playwright().start()

    browser = None
    context = None
    monitor = None
    dash_task = None
    send_task = None
    health_task = None
    restart_flag = asyncio.Event()

    try:
        while not restart_flag.is_set():
            try:
                browser, context = await launch_browser(pw, HARDCODED_SESSION_ID)
                page = context.pages[0] if context.pages else await context.new_page()
                await attach_scripts(page)
            except Exception as e:
                print(f"❌ Launch: {type(e).__name__}: {e}")
                print("   Try: python -m playwright install-deps msedge && python -m playwright install msedge")
                await asyncio.sleep(60)
                continue

            # Verify session
            try:
                await page.goto("https://www.instagram.com/",
                                wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(2500)
            except Exception:
                pass

            try:
                cur = page.url
            except Exception:
                cur = ""

            if "/accounts/login" in cur or "/challenge/" in cur:
                print(f"❌ Session invalid — landed on {cur[:60]}")
                await _cleanup_browser(browser, context)
                browser = context = None
                break

            print("✅ Session valid")

            # Navigate to GC — allow SPA time to render
            try:
                await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
                # Networkidle is risky on Instagram DM (WebSocket keeps it busy) — timeout-wrapped
                try:
                    await page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass
                await page.wait_for_timeout(random.randint(3000, 5000))
                await dismiss_notif_popup(page, max_rounds=3)
            except Exception:
                pass

            # Try to find input, with one retry
            input_el = await find_input(page, timeout_ms=15000)
            if not input_el:
                print("⏳ Input not found (attempt 1), waiting 5s and retrying...")
                await page.wait_for_timeout(5000)
                await dismiss_notif_popup(page, max_rounds=2)
                input_el = await find_input(page, timeout_ms=15000)

            if not input_el:
                await dump_page_debug(page, "input_not_found")
                print("❌ Input not found in GC after 2 attempts")
                await _cleanup_browser(browser, context)
                browser = context = None
                break

            print("✅ GC ready\n")

            monitor = asyncio.create_task(gc_monitor(page))
            dash_task = asyncio.create_task(dashboard())
            send_task = asyncio.create_task(send_loop(page))
            health_task = asyncio.create_task(
                browser_health_monitor(browser, page, restart_flag)
            )

            try:
                done, pending = await asyncio.wait(
                    [dash_task, send_task, health_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for t in done:
                    try: t.result()
                    except asyncio.CancelledError: pass
                    except Exception as e: print(f"⚠️ Task error: {type(e).__name__}: {e}")
                for t in pending:
                    t.cancel()
                    try: await t
                    except (asyncio.CancelledError, Exception): pass
            except KeyboardInterrupt:
                break

            for t in (dash_task, send_task, monitor, health_task):
                if t and not t.done():
                    t.cancel()
                    try: await t
                    except (asyncio.CancelledError, Exception): pass
            await _cleanup_browser(browser, context)
            browser = context = None

            if restart_flag.is_set():
                print("\n♻️ Restarting browser in 60s...")
                await asyncio.sleep(60)
                restart_flag.clear()
            else:
                break

    finally:
        for t in (dash_task, send_task, monitor, health_task):
            if t and not t.done():
                t.cancel()
                try: await t
                except (asyncio.CancelledError, Exception): pass
        await _cleanup_browser(browser, context)
        try: await pw.stop()
        except Exception: pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n🛑 Stopped. Sent: {stats['sent']}  |  Failed: {stats['failed']}")
