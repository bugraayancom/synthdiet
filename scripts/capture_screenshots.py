"""Capture screenshots of every Streamlit page for the README.

Spins up the app via subprocess, navigates with Playwright, drives the
sidebar widgets where needed (so pages have real content) and writes
PNG files to ``app/assets/screenshots/``.

Run from the repository root::

    python scripts/capture_screenshots.py
"""
from __future__ import annotations

import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
APP_FILE = ROOT / "app" / "streamlit_app.py"
OUT_DIR = ROOT / "app" / "assets" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PORT = 8765
URL = f"http://localhost:{PORT}"


def _free_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def start_streamlit() -> subprocess.Popen:
    if not _free_port(PORT):
        raise RuntimeError(f"Port {PORT} already in use")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP_FILE),
        "--server.headless=true",
        f"--server.port={PORT}",
        "--server.runOnSave=false",
        "--browser.gatherUsageStats=false",
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )
    # Wait for server up
    for _ in range(60):
        if not _free_port(PORT):
            time.sleep(2.0)  # let it warm up
            return proc
        time.sleep(0.5)
    proc.kill()
    raise RuntimeError("Streamlit failed to start within 30 s")


def stop_streamlit(proc: subprocess.Popen) -> None:
    try:
        proc.send_signal(signal.SIGINT)
        proc.wait(timeout=8)
    except Exception:
        proc.kill()


def _hide_sidebar_when_collapsed(page) -> None:
    """No-op placeholder; left here for future tweaks."""
    pass


def _wait_quiet(page, ms: int = 1500) -> None:
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(ms)


def _click_sidebar_link(page, label: str) -> None:
    """Click a Streamlit page-nav link in the sidebar by visible label."""
    nav = page.locator('[data-testid="stSidebarNav"]')
    nav.get_by_text(label, exact=False).first.click()
    _wait_quiet(page, 2500)


def _set_slider(page, label_substring: str, target_pct: float) -> None:
    """Coarsely move a Streamlit slider to a fractional position (0..1)."""
    sliders = page.locator('[data-testid="stSlider"]')
    count = sliders.count()
    for i in range(count):
        if label_substring.lower() in (sliders.nth(i).inner_text() or "").lower():
            handle = sliders.nth(i).locator('[role="slider"]').first
            box = handle.bounding_box()
            if not box:
                return
            track = sliders.nth(i).locator('div[data-baseweb="slider"] > div').first
            tbox = track.bounding_box()
            if not tbox:
                return
            target_x = tbox["x"] + tbox["width"] * target_pct
            target_y = tbox["y"] + tbox["height"] / 2
            handle.click()
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.mouse.down()
            page.mouse.move(target_x, target_y, steps=10)
            page.mouse.up()
            page.wait_for_timeout(400)
            return


def capture() -> list[str]:
    saved: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 1100},
            device_scale_factor=2,  # @2x for sharp screenshots
        )
        page = context.new_page()

        # ---- Hero (short viewport, Home page, very first capture) ----
        page.goto(URL, wait_until="networkidle", timeout=45_000)
        _wait_quiet(page, 2500)
        page.set_viewport_size({"width": 1440, "height": 760})
        page.wait_for_timeout(400)
        path = OUT_DIR / "00_hero.png"
        page.screenshot(path=str(path), full_page=False)
        saved.append(str(path))
        print(f"saved {path.name}")

        # Restore taller viewport for the rest
        page.set_viewport_size({"width": 1440, "height": 1100})
        page.wait_for_timeout(400)

        # ---- Home -----------------------------------------------------
        path = OUT_DIR / "01_home.png"
        page.screenshot(path=str(path), full_page=False)
        saved.append(str(path))
        print(f"saved {path.name}")

        # ---- Cohort Builder ------------------------------------------
        try:
            _click_sidebar_link(page, "Cohort Builder")
        except Exception as exc:
            print(f"cohort nav failed: {exc}")
        _wait_quiet(page, 3000)
        path = OUT_DIR / "02_cohort_builder.png"
        page.screenshot(path=str(path), full_page=False)
        saved.append(str(path))
        print(f"saved {path.name}")

        # ---- Diet Simulator ------------------------------------------
        try:
            _click_sidebar_link(page, "Diet Simulator")
        except Exception as exc:
            print(f"sim nav failed: {exc}")
        _wait_quiet(page, 3500)
        path = OUT_DIR / "03_diet_simulator.png"
        page.screenshot(path=str(path), full_page=False)
        saved.append(str(path))
        print(f"saved {path.name}")

        # ---- RCT Engine ----------------------------------------------
        try:
            _click_sidebar_link(page, "RCT Engine")
        except Exception as exc:
            print(f"rct nav failed: {exc}")
        _wait_quiet(page, 2500)
        # Click "Run trial" if present
        try:
            page.get_by_role("button", name="🧪 Run trial").click(timeout=5000)
            _wait_quiet(page, 5000)
        except Exception:
            pass
        path = OUT_DIR / "04_rct_engine.png"
        page.screenshot(path=str(path), full_page=False)
        saved.append(str(path))
        print(f"saved {path.name}")

        # ---- Case Studies --------------------------------------------
        try:
            _click_sidebar_link(page, "Case Studies")
        except Exception as exc:
            print(f"cases nav failed: {exc}")
        _wait_quiet(page, 2500)
        path = OUT_DIR / "05_case_studies.png"
        page.screenshot(path=str(path), full_page=False)
        saved.append(str(path))
        print(f"saved {path.name}")

        # ---- About ---------------------------------------------------
        try:
            _click_sidebar_link(page, "About")
        except Exception as exc:
            print(f"about nav failed: {exc}")
        _wait_quiet(page, 1500)
        path = OUT_DIR / "06_about.png"
        page.screenshot(path=str(path), full_page=False)
        saved.append(str(path))
        print(f"saved {path.name}")

        browser.close()
    return saved


def main() -> int:
    if shutil.which("streamlit") is None and not (ROOT / ".venv" / "bin" / "streamlit").exists():
        print("Streamlit not installed", file=sys.stderr)
        return 1

    print("Starting Streamlit…")
    proc = start_streamlit()
    try:
        print("Capturing screenshots…")
        files = capture()
    finally:
        print("Stopping Streamlit…")
        stop_streamlit(proc)

    print("\nWrote:")
    for f in files:
        size_kb = Path(f).stat().st_size / 1024
        print(f"  {f}  ({size_kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
