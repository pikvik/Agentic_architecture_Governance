#!/usr/bin/env python3
"""
End-to-End Test Script for Agentic AI Swarm
Tests the connection between frontend and backend
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

async def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing Backend Health...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/health") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Backend Health: {data}")
                return True
            else:
                print(f"❌ Backend Health Failed: {response.status}")
                return False

async def test_swarm_status():
    """Test swarm status endpoint"""
    print("\n🔍 Testing Swarm Status...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/swarm/status") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Swarm Status: {data['overall_health']}% health, {data['total_agents']} agents")
                return True
            else:
                print(f"❌ Swarm Status Failed: {response.status}")
                return False

async def test_agents_list():
    """Test agents list endpoint"""
    print("\n🔍 Testing Agents List...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/agents") as response:
            if response.status == 200:
                data = await response.json()
                agents = data['agents']
                print(f"✅ Found {len(agents)} agents:")
                for name, agent in agents.items():
                    print(f"   - {agent['name']}: {agent['status']} (Health: {agent['health_score']}%)")
                return True
            else:
                print(f"❌ Agents List Failed: {response.status}")
                return False

async def test_agent_control():
    """Test agent control endpoints"""
    print("\n🔍 Testing Agent Control...")
    async with aiohttp.ClientSession() as session:
        # Get first agent ID
        async with session.get(f"{BACKEND_URL}/agents") as response:
            if response.status == 200:
                data = await response.json()
                agents = data['agents']
                first_agent_id = list(agents.values())[0]['agent_id']
                
                # Test start
                async with session.post(f"{BACKEND_URL}/agents/{first_agent_id}/start") as start_response:
                    if start_response.status == 200:
                        print(f"✅ Agent Start: Success")
                    else:
                        print(f"❌ Agent Start Failed: {start_response.status}")
                
                # Test restart
                async with session.post(f"{BACKEND_URL}/agents/{first_agent_id}/restart") as restart_response:
                    if restart_response.status == 200:
                        print(f"✅ Agent Restart: Success")
                    else:
                        print(f"❌ Agent Restart Failed: {restart_response.status}")
                
                return True
            else:
                print(f"❌ Cannot get agents for control test: {response.status}")
                return False

async def test_governance_validation():
    """Test governance validation endpoint"""
    print("\n🔍 Testing Governance Validation...")
    
    # Create a test request
    test_request = {
        "request_id": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "scope": "comprehensive",
        "target_components": ["api_gateway", "user_service"],
        "business_context": {
            "industry": "technology",
            "scale": "enterprise"
        },
        "technical_context": {
            "platform": "cloud-native",
            "architecture": "microservices"
        },
        "compliance_requirements": ["ISO_27001", "GDPR"],
        "priority": "high",
        "timeout_seconds": 300
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/governance/validate",
            json=test_request,
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Governance Validation: Success")
                print(f"   Status: {data.get('status', 'N/A')}")
                print(f"   Risk Score: {data.get('risk_score', 'N/A')}")
                return True
            else:
                error_text = await response.text()
                print(f"❌ Governance Validation Failed: {response.status}")
                print(f"   Error: {error_text}")
                return False

async def test_frontend_connection():
    """Test frontend connection"""
    print("\n🔍 Testing Frontend Connection...")
    async with aiohttp.ClientSession() as session:
        async with session.get(FRONTEND_URL) as response:
            if response.status == 200:
                print(f"✅ Frontend: Accessible at {FRONTEND_URL}")
                return True
            else:
                print(f"❌ Frontend Connection Failed: {response.status}")
                return False

async def main():
    """Run all tests"""
    print("🚀 Starting End-to-End Tests for Agentic AI Swarm")
    print("=" * 60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Swarm Status", test_swarm_status),
        ("Agents List", test_agents_list),
        ("Agent Control", test_agent_control),
        ("Governance Validation", test_governance_validation),
        ("Frontend Connection", test_frontend_connection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} Test Exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working end-to-end.")
    else:
        print("⚠️  Some tests failed. Please check the system configuration.")
    
    print("\n🌐 Access URLs:")
    print(f"   Frontend: {FRONTEND_URL}")
    print(f"   Backend API: {BACKEND_URL}")
    print(f"   API Docs: {BACKEND_URL}/docs")

if __name__ == "__main__":
    asyncio.run(main())
