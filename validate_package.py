#!/usr/bin/env python3
"""
Package Validation Script
Validates that all components of the Bark.com scraper package are working correctly.
"""

import os
import sys
import importlib.util
from pathlib import Path

def print_status(message, status="INFO"):
    """Print formatted status message"""
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def validate_file_structure():
    """Validate that all required files are present"""
    print_status("Validating file structure...")
    
    required_files = [
        "src/bark_scraper.py",
        "src/scraper_cli.py", 
        "src/config.py",
        "src/__init__.py",
        "requirements.txt",
        "setup.sh",
        "README.md",
        "LICENSE",
        "docs/README.md",
        "examples/production_demo.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print_status(f"Missing files: {', '.join(missing_files)}", "ERROR")
        return False
    else:
        print_status("All required files present", "SUCCESS")
        return True

def validate_imports():
    """Validate that core modules can be imported"""
    print_status("Validating Python imports...")
    
    # Add src to path
    sys.path.insert(0, str(Path("src").resolve()))
    
    try:
        import bark_scraper
        import config
        print_status("Core modules import successfully", "SUCCESS")
        return True
    except ImportError as e:
        print_status(f"Import error: {e}", "ERROR")
        return False

def validate_dependencies():
    """Check if required dependencies are available"""
    print_status("Validating dependencies...")
    
    required_packages = [
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"), 
        ("selenium", "selenium"),
        ("pandas", "pandas"),
        ("tqdm", "tqdm"),
        ("lxml", "lxml")
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name.replace("-", "_"))
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print_status(f"Missing packages: {', '.join(missing_packages)}", "WARNING")
        print_status("Run 'pip install -r requirements.txt' to install", "INFO")
        return False
    else:
        print_status("All dependencies available", "SUCCESS")
        return True

def validate_sample_outputs():
    """Check if sample output files exist"""
    print_status("Validating sample outputs...")
    
    output_dir = Path("output")
    if not output_dir.exists():
        print_status("Output directory missing", "ERROR")
        return False
    
    csv_files = list(output_dir.glob("*.csv"))
    if len(csv_files) == 0:
        print_status("No sample CSV files found", "WARNING")
        return False
    
    print_status(f"Found {len(csv_files)} sample output files", "SUCCESS")
    return True

def main():
    """Run all validation checks"""
    print("🔍 Bark.com Scraper Package Validation")
    print("=" * 50)
    
    checks = [
        validate_file_structure,
        validate_imports,
        validate_dependencies,
        validate_sample_outputs
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print_status("Package is ready for production use! 🎉", "SUCCESS")
        return 0
    else:
        print_status("Some issues found. Please review above.", "WARNING")
        return 1

if __name__ == "__main__":
    sys.exit(main())
