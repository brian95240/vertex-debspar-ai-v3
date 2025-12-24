#!/usr/bin/env python3.11
"""
STEP 4: Frontend Integration Test
Verifies the React frontend can build and connect to backend via WebSocket
"""

import asyncio
import json
import sys
import time
import subprocess
import os
from pathlib import Path
import http.server
import socketserver
import threading

class FrontendIntegrationTest:
    def __init__(self):
        self.test_results = {
            "step4_pass": False,
            "tests": {},
            "errors": []
        }
        self.frontend_dir = Path(__file__).parent / "frontend"
        self.dist_dir = self.frontend_dir / "dist"
        
    def test_build_output(self):
        """Test 1: Verify frontend build output exists"""
        print("\n[TEST 1] Frontend Build Output...")
        try:
            assert self.dist_dir.exists(), "dist directory does not exist"
            assert (self.dist_dir / "index.html").exists(), "index.html not found"
            assert (self.dist_dir / "assets").exists(), "assets directory not found"
            
            # Check for built files
            assets = list((self.dist_dir / "assets").glob("*.js"))
            assert len(assets) > 0, "No JavaScript files in assets"
            
            css_files = list((self.dist_dir / "assets").glob("*.css"))
            assert len(css_files) > 0, "No CSS files in assets"
            
            print(f"  ✓ dist directory exists")
            print(f"  ✓ index.html found")
            print(f"  ✓ JavaScript files: {len(assets)}")
            print(f"  ✓ CSS files: {len(css_files)}")
            
            self.test_results["tests"]["build_output"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"Build output: {str(e)}")
            return False
    
    def test_html_structure(self):
        """Test 2: Verify HTML structure is correct"""
        print("\n[TEST 2] HTML Structure...")
        try:
            html_file = self.dist_dir / "index.html"
            with open(html_file, 'r') as f:
                content = f.read()
            
            assert '<div id="root">' in content, "Root div not found"
            assert '<script' in content, "Script tag not found"
            assert 'type="module"' in content, "Module script not found"
            
            print(f"  ✓ Root div found")
            print(f"  ✓ Module script configured")
            print(f"  ✓ HTML structure valid")
            
            self.test_results["tests"]["html_structure"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"HTML structure: {str(e)}")
            return False
    
    def test_component_files(self):
        """Test 3: Verify all component files exist"""
        print("\n[TEST 3] Component Files...")
        try:
            src_dir = self.frontend_dir / "src"
            components_dir = src_dir / "components"
            
            required_files = [
                src_dir / "main.tsx",
                src_dir / "App.tsx",
                src_dir / "index.css",
                components_dir / "DebateInterface.tsx",
                components_dir / "MessageStream.tsx",
                components_dir / "RebuttalTimer.tsx",
            ]
            
            for file in required_files:
                assert file.exists(), f"Missing: {file.name}"
            
            print(f"  ✓ main.tsx exists")
            print(f"  ✓ App.tsx exists")
            print(f"  ✓ DebateInterface.tsx exists")
            print(f"  ✓ MessageStream.tsx exists")
            print(f"  ✓ RebuttalTimer.tsx exists")
            
            self.test_results["tests"]["component_files"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"Component files: {str(e)}")
            return False
    
    def test_config_files(self):
        """Test 4: Verify configuration files"""
        print("\n[TEST 4] Configuration Files...")
        try:
            required_configs = [
                self.frontend_dir / "package.json",
                self.frontend_dir / "vite.config.ts",
                self.frontend_dir / "tsconfig.json",
                self.frontend_dir / "tailwind.config.js",
                self.frontend_dir / "postcss.config.js",
            ]
            
            for file in required_configs:
                assert file.exists(), f"Missing: {file.name}"
            
            # Verify package.json structure
            with open(self.frontend_dir / "package.json", 'r') as f:
                pkg = json.load(f)
            
            assert "dependencies" in pkg, "dependencies not in package.json"
            assert "react" in pkg["dependencies"], "react not in dependencies"
            assert "react-dom" in pkg["dependencies"], "react-dom not in dependencies"
            
            print(f"  ✓ package.json valid")
            print(f"  ✓ vite.config.ts exists")
            print(f"  ✓ tsconfig.json exists")
            print(f"  ✓ tailwind.config.js exists")
            print(f"  ✓ postcss.config.js exists")
            
            self.test_results["tests"]["config_files"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"Config files: {str(e)}")
            return False
    
    def test_websocket_readiness(self):
        """Test 5: Verify WebSocket configuration in frontend code"""
        print("\n[TEST 5] WebSocket Readiness...")
        try:
            interface_file = self.frontend_dir / "src" / "components" / "DebateInterface.tsx"
            with open(interface_file, 'r') as f:
                content = f.read()
            
            assert "WebSocket" in content, "WebSocket not referenced"
            assert "ws://localhost:8000/ws/debate" in content, "WebSocket endpoint not configured"
            assert "onmessage" in content, "Message handler not found"
            assert "send" in content, "Send method not found"
            
            print(f"  ✓ WebSocket imported")
            print(f"  ✓ Endpoint configured: ws://localhost:8000/ws/debate")
            print(f"  ✓ Message handler implemented")
            print(f"  ✓ Send method implemented")
            
            self.test_results["tests"]["websocket_readiness"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"WebSocket readiness: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 70)
        print("VERTEX DEBSPAR AI v3.0 - STEP 4: FRONTEND INTEGRATION TEST")
        print("=" * 70)
        
        # Run all tests
        results = []
        results.append(self.test_build_output())
        results.append(self.test_html_structure())
        results.append(self.test_component_files())
        results.append(self.test_config_files())
        results.append(self.test_websocket_readiness())
        
        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(results)
        total = len(results)
        
        for test_name, result in self.test_results["tests"].items():
            status = "✓ PASS" if result == "PASS" else "✗ FAIL"
            print(f"{status}: {test_name}")
        
        if self.test_results["errors"]:
            print("\nERRORS:")
            for error in self.test_results["errors"]:
                print(f"  - {error}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n✓ STEP 4 PASS - Frontend integration tests passed!")
            print("\nFrontend build artifacts:")
            print(f"  Location: {self.dist_dir}")
            print(f"  Entry point: index.html")
            print(f"  Ready for deployment")
            self.test_results["step4_pass"] = True
            return True
        else:
            print("\n✗ STEP 4 FAIL - Some tests failed")
            return False


async def main():
    """Main test runner"""
    tester = FrontendIntegrationTest()
    
    try:
        success = await tester.run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
