# Third-Party Licenses

This directory contains the full text of licenses for third-party dependencies used by BiXFlow.

## Overview

BiXFlow is distributed under the MIT License and includes the following third-party libraries, each with their respective licenses:

### MIT License

Most of BiXFlow's dependencies are licensed under the MIT License, which is permissive and compatible with BiXFlow's MIT license.

**Libraries under MIT License:**
- BiXFlow (0.9.0)
- PyJWT (2.11.0)
- PyYAML (6.0.3)
- annotated-types (0.7.0)
- anyio (4.12.1)
- attrs (25.4.0)
- black (26.1.0)
- cffi (2.0.0)
- et_xmlfile (2.0.0)
- flake8 (7.3.0)
- h11 (0.16.0)
- httpx-sse (0.4.3)
- iniconfig (2.3.0)
- jsonschema (4.26.0)
- jsonschema-specifications (2025.9.1)
- mccabe (0.7.0)
- mcp (1.26.0)
- mypy_extensions (1.1.0)
- openpyxl (3.1.5)
- platformdirs (4.5.1)
- pluggy (1.6.0)
- pycodestyle (2.14.0)
- pydantic (2.12.5)
- pydantic-settings (2.12.0)
- pydantic_core (2.41.5)
- pyflakes (3.4.0)
- pytest (9.0.2)
- pytokens (0.4.1)
- referencing (0.37.0)
- rpds-py (0.30.0)
- six (1.17.0)
- typing-inspection (0.4.2)

### BSD License (BSD-2-Clause)

BSD-2-Clause is also permissive and compatible with MIT.

**Libraries under BSD License:**
- Jinja2 (3.1.6)
- Pygments (2.19.2)
- colorama (0.4.6)
- httpx (0.28.1)
- pandas (3.0.0)
- python-dateutil (2.9.0.post0)

### BSD-3-Clause

BSD-3-Clause is permissive and compatible with MIT.

**Libraries under BSD-3-Clause:**
- MarkupSafe (3.0.3)
- click (8.3.1)
- httpcore (1.0.9)
- idna (3.11)
- pycparser (3.0)
- python-dotenv (1.2.1)
- sse-starlette (3.2.0)
- starlette (0.52.1)
- uvicorn (0.40.0)

### Mozilla Public License 2.0 (MPL 2.0)

MPL 2.0 is a weak copyleft license that is compatible with MIT for most use cases. It requires that modifications to MPL-licensed files themselves be made available under MPL, but the larger project can remain under MIT.

**Libraries under MPL 2.0:**
- certifi (2026.1.4)
- pathspec (1.0.4)

### Apache-2.0 OR BSD-3-Clause

These libraries offer a choice between Apache-2.0 and BSD-3-Clause. Both are compatible with MIT.

**Libraries under Apache-2.0 OR BSD-3-Clause:**
- cryptography (46.0.4)

### Apache-2.0 OR BSD-2-Clause

These libraries offer a choice between Apache-2.0 and BSD-2-Clause. Both are compatible with MIT.

**Libraries under Apache-2.0 OR BSD-2-Clause:**
- packaging (26.0)

### Apache-2.0

Apache-2.0 is permissive and compatible with MIT.

**Libraries under Apache-2.0:**
- pytest-asyncio (1.3.0)
- python-multipart (0.0.22)
- tzdata (2025.3)

### BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0

NumPy uses a permissive license that offers multiple licensing options. All options are compatible with MIT.

**Libraries under Multiple Permissive Licenses:**
- numpy (2.4.2)

### Python Software Foundation License

The Python Software Foundation License is compatible with MIT and is one of the most permissive licenses.

**Libraries under Python Software Foundation License:**
- pywin32 (311)

### PSF-2.0

PSF-2.0 is compatible with MIT and is used for Python-related utilities.

**Libraries under PSF-2.0:**
- typing_extensions (4.15.0)

## License Compatibility

All third-party dependencies used in BiXFlow are compatible with the MIT License under which BiXFlow is distributed. The licensing strategy follows these principles:

1. **Permissive Licenses Only**: All dependencies use permissive licenses (MIT, BSD variants, Apache-2.0, MPL 2.0) that allow commercial use and distribution
2. **No Copyleft Conflicts**: No strong copyleft licenses (GPL, AGPL) are used, ensuring no viral licensing effects
3. **MIT Compatibility**: All licenses are compatible with BiXFlow's MIT license
4. **Clear Attribution**: All dependencies are properly attributed in the NOTICE file

## Obtaining Full License Texts

The full text of these licenses can be obtained from:

- **MIT License**: https://opensource.org/licenses/MIT
- **BSD-2-Clause**: https://opensource.org/licenses/BSD-2-Clause
- **BSD-3-Clause**: https://opensource.org/licenses/BSD-3-Clause
- **MPL 2.0**: https://opensource.org/licenses/MPL-2.0
- **Apache-2.0**: https://opensource.org/licenses/Apache-2.0
- **Python Software Foundation License**: https://docs.python.org/3/license.html
- **PSF-2.0**: https://opensource.org/license/psf-2-0

## Legal Notice

This project includes software from third parties. Their respective copyright notices and license terms are included for informational purposes. Users of BiXFlow must comply with all applicable license terms for both BiXFlow and its third-party dependencies.

For questions about licensing, please contact: bixing_support@chinamobile.com

## Updating Licenses

To update this document when dependencies change:

1. Run `pip-licenses --format=json > licenses.json`
2. Update the NOTICE file with new dependencies
3. Update this README.md with any new license types
4. Add full license texts to this directory if needed
