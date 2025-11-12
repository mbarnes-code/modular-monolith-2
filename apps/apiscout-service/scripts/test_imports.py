#!/usr/bin/env python3
"""
Quick verification script to test APIScout imports work correctly
"""

import os
import sys

# Add src directory to path (same as in main scripts)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all main APIScout modules can be imported"""
    try:
        from apiscout.ApiScout import ApiScout
        print("✅ ApiScout import successful")
        
        from apiscout.ApiQR import ApiQR
        print("✅ ApiQR import successful")
        
        from apiscout.FingerprintCrawler import FingerprintCrawler
        print("✅ FingerprintCrawler import successful")
        
        from apiscout.IdaTools import IdaTools
        print("✅ IdaTools import successful")
        
        from apiscout.ApiVector import ApiVector
        print("✅ ApiVector import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing APIScout NX Service imports...")
    if test_imports():
        print("\n🎉 All imports successful! APIScout NX Service is ready.")
        sys.exit(0)
    else:
        print("\n❌ Import test failed. Check your setup.")
        sys.exit(1)