#!/usr/bin/env python3
# ============================================================
# Moode Radio Builder v1
# MULTIPLATFORM + WATCHDOG + AUTO PACKAGE INSTALL + LOGO JPG
# MOODE AUDIO COMPATIBLE - MATCHES radio.php STRUCTURE
# NOW WITH PYVIPS FOR SVG SUPPORT (replaces CairoSVG)
# ============================================================

import sys
import subprocess
import importlib.util
import platform

# ============================================================
# AUTO PACKAGE MANAGEMENT
# ============================================================

REQUIRED_PACKAGES = {
    "requests": "requests",
    "bs4": "beautifulsoup4",
    "PIL": "pillow"
}

OPTIONAL_PACKAGES = {
    "pyvips": "pyvips"
}


def get_os_name():
    """Detect operating system."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    return "unknown"


def ensure_packages(packages, optional=False):
    """Install missing packages automatically."""
    for module, package in packages.items():
        if importlib.util.find_spec(module) is None:
            print(f"[BOOTSTRAP] Package '{package}' missing → installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            except subprocess.CalledProcessError:
                if not optional:
                    print(f"[BOOTSTRAP] ERROR: Failed to install required package '{package}'")
                    sys.exit(1)
                else:
                    print(f"[BOOTSTRAP] WARNING: Optional package '{package}' could not be installed")
        else:
            print(f"[BOOTSTRAP] Package '{package}' OK")


def prompt_yes_no(message, default_yes=True):
    """Prompt user for yes/no confirmation."""
    suffix = " (Y/n): " if default_yes else " (y/N): "
    while True:
        response = input(message + suffix).strip().lower()
        if response == "":
            return default_yes
        if response in ('y', 'yes', 'ja', 'j'):
            return True
        if response in ('n', 'no', 'nee'):
            return False
        print("  → Please enter 'y' or 'n'")


def check_pyvips():
    """Check PyVips availability and prompt user if not available."""
    global SVG_ENABLED, pyvips
    SVG_ENABLED = False
    pyvips = None

    try:
        import pyvips as _pyvips
        pyvips = _pyvips
        # Test if vips can actually load SVG
        test_svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>'
        _pyvips.Image.new_from_buffer(test_svg, "")
        SVG_ENABLED = True
        print("[BOOTSTRAP] PyVips available → SVG conversion enabled ✓")
        print(f"[BOOTSTRAP] libvips version: {_pyvips.version(0)}.{_pyvips.version(1)}.{_pyvips.version(2)}")
        return True

    except OSError as e:
        os_name = get_os_name()
        print("\n" + "=" * 65)
        print("  ⚠  WARNING: PyVips requires native libvips library!")
        print("=" * 65)
        print(f"\n  Error: {e}\n")

        print("  Installation instructions:")
        if os_name == "windows":
            print("  ┌─────────────────────────────────────────────────────────────┐")
            print("  │  Windows: Install libvips                                   │")
            print("  │                                                             │")
            print("  │  Option 1 - Automatic (recommended):                        │")
            print("  │  pip install pyvips                                         │")
            print("  │  (Downloads vips DLLs automatically on first use)           │")
            print("  │                                                             │")
            print("  │  Option 2 - Manual:                                         │")
            print("  │  1. Download from: https://github.com/libvips/libvips/      │")
            print("  │     releases (vips-dev-w64-all-x.x.x.zip)                   │")
            print("  │  2. Extract to C:\\vips or add bin\\ to PATH                 │")
            print("  │  3. Restart terminal/IDE                                    │")
            print("  └─────────────────────────────────────────────────────────────┘")
        elif os_name == "macos":
            print("  ┌─────────────────────────────────────────────────────────────┐")
            print("  │  macOS: Install via Homebrew                                │")
            print("  │  $ brew install vips                                        │")
            print("  └─────────────────────────────────────────────────────────────┘")
        elif os_name == "linux":
            print("  ┌─────────────────────────────────────────────────────────────┐")
            print("  │  Linux (Debian/Ubuntu):                                     │")
            print("  │  $ sudo apt-get install libvips-dev                         │")
            print("  │                                                             │")
            print("  │  Linux (Fedora/RHEL):                                       │")
            print("  │  $ sudo dnf install vips-devel                              │")
            print("  │                                                             │")
            print("  │  Linux (Arch):                                              │")
            print("  │  $ sudo pacman -S libvips                                   │")
            print("  └─────────────────────────────────────────────────────────────┘")

        print("\n  Impact if you proceed without SVG support:")
        print("  • Stations with SVG logos will have NO logo image")
        print("  • PNG, JPG, WEBP logos will still work normally")
        print("  • You can re-run the scraper later after installing libvips")
        print("=" * 65)

        if prompt_yes_no("\n  Do you wish to proceed without SVG support?", default_yes=True):
            print("  → Proceeding without SVG support...\n")
            return True
        else:
            print("  → Exiting. Please install libvips and try again.")
            sys.exit(0)

    except ImportError:
        print("\n" + "=" * 65)
        print("  ⚠  WARNING: PyVips module not installed!")
        print("=" * 65)
        print("\n  The pyvips Python package is not available.")
        print("  This is needed to convert SVG logos to JPG format.\n")
        print("  Impact if you proceed without SVG support:")
        print("  • Stations with SVG logos will have NO logo image")
        print("  • PNG, JPG, WEBP logos will still work normally")
        print("=" * 65)

        if prompt_yes_no("\n  Do you wish to proceed without SVG support?", default_yes=True):
            print("  → Proceeding without SVG support...\n")
            return True
        else:
            print("  → Exiting. Install with: pip install pyvips")
            sys.exit(0)

    except Exception as e:
        print("\n" + "=" * 65)
        print("  ⚠  WARNING: PyVips failed to initialize!")
        print("=" * 65)
        print(f"\n  Error: {e}\n")
        print("  Impact if you proceed without SVG support:")
        print("  • Stations with SVG logos will have NO logo image")
        print("  • PNG, JPG, WEBP logos will still work normally")
        print("=" * 65)

        if prompt_yes_no("\n  Do you wish to proceed without SVG support?", default_yes=True):
            print("  → Proceeding without SVG support...\n")
            return True
        else:
            print("  → Exiting.")
            sys.exit(0)


# ============================================================
# BOOTSTRAP SEQUENCE
# ============================================================

print("\n" + "=" * 65)
print("  RADIO STREAM SCRAPER v29 - Bootstrap")
print("  (Now using PyVips for SVG support)")
print("=" * 65)

ensure_packages(REQUIRED_PACKAGES)
ensure_packages(OPTIONAL_PACKAGES, optional=True)

# Check PyVips/SVG support with user confirmation
SVG_ENABLED = False
pyvips = None
check_pyvips()

print(f"[BOOTSTRAP] Detected OS: {get_os_name()}")
print(f"[BOOTSTRAP] SVG support: {'ENABLED ✓' if SVG_ENABLED else 'DISABLED ✗'}")
print("=" * 65 + "\n")

# ============================================================
# IMPORTS (after bootstrap)
# ============================================================

import os
import re
import csv
import json
import time
import logging
import traceback
import zipfile
import webbrowser
import threading
import requests
from pathlib import Path
from datetime import datetime, timezone
from io import BytesIO
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from PIL import Image

# ============================================================
# CONFIG - MATCHES MOODE radio.php STRUCTURE
# ============================================================

# Radio Browser API (multiple servers for redundancy)
API_SERVERS = [
    "https://de1.api.radio-browser.info",
    "https://de2.api.radio-browser.info",
    "https://nl1.api.radio-browser.info",
    "https://at1.api.radio-browser.info",
]
API_ENDPOINT = "/json/stations/search"

# Radio Browser website for reference
RADIO_BROWSER_URL = "https://www.radio-browser.info/"
RADIO_BROWSER_COUNTRIES_URL = "https://www.radio-browser.info/#/countries"
RADIO_BROWSER_TAGS_URL = "https://www.radio-browser.info/#/tags"
RADIO_BROWSER_LANGUAGES_URL = "https://www.radio-browser.info/#/languages"

# Common country codes reference
COMMON_COUNTRY_CODES = {
    "NL": "Netherlands", "BE": "Belgium", "DE": "Germany",
    "GB": "United Kingdom", "US": "United States", "FR": "France",
    "ES": "Spain", "IT": "Italy", "AT": "Austria", "CH": "Switzerland",
    "PL": "Poland", "SE": "Sweden", "NO": "Norway", "DK": "Denmark",
    "FI": "Finland", "PT": "Portugal", "IE": "Ireland", "AU": "Australia",
    "CA": "Canada", "BR": "Brazil", "JP": "Japan", "KR": "South Korea",
    "IN": "India", "RU": "Russia", "ZA": "South Africa",
}

# Common tags/genres reference
COMMON_TAGS = [
    "pop", "rock", "jazz", "classical", "news", "talk", "country",
    "electronic", "dance", "house", "techno", "trance", "ambient",
    "hip hop", "rap", "r&b", "soul", "blues", "folk", "metal",
    "punk", "reggae", "latin", "world", "80s", "90s", "oldies",
    "top 40", "hits", "alternative", "indie", "lounge", "chill"
]

# Common languages reference
COMMON_LANGUAGES = [
    "dutch", "english", "german", "french", "spanish", "italian",
    "portuguese", "polish", "russian", "japanese", "korean", "chinese",
    "arabic", "hindi", "turkish", "swedish", "norwegian", "danish",
    "finnish", "greek", "czech", "hungarian", "romanian"
]

BASE_DIR = Path(__file__).parent.resolve()

# moOde directory structure (matches radio.php paths)
RADIO_DIR = BASE_DIR / "RADIO"
LOGO_DIR = BASE_DIR / "radio-logos"
THUMB_DIR = LOGO_DIR / "thumbs"

# Output files
JSON_OUT = BASE_DIR / "station_data.json"
ZIP_OUT = BASE_DIR / "moode_radio_backup.zip"
CSV_OUT = BASE_DIR / "radiostreams.csv"
LOG_FILE = BASE_DIR / "scraper.log"
SUMMARY_OUT = BASE_DIR / "run_summary.json"
ERROR_OUT = BASE_DIR / "error_report.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
AUDIO_EXTENSIONS = (".mp3", ".aac", ".aacp", ".ogg", ".m3u8", ".flac", ".opus")

# Timeout settings
REQUEST_TIMEOUT = 15
STATION_TIMEOUT = 60
LOGO_TIMEOUT = 30
REQUEST_DELAY = 0.3

# Logo sizes per moOde specs
LOGO_SIZE = (335, 335)
THUMB_SIZE = (80, 80)
THUMB_SM_SIZE = (80, 80)

# Database fields matching cfg_radio table structure
FIELDS = [
    "id", "station", "name", "type", "logo", "genre", "broadcaster",
    "language", "country", "region", "bitrate", "format", "geo_fenced",
    "home_page", "monitor"
]

# Create directories
RADIO_DIR.mkdir(parents=True, exist_ok=True)
LOGO_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOGGER
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("radio-scraper")


# ============================================================
# TIMEOUT HELPER - NO RETRY ON TIMEOUT
# ============================================================

def run_with_timeout(func, args=(), kwargs=None, timeout=STATION_TIMEOUT):
    """Run a function with a timeout. NO RETRY on timeout."""
    if kwargs is None:
        kwargs = {}

    result_container = {"result": None, "error": None, "completed": False}

    def target():
        try:
            result_container["result"] = func(*args, **kwargs)
            result_container["completed"] = True
        except Exception as e:
            result_container["error"] = e
            result_container["completed"] = True

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    if not result_container["completed"]:
        return False, f"TIMEOUT after {timeout}s - skipped (no retry)"

    if result_container["error"]:
        return False, str(result_container["error"])

    return True, result_container["result"]


# ============================================================
# WATCHDOG - MONITORING & ERROR TRACKING
# ============================================================

class Watchdog:
    """Monitors scraping progress and tracks errors for reporting."""

    def __init__(self):
        self.start_time = datetime.now(timezone.utc)
        self.errors = []
        self.warnings = []
        self.timeouts = []
        self.metrics = {
            "stations_total": 0,
            "stations_success": 0,
            "stations_failed": 0,
            "stations_skipped": 0,
            "stations_timeout": 0,
            "streams_found": 0,
            "pls_created": 0,
            "logos_converted": 0,
            "logos_skipped": 0,
            "logos_failed": 0,
            "logos_timeout": 0,
            "svg_skipped": 0
        }
        self._lock = threading.Lock()

    def log_error(self, station, phase, message, exception=None):
        """Log an error for a station (thread-safe)."""
        with self._lock:
            self.errors.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "station": station,
                "phase": phase,
                "message": message,
                "exception": str(exception) if exception else None
            })

    def log_warning(self, station, message):
        """Log a warning for a station (thread-safe)."""
        with self._lock:
            self.warnings.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "station": station,
                "message": message
            })

    def log_timeout(self, station, phase, duration):
        """Log a timeout - NOT retried (thread-safe)."""
        with self._lock:
            self.timeouts.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "station": station,
                "phase": phase,
                "duration_seconds": duration,
                "action": "skipped (no retry)"
            })
            self.metrics["stations_timeout"] += 1

    def increment(self, metric, value=1):
        """Thread-safe metric increment."""
        with self._lock:
            if metric in self.metrics:
                self.metrics[metric] += value

    def finish(self):
        """Generate summary and error reports."""
        end_time = datetime.now(timezone.utc)
        runtime = (end_time - self.start_time).total_seconds()

        summary = {
            "version": "v29",
            "svg_library": "pyvips",
            "started_at": self.start_time.isoformat(),
            "ended_at": end_time.isoformat(),
            "runtime_seconds": runtime,
            "runtime_formatted": f"{int(runtime // 60)}m {int(runtime % 60)}s",
            "svg_support": SVG_ENABLED,
            "timeout_setting": f"{STATION_TIMEOUT}s per station (no retry)",
            "metrics": self.metrics,
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "total_timeouts": len(self.timeouts)
        }

        with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        error_report = {
            "generated_at": end_time.isoformat(),
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "total_timeouts": len(self.timeouts),
            "errors": self.errors,
            "warnings": self.warnings,
            "timeouts": self.timeouts
        }
        with open(ERROR_OUT, "w", encoding="utf-8") as f:
            json.dump(error_report, f, indent=2, ensure_ascii=False)

        m = self.metrics
        print("\n" + "=" * 65)
        print("  SCRAPING SUMMARY")
        print("=" * 65)
        print(f"  Runtime:           {summary['runtime_formatted']}")
        print(f"  SVG Support:       {'Enabled (pyvips)' if SVG_ENABLED else 'Disabled'}")
        print(f"  Timeout:           {STATION_TIMEOUT}s per station (no retry)")
        print("-" * 65)
        print(f"  Stations Total:    {m['stations_total']}")
        print(f"  Stations Success:  {m['stations_success']}")
        print(f"  Stations Failed:   {m['stations_failed']}")
        print(f"  Stations Timeout:  {m['stations_timeout']} (skipped, no retry)")
        print(f"  Stations Skipped:  {m['stations_skipped']}")
        print("-" * 65)
        print(f"  PLS Files Created: {m['pls_created']}")
        print(f"  Logos Converted:   {m['logos_converted']}")
        print(f"  Logos Skipped:     {m['logos_skipped']}")
        print(f"  Logos Failed:      {m['logos_failed']}")
        if m['svg_skipped'] > 0:
            print(f"  SVG Skipped:       {m['svg_skipped']} (pyvips not available)")
        print("-" * 65)
        print(f"  Errors:            {len(self.errors)}")
        print(f"  Warnings:          {len(self.warnings)}")
        print(f"  Timeouts:          {len(self.timeouts)}")
        print("=" * 65)

        if self.errors:
            logger.warning(f"Completed with {len(self.errors)} errors - see {ERROR_OUT}")
        if not self.errors and not self.timeouts:
            logger.info("Completed successfully with no errors")


# ============================================================
# HELPERS
# ============================================================

def open_browser(url):
    """Open a URL in the default web browser."""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        logger.warning(f"Could not open browser: {e}")
        return False


def sanitize_filename(name: str) -> str:
    """Sanitize filename for moOde compatibility."""
    if not name:
        return "unnamed"
    sanitized = re.sub(r"[^\w\s\-]", "", name, flags=re.UNICODE)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    if not sanitized:
        sanitized = "unnamed"
    if len(sanitized) > 100:
        sanitized = sanitized[:100].rstrip(" -")
    return sanitized


def convert_svg_to_png(svg_data, width, height):
    """Convert SVG data to PNG using pyvips."""
    if not SVG_ENABLED or pyvips is None:
        return None
    
    try:
        # Load SVG from buffer
        image = pyvips.Image.new_from_buffer(svg_data, "", access="sequential")
        
        # Calculate scale to fit within target size
        scale = min(width / image.width, height / image.height)
        
        # Resize if needed
        if scale < 1:
            image = image.resize(scale)
        
        # Convert to PNG in memory
        png_data = image.write_to_buffer(".png")
        return png_data
    
    except Exception as e:
        logger.warning(f"SVG conversion failed: {e}")
        return None


def save_jpg(content, path, size=None, is_svg=False):
    """Convert image content to JPG and save."""
    # Handle SVG conversion via pyvips
    if is_svg:
        if not SVG_ENABLED:
            return None, "svg_skip"
        png_data = convert_svg_to_png(content, size[0] if size else 335, size[1] if size else 335)
        if png_data is None:
            return None, "svg_failed"
        content = png_data
    
    img = Image.open(BytesIO(content))
    
    if img.mode in ("RGBA", "P", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        if img.mode in ("RGBA", "LA"):
            try:
                alpha = img.split()[-1]
                background.paste(img, mask=alpha)
            except Exception:
                background.paste(img)
        else:
            background.paste(img)
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    if size:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", size, (255, 255, 255))
        offset = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
        canvas.paste(img, offset)
        img = canvas

    img.save(path, format="JPEG", quality=92, optimize=True)
    return img, "ok"


def create_thumbnails(img, safe_name):
    """Create thumbnails matching moOde structure."""
    thumb_path = THUMB_DIR / f"{safe_name}.jpg"
    thumb = img.copy()
    thumb.thumbnail(THUMB_SIZE, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", THUMB_SIZE, (255, 255, 255))
    offset = ((THUMB_SIZE[0] - thumb.width) // 2, (THUMB_SIZE[1] - thumb.height) // 2)
    canvas.paste(thumb, offset)
    canvas.save(thumb_path, format="JPEG", quality=85, optimize=True)

    thumb_sm_path = THUMB_DIR / f"{safe_name}_sm.jpg"
    canvas.save(thumb_sm_path, format="JPEG", quality=85, optimize=True)
    return thumb_path, thumb_sm_path


def is_svg_content(url, content_type, content):
    """Check if content is SVG."""
    url_lower = url.lower()
    if url_lower.endswith(".svg"):
        return True
    if "svg" in content_type.lower():
        return True
    # Check content starts with SVG marker
    if content[:100].lstrip().startswith((b'<svg', b'<?xml')):
        if b'<svg' in content[:500]:
            return True
    return False


def download_logo_internal(url, safe_name):
    """Internal logo download function."""
    jpg_path = LOGO_DIR / f"{safe_name}.jpg"
    if jpg_path.exists():
        return "exists", safe_name

    r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    
    content_type = r.headers.get('content-type', '').lower()
    is_svg = is_svg_content(url, content_type, r.content)
    
    if is_svg:
        if not SVG_ENABLED:
            return "svg_skip", None
        img, status = save_jpg(r.content, jpg_path, size=LOGO_SIZE, is_svg=True)
        if status != "ok":
            return status, None
    else:
        img, status = save_jpg(r.content, jpg_path, size=LOGO_SIZE, is_svg=False)
        if status != "ok":
            return status, None
    
    create_thumbnails(img, safe_name)
    return "converted", safe_name


def download_and_convert_logo(url, station_name, watchdog):
    """Download logo with timeout - NO RETRY on timeout."""
    if not url:
        watchdog.increment("logos_skipped")
        return None

    safe_name = sanitize_filename(station_name)
    success, result = run_with_timeout(
        download_logo_internal, args=(url, safe_name), timeout=LOGO_TIMEOUT
    )

    if not success:
        if "TIMEOUT" in str(result):
            watchdog.increment("logos_timeout")
            watchdog.log_timeout(station_name, "logo_download", LOGO_TIMEOUT)
            logger.warning(f"{station_name}: logo TIMEOUT ({LOGO_TIMEOUT}s) → skipped")
        else:
            watchdog.increment("logos_failed")
            watchdog.log_error(station_name, "logo", str(result))
            logger.warning(f"{station_name}: logo failed - {result}")
        return None

    status, name = result
    if status == "exists":
        watchdog.increment("logos_converted")
        return name
    elif status == "svg_skip":
        watchdog.increment("svg_skipped")
        watchdog.increment("logos_skipped")
        return None
    elif status == "svg_failed":
        watchdog.increment("logos_failed")
        watchdog.log_warning(station_name, "SVG conversion failed")
        return None
    elif status == "converted":
        watchdog.increment("logos_converted")
        return name
    return None


def detect_format(url, codec=None):
    """Detect audio format from URL or codec string."""
    if codec:
        codec_upper = codec.upper()
        if codec_upper in ["MP3", "AAC", "AAC+", "OGG", "FLAC", "OPUS", "HLS"]:
            return codec_upper
    url_lower = url.lower()
    if ".mp3" in url_lower:
        return "MP3"
    elif ".aac" in url_lower or ".aacp" in url_lower:
        return "AAC"
    elif ".ogg" in url_lower:
        return "OGG"
    elif ".flac" in url_lower:
        return "FLAC"
    elif ".opus" in url_lower:
        return "OPUS"
    elif ".m3u8" in url_lower:
        return "HLS"
    return "MP3"


def create_pls_file(station_name, stream_url, watchdog):
    """Create .pls file matching moOde format."""
    safe_name = sanitize_filename(station_name)
    pls_path = RADIO_DIR / f"{safe_name}.pls"
    contents = f"""[playlist]
File1={stream_url}
Title1={station_name}
Length1=-1
NumberOfEntries=1
Version=2
"""
    try:
        with open(pls_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(contents)
        watchdog.increment("pls_created")
        return safe_name
    except Exception as e:
        watchdog.log_error(station_name, "pls", str(e), e)
        return None


# ============================================================
# RADIO BROWSER API
# ============================================================

def fetch_stations_from_api(params, watchdog):
    """Fetch stations from the Radio Browser API with server fallback."""
    for server in API_SERVERS:
        try:
            url = server + API_ENDPOINT
            logger.info(f"Trying API server: {server}")
            response = requests.get(url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            logger.info(f"API returned {len(data)} stations from {server}")
            return data
        except requests.RequestException as e:
            logger.warning(f"API server {server} failed: {e}")
            continue
    logger.error("All API servers failed!")
    watchdog.log_error("API", "fetch", "All Radio Browser API servers failed")
    return []


def process_api_station(station, station_name, watchdog):
    """Process a single API station."""
    stream_url = station.get("url", "") or station.get("url_resolved", "")
    if not stream_url:
        return None, "no_stream"

    logo_url = station.get("favicon", "")
    logo_name = download_and_convert_logo(logo_url, station_name, watchdog) if logo_url else None
    safe_name = sanitize_filename(station_name)
    create_pls_file(station_name, stream_url, watchdog)

    return {
        "stream_url": stream_url,
        "logo_name": logo_name,
        "safe_name": safe_name
    }, "ok"


def scrape_via_api(choice, user_input, watchdog):
    """Scrape stations via Radio Browser API."""
    params = {
        "hidebroken": "true",
        "limit": 500,
        "order": "clickcount",
        "reverse": "true"
    }

    if choice == "country":
        params["countrycode"] = user_input
    elif choice == "tag":
        params["tag"] = user_input
    elif choice == "language":
        params["language"] = user_input
    elif choice == "name":
        params["name"] = user_input

    api_stations = fetch_stations_from_api(params, watchdog)
    watchdog.metrics["stations_total"] = len(api_stations)

    if not api_stations:
        logger.warning("No stations returned from API")
        return {"fields": FIELDS, "stations": []}, []

    json_data = {"fields": FIELDS, "stations": []}
    csv_rows = []
    station_id = 500
    used_names = set()
    total = len(api_stations)
    start_time = time.time()

    for idx, station in enumerate(api_stations, 1):
        station_name = station.get("name", "").strip() or f"Station {idx}"

        elapsed = time.time() - start_time
        avg_per_station = elapsed / idx if idx > 0 else 0
        remaining = (total - idx) * avg_per_station
        eta_min, eta_sec = int(remaining // 60), int(remaining % 60)

        logger.info(f"[{idx}/{total}] {station_name} (ETA: {eta_min}m {eta_sec}s)")

        success, result = run_with_timeout(
            process_api_station, args=(station, station_name, watchdog), timeout=STATION_TIMEOUT
        )

        if not success:
            if "TIMEOUT" in str(result):
                watchdog.log_timeout(station_name, "station_process", STATION_TIMEOUT)
                logger.warning(f"{station_name}: TIMEOUT ({STATION_TIMEOUT}s) → skipped")
            else:
                watchdog.increment("stations_failed")
                watchdog.log_error(station_name, "api_process", str(result))
            continue

        processed, status = result
        if status == "no_stream":
            watchdog.increment("stations_skipped")
            continue
        if processed is None:
            watchdog.increment("stations_failed")
            continue

        safe_name = processed["safe_name"]
        original_safe_name = safe_name
        counter = 1
        while safe_name in used_names:
            safe_name = f"{original_safe_name} {counter}"
            counter += 1
        used_names.add(safe_name)

        station_record = {
            "id": station_id,
            "station": processed["stream_url"],
            "name": safe_name,
            "type": "r",
            "logo": "local" if processed["logo_name"] else "",
            "genre": (station.get("tags", "") or "")[:255],
            "broadcaster": (station.get("name", "") or "")[:100],
            "language": (station.get("language", "") or "")[:50],
            "country": (station.get("country", "") or "")[:50],
            "region": (station.get("state", "") or "")[:50],
            "bitrate": str(station.get("bitrate", "")) if station.get("bitrate") else "",
            "format": detect_format(processed["stream_url"], station.get("codec")),
            "geo_fenced": "No",
            "home_page": (station.get("homepage", "") or "")[:255],
            "monitor": ""
        }

        json_data["stations"].append(station_record)
        csv_rows.append({
            "id": station_id,
            "station": safe_name,
            "stream_url": processed["stream_url"],
            "logo": "local" if processed["logo_name"] else ""
        })

        watchdog.increment("streams_found")
        watchdog.increment("stations_success")
        station_id += 1
        time.sleep(REQUEST_DELAY)

    return json_data, csv_rows


# ============================================================
# MOODE ZIP CREATION
# ============================================================

def create_moode_zip(json_data):
    """Create moOde-compatible backup ZIP."""
    logger.info("Creating moOde-compatible backup ZIP...")
    try:
        with zipfile.ZipFile(ZIP_OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            if JSON_OUT.exists():
                zipf.write(JSON_OUT, "station_data.json")

            pls_count = 0
            if RADIO_DIR.exists():
                for pls_file in sorted(RADIO_DIR.iterdir()):
                    if pls_file.is_file() and pls_file.suffix.lower() == '.pls':
                        zipf.write(pls_file, f"RADIO/{pls_file.name}")
                        pls_count += 1

            logo_count = 0
            if LOGO_DIR.exists():
                for logo_file in sorted(LOGO_DIR.iterdir()):
                    if logo_file.is_file() and logo_file.suffix.lower() in ['.jpg', '.jpeg']:
                        zipf.write(logo_file, f"radio-logos/{logo_file.name}")
                        logo_count += 1

            thumb_count = 0
            if THUMB_DIR.exists():
                for thumb_file in sorted(THUMB_DIR.iterdir()):
                    if thumb_file.is_file() and thumb_file.suffix.lower() in ['.jpg', '.jpeg']:
                        zipf.write(thumb_file, f"radio-logos/thumbs/{thumb_file.name}")
                        thumb_count += 1

        logger.info(f"ZIP saved: {pls_count} PLS, {logo_count} logos, {thumb_count} thumbs")
        return True
    except Exception as e:
        logger.error(f"Failed to create ZIP: {e}")
        return False


def verify_moode_zip():
    """Verify the moOde ZIP file structure."""
    if not ZIP_OUT.exists():
        return False

    print(f"\n{'=' * 65}")
    print("  moOde ZIP VERIFICATION (v29 - pyvips)")
    print("=" * 65)

    try:
        with zipfile.ZipFile(ZIP_OUT, 'r') as zipf:
            if zipf.testzip():
                print("  ✗ ZIP file corrupted!")
                return False
            print("  ✓ ZIP integrity: OK")

            all_files = zipf.namelist()
            pls_files = [f for f in all_files if f.startswith("RADIO/") and f.endswith('.pls')]
            logo_files = [f for f in all_files if f.startswith("radio-logos/") and "/thumbs/" not in f]
            thumb_files = [f for f in all_files if "thumbs/" in f]

            print(f"\n  Contents:")
            print(f"    PLS files:    {len(pls_files)}")
            print(f"    Logos:        {len(logo_files)}")
            print(f"    Thumbnails:   {len(thumb_files)}")

            total_size = sum(info.file_size for info in zipf.infolist())
            compressed_size = sum(info.compress_size for info in zipf.infolist())
            print(f"\n  Size: {compressed_size / 1024:.1f} KB (from {total_size / 1024:.1f} KB)")

        print("=" * 65)
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


# ============================================================
# MENU DISPLAY FUNCTIONS
# ============================================================

def show_main_menu():
    """Display the main menu with Radio Browser reference info."""
    print("\n" + "=" * 65)
    print("         RADIO STREAM SCRAPER v29")
    print("         moOde Audio Compatible (uses PyVips)")
    print("=" * 65)
    print(f"\n  SVG Support:       {'ENABLED ✓ (pyvips)' if SVG_ENABLED else 'DISABLED ✗'}")
    print(f"  Station Timeout:   {STATION_TIMEOUT}s (skip after timeout, no retry)")

    print("\n" + "-" * 65)
    print("  DATA SOURCES (Radio Browser API)")
    print("-" * 65)
    print("  [1] All stations (top 500 by popularity)")
    print("  [2] By country code")
    print("  [3] By tag/genre")
    print("  [4] By language")
    print("  [5] By station name")

    print("\n" + "-" * 65)
    print("  HELP & REFERENCE")
    print("-" * 65)
    print("  [6] Show country codes reference")
    print("  [7] Show tags/genres reference")
    print("  [8] Show languages reference")
    print("  [9] Open Radio Browser website in browser")

    print("\n" + "-" * 65)
    print("  [0] Exit")
    print("=" * 65)


def show_country_codes():
    """Display country codes reference."""
    print("\n" + "=" * 65)
    print("  COUNTRY CODES REFERENCE (ISO 3166-1 alpha-2)")
    print("=" * 65)
    print("\n  Common country codes for Radio Browser API:\n")

    codes = list(COMMON_COUNTRY_CODES.items())
    col_width = 30
    for i in range(0, len(codes), 2):
        left = f"  {codes[i][0]:4} = {codes[i][1]}"
        right = f"  {codes[i + 1][0]:4} = {codes[i + 1][1]}" if i + 1 < len(codes) else ""
        print(f"{left:<{col_width}}{right}")

    print("\n" + "-" * 65)
    print("  💡 TIP: Visit Radio Browser for the complete list:")
    print(f"     {RADIO_BROWSER_COUNTRIES_URL}")
    print("-" * 65)

    if prompt_yes_no("\n  Open Radio Browser countries page in browser?", default_yes=False):
        open_browser(RADIO_BROWSER_COUNTRIES_URL)


def show_tags():
    """Display tags/genres reference."""
    print("\n" + "=" * 65)
    print("  TAGS / GENRES REFERENCE")
    print("=" * 65)
    print("\n  Common tags for Radio Browser API:\n")

    col_width = 20
    cols = 3
    for i in range(0, len(COMMON_TAGS), cols):
        row = COMMON_TAGS[i:i + cols]
        print("  " + "".join(f"{tag:<{col_width}}" for tag in row))

    print("\n" + "-" * 65)
    print("  💡 TIP: Tags are case-insensitive. You can also combine them.")
    print(f"     Visit Radio Browser for all available tags:")
    print(f"     {RADIO_BROWSER_TAGS_URL}")
    print("-" * 65)

    if prompt_yes_no("\n  Open Radio Browser tags page in browser?", default_yes=False):
        open_browser(RADIO_BROWSER_TAGS_URL)


def show_languages():
    """Display languages reference."""
    print("\n" + "=" * 65)
    print("  LANGUAGES REFERENCE")
    print("=" * 65)
    print("\n  Common languages for Radio Browser API:\n")

    col_width = 20
    cols = 3
    for i in range(0, len(COMMON_LANGUAGES), cols):
        row = COMMON_LANGUAGES[i:i + cols]
        print("  " + "".join(f"{lang:<{col_width}}" for lang in row))

    print("\n" + "-" * 65)
    print("  💡 TIP: Languages are case-insensitive.")
    print(f"     Visit Radio Browser for all available languages:")
    print(f"     {RADIO_BROWSER_LANGUAGES_URL}")
    print("-" * 65)

    if prompt_yes_no("\n  Open Radio Browser languages page in browser?", default_yes=False):
        open_browser(RADIO_BROWSER_LANGUAGES_URL)


def show_radio_browser_info():
    """Show Radio Browser website info and offer to open browser."""
    print("\n" + "=" * 65)
    print("  RADIO BROWSER - ONLINE DATABASE")
    print("=" * 65)
    print(f"""
  Radio Browser is a free, community-driven database of internet
  radio stations from around the world.

  🌐 Website:    {RADIO_BROWSER_URL}

  Useful pages:
  ─────────────────────────────────────────────────────────────
  📍 Countries:  {RADIO_BROWSER_COUNTRIES_URL}
     → Find country codes (NL, DE, US, GB, etc.)

  🏷️  Tags:       {RADIO_BROWSER_TAGS_URL}
     → Browse all genres/tags (rock, jazz, news, etc.)

  🗣️  Languages:  {RADIO_BROWSER_LANGUAGES_URL}
     → Find language names (dutch, english, german, etc.)
  ─────────────────────────────────────────────────────────────
""")
    print("=" * 65)

    print("\n  Which page would you like to open?")
    print("  [1] Main page (radio-browser.info)")
    print("  [2] Countries page")
    print("  [3] Tags page")
    print("  [4] Languages page")
    print("  [0] Return to main menu")

    sub_choice = input("\n  Enter choice (0-4): ").strip()

    if sub_choice == "1":
        open_browser(RADIO_BROWSER_URL)
    elif sub_choice == "2":
        open_browser(RADIO_BROWSER_COUNTRIES_URL)
    elif sub_choice == "3":
        open_browser(RADIO_BROWSER_TAGS_URL)
    elif sub_choice == "4":
        open_browser(RADIO_BROWSER_LANGUAGES_URL)


# ============================================================
# MAIN
# ============================================================

def main():
    watchdog = Watchdog()
    logger.info("=" * 50)
    logger.info("Scraper started (v29 - pyvips)")
    logger.info(f"SVG support: {'enabled (pyvips)' if SVG_ENABLED else 'disabled'}")
    logger.info("=" * 50)

    while True:
        show_main_menu()
        choice = input("\n  Enter your choice (0-9): ").strip()

        json_data = None

        try:
            # Help/reference options
            if choice == "6":
                show_country_codes()
                continue
            elif choice == "7":
                show_tags()
                continue
            elif choice == "8":
                show_languages()
                continue
            elif choice == "9":
                show_radio_browser_info()
                continue

            if choice == "0":
                print("\n  Exiting...")
                return

            elif choice == "1":
                print("\n  Fetching top 500 stations by popularity...")
                json_data, csv_rows = scrape_via_api("all", None, watchdog)

            elif choice == "2":
                print("\n" + "-" * 65)
                print("  SEARCH BY COUNTRY CODE")
                print(f"  💡 See all codes at: {RADIO_BROWSER_COUNTRIES_URL}")
                print("-" * 65)
                country_code = input("\n  Country code (e.g., NL, DE, US): ").strip().upper()
                if not country_code or len(country_code) != 2:
                    print("  ⚠ Invalid country code.")
                    continue
                json_data, csv_rows = scrape_via_api("country", country_code, watchdog)

            elif choice == "3":
                print("\n" + "-" * 65)
                print("  SEARCH BY TAG / GENRE")
                print(f"  💡 See all tags at: {RADIO_BROWSER_TAGS_URL}")
                print("-" * 65)
                tag = input("\n  Tag/genre (e.g., rock, jazz): ").strip().lower()
                if not tag:
                    continue
                json_data, csv_rows = scrape_via_api("tag", tag, watchdog)

            elif choice == "4":
                print("\n" + "-" * 65)
                print("  SEARCH BY LANGUAGE")
                print(f"  💡 See all languages at: {RADIO_BROWSER_LANGUAGES_URL}")
                print("-" * 65)
                language = input("\n  Language (e.g., dutch, english): ").strip().lower()
                if not language:
                    continue
                json_data, csv_rows = scrape_via_api("language", language, watchdog)

            elif choice == "5":
                name = input("\n  Station name to search: ").strip()
                if not name:
                    continue
                json_data, csv_rows = scrape_via_api("name", name, watchdog)

            else:
                print("\n  Invalid choice.")
                continue

            # Process results
            if not json_data or not json_data.get("stations"):
                print("\n  ⚠ No stations found!")
                watchdog.finish()
                continue

            print(f"\n  Found {len(json_data['stations'])} stations")

            # Handle existing data
            if JSON_OUT.exists():
                print("\n  Existing data found. [1] Overwrite [2] Merge [3] Cancel")
                save_choice = input("  Choice: ").strip()
                if save_choice == "2":
                    try:
                        with open(JSON_OUT, "r", encoding="utf-8") as f:
                            existing = json.load(f)
                        existing_urls = {s.get("station") for s in existing.get("stations", [])}
                        new_unique = [s for s in json_data["stations"] if s.get("station") not in existing_urls]
                        max_id = max((s.get("id", 0) for s in existing.get("stations", [])), default=499)
                        for i, s in enumerate(new_unique, 1):
                            s["id"] = max_id + i
                        json_data["stations"] = existing.get("stations", []) + new_unique
                        print(f"  Added {len(new_unique)} new stations")
                    except Exception as e:
                        print(f"  ⚠ Error: {e}")
                elif save_choice == "3":
                    continue

            # Save files
            with open(JSON_OUT, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ JSON saved")

            csv_rows = [{"id": s["id"], "station": s["name"], "stream_url": s["station"], "logo": s.get("logo", "")}
                        for s in json_data["stations"]]
            with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "station", "stream_url", "logo"])
                writer.writeheader()
                writer.writerows(csv_rows)
            print(f"  ✓ CSV saved")

            # ZIP option
            if input("\n  Create ZIP? (y/n): ").strip().lower() == 'y':
                if create_moode_zip(json_data):
                    verify_moode_zip()

            watchdog.finish()

            if not prompt_yes_no("\n  Run another scrape?", default_yes=False):
                break

        except KeyboardInterrupt:
            print("\n\n  Interrupted!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            traceback.print_exc()
            watchdog.finish()
            break


if __name__ == "__main__":
    main()
