#!/usr/bin/env python3
"""Script to run FutureHouse MCP battle integration tests.

This script runs the integration tests that make real API calls to FutureHouse.
Requires FUTUREHOUSE_API_KEY environment variable or .env file.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    """Run the battle integration tests."""
    # Check if API key is available
    api_key = os.getenv("FUTUREHOUSE_API_KEY")
    if not api_key:
        print("❌ ERROR: FUTUREHOUSE_API_KEY not found!")
        print("Set your API key before running battle tests:")
        print("Option 1: Create .env file with: FUTUREHOUSE_API_KEY=your_api_key_here")
        print("Option 2: Export environment variable: export FUTUREHOUSE_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    print("🧪 Starting FutureHouse MCP Battle Integration Tests...")
    print(f"Using API key: {api_key[:8]}..." if len(api_key) > 8 else "Using provided API key")
    print("-" * 60)
    
    # Run integration tests
    cmd = [
        "python3", "-m", "pytest",
        "test/test_battle_integration.py",
        "-v",
        "-m", "integration",
        "--tb=short",
        "-s"  # Don't capture output so we can see the battle test prints
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print("\n🎯 ALL BATTLE TESTS PASSED!")
        else:
            print(f"\n❌ Some battle tests failed (exit code: {result.returncode})")
        return result.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Battle tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error running battle tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 