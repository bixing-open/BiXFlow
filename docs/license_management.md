# License Management Guide

This guide explains how to manage and update license information for BiXFlow, ensuring compliance with all third-party license requirements.

## Overview

BiXFlow is distributed under the MIT License and uses various third-party libraries. Proper license management is essential for:

1. **Legal Compliance**: Ensuring all dependencies are properly attributed
2. **Transparency**: Providing clear information about third-party licenses
3. **Compatibility**: Verifying that all licenses are compatible with MIT
4. **Best Practices**: Following open-source licensing standards

## License Files Structure

```
BiXFlow/
├── LICENSE                    # BiXFlow's MIT License
├── NOTICE                     # Third-party attribution notice
├── licenses.json              # Generated license report (in .gitignore)
├── third-party-licenses/      # Third-party license documentation
│   └── README.md             # Detailed license information
├── docs/
│   └── license_management.md # This file
└── scripts/
    └── license_check.py      # License compliance checker
```

## Updating License Information

### When to Update

Update license information when:

1. **Adding New Dependencies**: When adding new packages to requirements.txt
2. **Updating Dependencies**: When upgrading package versions
3. **Removing Dependencies**: When removing packages from requirements.txt
4. **Regular Review**: At least once per release cycle

### Update Process

#### Step 1: Generate License Report

Use `pip-licenses` to generate a machine-readable license report:

```bash
# Install pip-licenses if not already installed
pip install pip-licenses

# Generate licenses.json in the project root
pip-licenses --format=json > licenses.json
```

#### Step 2: Run License Compliance Check

Use the provided script to verify license compatibility:

```bash
# Run the license checker
python scripts/license_check.py

# Run with notice file generation
python scripts/license_check.py --generate-notice
```

The script will:

- Check all dependencies for MIT compatibility
- Identify any copyleft or incompatible licenses
- Generate a summary report
- Optionally regenerate the NOTICE file

#### Step 3: Review Results

The license checker will output:

```
======================================================================
BiXFlow License Compliance Check
======================================================================

BiXFlow License: MIT License
Total Dependencies: 54

Analyzing dependencies...
----------------------------------------------------------------------
✓ BiXFlow                         MIT License
✓ Jinja2                          BSD License
⊘ certifi                         Mozilla Public License 2.0 (MPL 2.0)
✓ click                           BSD-3-Clause
...

----------------------------------------------------------------------
Summary:
  Compatible (MIT/BSD/Apache):  50
  Weak Copyleft (MPL 2.0):       2
  Unknown/Unrecognized:          0
  Incompatible:                  0

======================================================================
✓ LICENSE COMPLIANCE CHECK PASSED
======================================================================
```

#### Step 4: Update Documentation

If licenses.json changed:

1. **Update NOTICE file** (if using `--generate-notice`, this is done automatically)
2. **Update third-party-licenses/README.md** with any new license types
3. **Update README_en.md** if the license summary changed
4. **Review changes** to ensure accuracy

#### Step 5: Commit Changes

```bash
# Add updated license files
git add NOTICE third-party-licenses/README.md README_en.md

# Commit with a clear message
git commit -m "docs: update license information for [version]

- Updated NOTICE with new third-party dependencies
- Updated third-party-licenses/README.md
- All dependencies verified as MIT-compatible"
```

## License Categories

### Permissive Licenses (No Issues)

These licenses are fully compatible with MIT and require no special handling:

- **MIT License**: Most common, fully compatible
- **BSD-2-Clause**: Compatible, requires attribution
- **BSD-3-Clause**: Compatible, requires attribution
- **Apache-2.0**: Compatible, includes patent grant

### Weak Copyleft Licenses (Requires Attention)

These licenses are compatible but require special handling:

- **MPL 2.0**: 
  - Modifications to MPL files must remain under MPL
  - Larger project can remain under MIT
  - Must track which files are under MPL
  - Common in: `certifi`, `pathspec`

### Incompatible Licenses (Not Allowed)

These licenses are **NOT** compatible and must **NOT** be used:

- **GPL**: Strong copyleft, incompatible with MIT
- **AGPL**: Strong copyleft with network use, incompatible
- **LGPL**: Weak copyleft but complex, avoid

## Adding New Dependencies

When adding a new dependency:

1. **Check License First**: Before adding, verify the license is compatible
2. **Run License Check**: After installing, run `python scripts/license_check.py`
3. **Update Documentation**: Update license files if check passes
4. **Review Impact**: Understand if the license has any special requirements

### Example: Adding a New Dependency

```bash
# 1. Research the license (e.g., on PyPI or GitHub)
# 2. Install the package
pip install new-package

# 3. Generate updated license report
pip-licenses --format=json > licenses.json

# 4. Run license check
python scripts/license_check.py

# 5. If check passes, update documentation
python scripts/license_check.py --generate-notice

# 6. Commit changes
git add NOTICE third-party-licenses/README.md
git commit -m "docs: update licenses for new-package"
```

## Automated License Checking

### Pre-commit Hook

Consider adding a pre-commit hook to check licenses automatically:

```bash
# Create .git/hooks/pre-commit
#!/bin/bash
python scripts/license_check.py
if [ $? -ne 0 ]; then
    echo "❌ License compliance check failed. Please fix before committing."
    exit 1
fi
```

### CI/CD Integration

Add license checking to your CI/CD pipeline:

```yaml
# .github/workflows/license-check.yml
name: License Compliance Check

on: [push, pull_request]

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - run: pip install pip-licenses
      - run: pip-licenses --format=json > licenses.json
      - run: python scripts/license_check.py
```

## Legal Considerations

### Attribution Requirements

Ensure proper attribution for all third-party software:

1. **NOTICE File**: Contains attribution for all dependencies
2. **README**: Mentions third-party licenses
3. **Package Metadata**: Include license information in setup.py
4. **Distribution**: Include license files in package distribution

### Copyleft Handling

For MPL 2.0 dependencies:

1. **Track Files**: Know which files are under MPL
2. **Keep Separate**: Don't mix MPL and MIT code in same files
3. **Document**: Clearly document MPL files in comments
4. **Comply**: Ensure modifications to MPL files remain under MPL

### Commercial Use

All current licenses allow commercial use:

- ✅ Can be used in commercial products
- ✅ Can be distributed commercially
- ✅ No attribution fees
- ✅ No copyleft viral effects

## Troubleshooting

### License Check Fails

If the license check fails:

1. **Review Issues**: Check which dependencies have problems
2. **Investigate**: Look up the actual license on PyPI or GitHub
3. **Update Checker**: If license is compatible but unrecognized, update `COMPATIBLE_LICENSES` in `scripts/license_check.py`
4. **Replace**: If incompatible, find an alternative library

### Unknown Licenses

If a license is marked as unknown:

1. **Verify**: Check the package's license file
2. **Research**: Look up license on SPDX License List
3. **Update**: Add to `COMPATIBLE_LICENSES` if compatible
4. **Document**: Update third-party-licenses/README.md

### MPL 2.0 Warnings

If you see MPL 2.0 warnings:

1. **Review**: Check which dependencies use MPL 2.0
2. **Understand**: Know the requirements (file-level copyleft)
3. **Track**: Keep track of MPL-licensed files
4. **Comply**: Ensure proper handling of MPL files

## Best Practices

1. **Regular Updates**: Check licenses with every release
2. **Automation**: Use automated tools and CI/CD checks
3. **Documentation**: Keep all license files up to date
4. **Review**: Manually review license changes
5. **Transparency**: Be clear about all third-party licenses
6. **Compliance**: Follow all license requirements strictly

## Resources

- **SPDX License List**: https://spdx.org/licenses/
- **Choose a License**: https://choosealicense.com/
- **Open Source Initiative**: https://opensource.org/licenses/
- **pip-licenses Documentation**: https://github.com/raimon49/pip-licenses
- **MIT License**: https://opensource.org/licenses/MIT
- **MPL 2.0 FAQ**: https://www.mozilla.org/en-US/MPL/2.0/FAQ/

## Contact

For questions about licensing or compliance:

- Email: bixing_support@chinamobile.com
- Issues: https://github.com/your-organization/BiXFlow/issues

---

**Last Updated**: 2026-02-10
**Version**: 0.9.0
