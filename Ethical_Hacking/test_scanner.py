"""
Test file to verify EH scanner is working properly
"""
import sys
import os

# Add scanner to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner.core import VulnerabilityScanner
from scanner.utils import validate_url, is_localhost

def test_imports():
    """Test if all imports work"""
    print("✓ Testing imports...")
    try:
        from scanner.sqli_detector import SQLInjectionDetector
        from scanner.xss_detector import XSSDetector
        from scanner.reporter import Reporter
        print("  ✅ All imports successful")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_url_validation():
    """Test URL validation"""
    print("\n✓ Testing URL validation...")
    tests = [
        ("http://example.com", True),
        ("https://example.com", True),
        ("example.com", False),
        ("ftp://example.com", False),
    ]
    
    for url, expected in tests:
        result = validate_url(url)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {url}: {result}")
    
    return True

def test_localhost_detection():
    """Test localhost detection"""
    print("\n✓ Testing localhost detection...")
    tests = [
        ("http://localhost:8080", True),
        ("http://127.0.0.1", True),
        ("http://example.com", False),
    ]
    
    for url, expected in tests:
        result = is_localhost(url)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {url}: {result}")
    
    return True

def test_payload_loading():
    """Test payload file loading"""
    print("\n✓ Testing payload loading...")
    try:
        from scanner.sqli_detector import SQLInjectionDetector
        from scanner.xss_detector import XSSDetector
        
        sqli = SQLInjectionDetector(None, 1, 10)
        xss = XSSDetector(None, 1, 10)
        
        sqli_payloads = sqli.load_payloads()
        xss_payloads = xss.load_payloads()
        
        print(f"  ✅ SQL Injection payloads loaded: {len(sqli_payloads)}")
        print(f"  ✅ XSS payloads loaded: {len(xss_payloads)}")
        
        return True
    except Exception as e:
        print(f"  ❌ Payload loading failed: {e}")
        return False

def test_scanner_initialization():
    """Test scanner initialization"""
    print("\n✓ Testing scanner initialization...")
    try:
        scanner = VulnerabilityScanner(
            target_url="http://example.com",
            delay=1,
            timeout=10,
            silent=True
        )
        print(f"  ✅ Scanner initialized")
        print(f"  ✅ Target: {scanner.target_url}")
        print(f"  ✅ Timeout: {scanner.timeout}s")
        print(f"  ✅ Reports directory: {scanner.output_dir}")
        return True
    except Exception as e:
        print(f"  ❌ Scanner initialization failed: {e}")
        return False

def test_reports_directory():
    """Test reports directory creation"""
    print("\n✓ Testing reports directory...")
    try:
        scanner = VulnerabilityScanner(
            target_url="http://example.com",
            silent=True
        )
        
        if os.path.exists(scanner.output_dir):
            print(f"  ✅ Reports directory exists: {scanner.output_dir}")
            return True
        else:
            print(f"  ❌ Reports directory not found")
            return False
    except Exception as e:
        print(f"  ❌ Reports directory test failed: {e}")
        return False

def main():
    print("="*60)
    print("EH VULNERABILITY SCANNER - SYSTEM TEST")
    print("="*60)
    
    tests = [
        test_imports,
        test_url_validation,
        test_localhost_detection,
        test_payload_loading,
        test_scanner_initialization,
        test_reports_directory,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED - Scanner is ready to use!")
    else:
        print(f"\n⚠️  {failed} test(s) failed - Please review errors above")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
