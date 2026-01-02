# MoodeRadioBuilder

A Python tool for building internet radio station collections compatible with [moOde Audio Player](https://moodeaudio.org/).

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

## Overview

MoodeRadioBuilder fetches radio station data from the [Radio Browser API](https://www.radio-browser.info/), downloads and processes station logos, and packages everything into a ZIP file that can be directly imported into moOde Audio Player using its built-in backup/restore functionality.

### What It Does

1. **Fetches Station Data** - Queries the Radio Browser community database (30,000+ stations worldwide)
2. **Downloads & Converts Logos** - Processes station artwork to moOde-compatible JPG format with thumbnails
3. **Creates Playlist Files** - Generates `.pls` files for each station
4. **Builds Import Package** - Creates a `moode_radio_backup.zip` ready for moOde import

### Search Options

- **By Country** - ISO 3166-1 alpha-2 codes (NL, DE, US, GB, etc.)
- **By Genre/Tag** - rock, jazz, classical, news, etc.
- **By Language** - dutch, english, german, french, etc.
- **By Station Name** - Search for specific stations
- **Top Stations** - Most popular stations globally

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. Clone the repository
2. Navigate to the project directory
3. Run `python moode_radio_builder.py` (packages install automatically on first run)

### Dependencies

The following packages are **automatically installed** on first run:

| Package | Purpose | License |
|---------|---------|---------|
| [requests](https://pypi.org/project/requests/) | HTTP requests | Apache 2.0 |
| [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) | HTML parsing | MIT |
| [Pillow](https://pypi.org/project/Pillow/) | Image processing | HPND |

### Optional: SVG Support

For stations with SVG logos, install [PyVips](https://pypi.org/project/pyvips/) (LGPL 2.1+):

| Platform | Installation |
|----------|--------------|
| **Windows** | `pip install pyvips` (downloads DLLs automatically) |
| **macOS** | `brew install vips` then `pip install pyvips` |
| **Linux (Debian/Ubuntu)** | `sudo apt-get install libvips-dev` then `pip install pyvips` |
| **Linux (Fedora)** | `sudo dnf install vips-devel` then `pip install pyvips` |

> **Note:** The tool works without SVG support—stations with SVG logos will simply not have logo images.

## Usage

Run the script and follow the interactive menu to:
1. Select a search method (country, genre, language, etc.)
2. Enter search criteria
3. Wait for stations to be processed
4. Optionally create the moOde backup ZIP

## Output Files

| File | Description |
|------|-------------|
| `moode_radio_backup.zip` | **Import this into moOde** via System → Backup/Restore |
| `station_data.json` | Station metadata |
| `radiostreams.csv` | Simple CSV export |
| `RADIO/` | Directory with `.pls` playlist files |
| `radio-logos/` | Station logos (335×335 JPG) |
| `radio-logos/thumbs/` | Thumbnails (80×80 JPG) |

## moOde Import Instructions

1. Run MoodeRadioBuilder and create the ZIP file
2. In moOde web interface: **System → Backup/Restore → Restore**
3. Select the ZIP file and restore
4. Your stations appear in the Radio section

## Data Sources & Attribution

### Radio Browser API

This tool uses the [Radio Browser](https://www.radio-browser.info/) community database.

- **Website:** https://www.radio-browser.info/
- **API Documentation:** https://de1.api.radio-browser.info/
- **License:** The Radio Browser database is community-maintained and freely accessible
- **Attribution:** Station data provided by [Radio Browser](https://www.radio-browser.info/)

### moOde Audio Player

- **Website:** https://moodeaudio.org/
- **License:** GPLv3
- **GitHub:** https://github.com/moode-player/moode

## Configuration

The following settings can be adjusted in the script:

| Setting | Default | Description |
|---------|---------|-------------|
| `STATION_TIMEOUT` | 60s | Max time per station before skip |
| `REQUEST_TIMEOUT` | 15s | HTTP request timeout |
| `LOGO_TIMEOUT` | 30s | Logo download timeout |
| `REQUEST_DELAY` | 0.3s | Delay between API requests |

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "All API servers failed" | Check internet connection; Radio Browser may be temporarily unavailable |
| SVG logos not converting | Install libvips (see Optional: SVG Support) |
| ZIP import fails in moOde | Ensure ZIP structure matches expected format; check moOde version compatibility |

### Logs & Reports

- `scraper.log` - Detailed operation log
- `run_summary.json` - Statistics from last run
- `error_report.json` - Detailed error information

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## Third-Party Licenses

This project uses the following open-source packages:

| Package | License | Link |
|---------|---------|------|
| requests | Apache 2.0 | [License](https://github.com/psf/requests/blob/main/LICENSE) |
| beautifulsoup4 | MIT | [License](https://www.crummy.com/software/BeautifulSoup/) |
| Pillow | HPND | [License](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| pyvips (optional) | LGPL 2.1+ | [License](https://github.com/libvips/pyvips/blob/master/LICENSE.txt) |
| libvips (optional) | LGPL 2.1+ | [License](https://github.com/libvips/libvips/blob/master/LICENSE) |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Acknowledgments

- [Radio Browser](https://www.radio-browser.info/) - Community radio station database
- [moOde Audio](https://moodeaudio.org/) - Audiophile-quality music playback for Raspberry Pi
- All the open-source package maintainers

## Disclaimer

This tool is provided for personal use. Radio streams are provided by third parties and may be subject to geographic restrictions or usage terms. Users are responsible for ensuring compliance with applicable laws and terms of service.

---

**Note:** This project is not affiliated with or endorsed by moOde Audio or Radio Browser.
