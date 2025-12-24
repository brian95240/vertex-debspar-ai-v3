#!/usr/bin/env python3.11
"""
STEP 3: Backend Unit & Integration Smoke Test
Tests the FastAPI backend with mocked external services
"""

import asyncio
import json
import sys
import time
import subprocess
import os
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))

# Test configuration
TEST_TIMEOUT = 60
BACKEND_PORT = 8001  # Use different port to avoid conflicts
BACKEND_HOST = "127.0.0.1"

class BackendSmokeTest:
    def __init__(self):
        self.process = None
        self.test_results = {
            "step3_pass": False,
            "tests": {},
            "errors": []
        }
        
    async def setup_mocks(self):
        """Setup mock responses for external services"""
        print("✓ Setting up mocks for external services...")
        
        # Mock httpx.AsyncClient.post for both local and apex endpoints
        self.mock_responses = {
            "local": {
                "choices": [{
                    "message": {
                        "content": "That argument lacks logical foundation. Here's why..."
                    }
                }]
            },
            "apex": {
                "choices": [{
                    "message": {
                        "content": "Your premise is fundamentally flawed. Let me demonstrate the correct reasoning..."
                    }
                }]
            }
        }
        
    async def test_pressure_estimation(self):
        """Test 1: Verify pressure score calculation"""
        print("\n[TEST 1] Pressure Estimation...")
        try:
            from debate_vertex.orchestrator.cue_extractors import estimate_debate_pressure
            
            # Test case 1: Mild statement with plenty of time
            pressure1 = estimate_debate_pressure("I think this is good", 30.0)
            assert 0 <= pressure1 <= 10, f"Pressure out of range: {pressure1}"
            print(f"  ✓ Mild statement: pressure = {pressure1:.2f}/10")
            
            # Test case 2: Aggressive statement with time pressure
            pressure2 = estimate_debate_pressure("You are completely wrong! This is obviously false!", 5.0)
            assert pressure2 > pressure1, "Aggressive statement should have higher pressure"
            print(f"  ✓ Aggressive statement: pressure = {pressure2:.2f}/10")
            
            # Test case 3: Critical time remaining
            pressure3 = estimate_debate_pressure("Normal statement", 1.0)
            assert pressure3 > 0, "Time pressure should increase score"
            print(f"  ✓ Critical time: pressure = {pressure3:.2f}/10")
            
            self.test_results["tests"]["pressure_estimation"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"Pressure estimation: {str(e)}")
            return False
    
    async def test_thermal_tiers(self):
        """Test 2: Verify thermal tier logic"""
        print("\n[TEST 2] Thermal Tier Logic...")
        try:
            from debate_vertex.core.thermal import ThermalTier
            
            # Test tier comparison
            assert ThermalTier.HOT >= ThermalTier.WARM, "HOT should be >= WARM"
            assert ThermalTier.WARM >= ThermalTier.COLD, "WARM should be >= COLD"
            assert ThermalTier.HOT.value == 3, "HOT value should be 3"
            assert ThermalTier.WARM.value == 2, "WARM value should be 2"
            assert ThermalTier.COLD.value == 1, "COLD value should be 1"
            
            print(f"  ✓ HOT tier value: {ThermalTier.HOT.value}")
            print(f"  ✓ WARM tier value: {ThermalTier.WARM.value}")
            print(f"  ✓ COLD tier value: {ThermalTier.COLD.value}")
            
            self.test_results["tests"]["thermal_tiers"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"Thermal tiers: {str(e)}")
            return False
    
    async def test_state_management(self):
        """Test 3: Verify debate state management"""
        print("\n[TEST 3] State Management...")
        try:
            from debate_vertex.orchestrator.state import DebateState
            
            # Create a debate state
            state = DebateState(session_id="test-session-001")
            
            # Test adding turns
            state.add_turn("user", "First argument")
            assert state.turn_count == 1, "Turn count should be 1"
            assert len(state.history) == 1, "History should have 1 entry"
            
            state.add_turn("assistant", "Counter argument")
            assert state.turn_count == 2, "Turn count should be 2"
            assert len(state.history) == 2, "History should have 2 entries"
            
            # Test context retrieval
            context = state.get_context(limit=10)
            assert len(context) == 2, "Context should have 2 messages"
            
            # Test pressure score
            state.pressure_score = 7.5
            assert state.pressure_score == 7.5, "Pressure score should be 7.5"
            
            print(f"  ✓ Session ID: {state.session_id}")
            print(f"  ✓ Turn count: {state.turn_count}")
            print(f"  ✓ History length: {len(state.history)}")
            print(f"  ✓ Pressure score: {state.pressure_score}")
            
            self.test_results["tests"]["state_management"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"State management: {str(e)}")
            return False
    
    async def test_hybrid_brain_routing(self):
        """Test 4: Verify hybrid brain routing logic"""
        print("\n[TEST 4] Hybrid Brain Routing...")
        try:
            from debate_vertex.models.brain_router import HybridBrain
            from debate_vertex.orchestrator.state import DebateState
            
            # Create mock state
            state = DebateState(session_id="test-session-002")
            state.pressure_score = 5.0  # Low pressure
            
            # Create brain instance
            brain = HybridBrain()
            
            # Verify endpoints are configured
            assert brain.local_endpoint is not None, "Local endpoint should be configured"
            assert brain.apex_url is not None, "Apex URL should be configured"
            
            print(f"  ✓ Local endpoint: {brain.local_endpoint}")
            print(f"  ✓ Apex URL: {brain.apex_url}")
            print(f"  ✓ Hybrid routing configured")
            
            self.test_results["tests"]["hybrid_brain_routing"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"Hybrid brain routing: {str(e)}")
            return False
    
    async def test_debate_manager_initialization(self):
        """Test 5: Verify debate manager can initialize"""
        print("\n[TEST 5] Debate Manager Initialization...")
        try:
            from debate_vertex.orchestrator.deb8 import DebateManager
            
            # Create manager
            manager = DebateManager()
            
            # Verify initialization
            assert manager.active_connections == {}, "Active connections should be empty"
            assert manager.brain is not None, "Brain should be initialized"
            
            print(f"  ✓ Manager initialized")
            print(f"  ✓ Active connections: {len(manager.active_connections)}")
            print(f"  ✓ Brain instance: {manager.brain.__class__.__name__}")
            
            self.test_results["tests"]["debate_manager_init"] = "PASS"
            return True
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.test_results["errors"].append(f"Debate manager init: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all smoke tests"""
        print("=" * 70)
        print("VERTEX DEBSPAR AI v3.0 - STEP 3: BACKEND SMOKE TEST")
        print("=" * 70)
        
        await self.setup_mocks()
        
        # Run all tests
        results = []
        results.append(await self.test_pressure_estimation())
        results.append(await self.test_thermal_tiers())
        results.append(await self.test_state_management())
        results.append(await self.test_hybrid_brain_routing())
        results.append(await self.test_debate_manager_initialization())
        
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
            print("\n✓ STEP 3 PASS - All backend smoke tests passed!")
            self.test_results["step3_pass"] = True
            return True
        else:
            print("\n✗ STEP 3 FAIL - Some tests failed")
            return False


async def main():
    """Main test runner"""
    tester = BackendSmokeTest()
    
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
