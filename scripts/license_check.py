#!/usr/bin/env python3
"""
License Compliance Check Script for BiXFlow

This script analyzes the licenses.json file to verify that all third-party
dependencies are compatible with BiXFlow's MIT License.
"""

import json
import sys
from pathlib import Path


class LicenseChecker:
    """Check license compatibility for BiXFlow dependencies."""
    
    # Compatible license types with BiXFlow's MIT License
    COMPATIBLE_LICENSES = {
        'MIT',
        'MIT License',
        'BSD License',
        'BSD-2-Clause',
        'BSD-3-Clause',
        'Apache-2.0',
        'Apache-2.0 OR BSD-2-Clause',
        'Apache-2.0 OR BSD-3-Clause',
        'Mozilla Public License 2.0 (MPL 2.0)',
        'MPL 2.0',
        'Python Software Foundation License',
        'PSF-2.0',
        'BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0',
        'Apache Software License; BSD License',
    }
    
    # Licenses that require special attention
    COPYLEFT_LICENSES = {
        'MPL 2.0',
        'Mozilla Public License 2.0 (MPL 2.0)',
    }
    
    # Incompatible licenses (strong copyleft)
    INCOMPATIBLE_LICENSES = {
        'GPL',
        'AGPL',
        'LGPL',
        'GPLv2',
        'GPLv3',
        'AGPLv3',
        'LGPLv3',
    }
    
    def __init__(self, licenses_file='licenses.json'):
        """Initialize the license checker.
        
        Args:
            licenses_file: Path to the licenses.json file
        """
        self.licenses_file = Path(licenses_file)
        self.dependencies = []
        self.issues = []
        self.warnings = []
        
    def load_licenses(self):
        """Load license information from JSON file."""
        try:
            # Try UTF-8 first
            with open(self.licenses_file, 'r', encoding='utf-8') as f:
                self.dependencies = json.load(f)
            return True
        except FileNotFoundError:
            print(f"❌ Error: {self.licenses_file} not found.")
            print(f"   Run: pip-licenses --format=json > {self.licenses_file}")
            return False
        except UnicodeDecodeError:
            # Try UTF-16 if UTF-8 fails
            try:
                with open(self.licenses_file, 'r', encoding='utf-16') as f:
                    self.dependencies = json.load(f)
                return True
            except Exception as e:
                print(f"❌ Error: Unable to decode {self.licenses_file}: {e}")
                return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {self.licenses_file}: {e}")
            return False
    
    def check_license_compatibility(self, dep):
        """Check if a dependency's license is compatible with MIT.
        
        Args:
            dep: Dependency dictionary with 'License' and 'Name' keys
            
        Returns:
            tuple: (is_compatible, is_copyleft, is_incompatible)
        """
        license_name = dep.get('License', '').strip()
        dep_name = dep.get('Name', 'Unknown')
        
        # Check for incompatible licenses
        for incompatible in self.INCOMPATIBLE_LICENSES:
            if incompatible in license_name:
                self.issues.append(
                    f"❌ {dep_name}: Uses incompatible license '{license_name}'"
                )
                return (False, False, True)
        
        # Check for copyleft licenses
        for copyleft in self.COPYLEFT_LICENSES:
            if copyleft in license_name:
                self.warnings.append(
                    f"⚠️  {dep_name}: Uses weak copyleft license '{license_name}' - "
                    f"modifications to MPL files must remain under MPL"
                )
                return (True, True, False)
        
        # Check for compatible licenses
        for compatible in self.COMPATIBLE_LICENSES:
            if compatible in license_name:
                return (True, False, False)
        
        # Unknown license
        self.warnings.append(
            f"⚠️  {dep_name}: License '{license_name}' not recognized - "
            f"manual review required"
        )
        return (None, False, False)
    
    def analyze(self):
        """Analyze all dependencies for license compatibility."""
        compatible_count = 0
        copyleft_count = 0
        unknown_count = 0
        incompatible_count = 0
        
        print("\n" + "="*70)
        print("BiXFlow License Compliance Check")
        print("="*70)
        print(f"\nBiXFlow License: MIT License")
        print(f"Total Dependencies: {len(self.dependencies)}")
        print("\nAnalyzing dependencies...")
        print("-"*70)
        
        for dep in self.dependencies:
            is_compatible, is_copyleft, is_incompatible = \
                self.check_license_compatibility(dep)
            
            if is_compatible and not is_copyleft:
                compatible_count += 1
                print(f"✓ {dep['Name']:30s} {dep['License']}")
            elif is_copyleft:
                copyleft_count += 1
                print(f"⊘ {dep['Name']:30s} {dep['License']}")
            elif is_incompatible:
                incompatible_count += 1
            else:
                unknown_count += 1
                print(f"? {dep['Name']:30s} {dep['License']}")
        
        print("-"*70)
        print(f"\nSummary:")
        print(f"  Compatible (MIT/BSD/Apache):  {compatible_count}")
        print(f"  Weak Copyleft (MPL 2.0):       {copyleft_count}")
        print(f"  Unknown/Unrecognized:          {unknown_count}")
        print(f"  Incompatible:                  {incompatible_count}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.issues:
            print("\n❌ Issues Found:")
            for issue in self.issues:
                print(f"  {issue}")
            print("\n" + "="*70)
            print("❌ LICENSE COMPLIANCE CHECK FAILED")
            print("="*70)
            return False
        
        if self.warnings:
            print("\n" + "="*70)
            print("⚠️  LICENSE COMPLIANCE CHECK PASSED WITH WARNINGS")
            print("="*70)
            print("\nRecommendations:")
            print("  1. Review all warnings above")
            print("  2. Ensure MPL-licensed files are properly handled")
            print("  3. Verify unknown licenses manually")
            print("  4. Update COMPATIBLE_LICENSES if needed")
            return True
        
        print("\n" + "="*70)
        print("✓ LICENSE COMPLIANCE CHECK PASSED")
        print("="*70)
        print("\nAll dependencies are compatible with BiXFlow's MIT License.")
        print("The project is ready for distribution.")
        return True
    
    def generate_notice_file(self, output_file='NOTICE'):
        """Generate a NOTICE file based on licenses.json.
        
        Args:
            output_file: Path to output NOTICE file
        """
        # Group dependencies by license
        license_groups = {}
        for dep in self.dependencies:
            license_name = dep.get('License', 'Unknown')
            if license_name not in license_groups:
                license_groups[license_name] = []
            license_groups[license_name].append(dep)
        
        notice_content = """BiXFlow
Copyright (c) 2026 BiXFlow Development Team

This product includes software developed by the following third parties:

"""
        
        # Sort licenses alphabetically
        for license_name in sorted(license_groups.keys()):
            deps = sorted(license_groups[license_name], key=lambda x: x['Name'])
            separator = "=" * 80
            notice_content += f"{separator}\n{license_name}\n{separator}\n"
            for dep in deps:
                name = dep['Name']
                version = dep.get('Version', 'unknown')
                notice_content += f"- {name} ({version})\n"
            notice_content += "\n"
        
        notice_content += """
For detailed license information, please see the LICENSE file and the
third-party-licenses directory.
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(notice_content)
        
        print(f"\n✓ Generated NOTICE file: {output_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Check license compatibility for BiXFlow dependencies'
    )
    parser.add_argument(
        '--licenses-file',
        default='licenses.json',
        help='Path to licenses.json file (default: licenses.json)'
    )
    parser.add_argument(
        '--generate-notice',
        action='store_true',
        help='Generate NOTICE file from licenses.json'
    )
    
    args = parser.parse_args()
    
    checker = LicenseChecker(args.licenses_file)
    
    if not checker.load_licenses():
        sys.exit(1)
    
    success = checker.analyze()
    
    if args.generate_notice:
        checker.generate_notice_file()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
