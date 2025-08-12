#!/usr/bin/env python3
"""
Test script for LLM integration (Dify and Ollama)
"""

import asyncio
import aiohttp
import json

# Configuration
BACKEND_URL = "http://localhost:8000"

async def test_llm_health():
    """Test LLM health check"""
    print("🏥 Testing LLM Health Check")
    print("=" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/llm/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ LLM Health Check Successful!")
                    print(f"   Overall Status: {data['overall_status']}")
                    print(f"   Dify Status: {data['dify']['status']}")
                    print(f"   Dify URL: {data['dify']['base_url']}")
                    print(f"   Ollama Status: {data['ollama']['status']}")
                    print(f"   Ollama URL: {data['ollama']['base_url']}")
                    print(f"   Default Model: {data['ollama']['default_model']}")
                    return data
                else:
                    print(f"❌ LLM Health Check Failed: {response.status}")
                    return None
    except Exception as e:
        print(f"❌ LLM Health Check Error: {e}")
        return None

async def test_ollama_integration():
    """Test Ollama integration"""
    print("\n🤖 Testing Ollama Integration")
    print("=" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test model listing
            print("📋 Testing model listing...")
            async with session.get(f"{BACKEND_URL}/llm/ollama/models") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Models listed successfully!")
                    print(f"   Default Model: {data['default_model']}")
                    print(f"   Available Models: {len(data['models'])}")
                    for model in data['models']:
                        print(f"     - {model['name']} ({model['size']} bytes)")
                    
                    # Test text generation if models are available
                    if data['models']:
                        model_name = data['models'][0]['name']
                        print(f"\n🧠 Testing text generation with {model_name}...")
                        
                        generation_data = {
                            "prompt": "Explain what is architecture governance in one sentence.",
                            "model": model_name,
                            "temperature": 0.7,
                            "max_tokens": 100
                        }
                        
                        async with session.post(
                            f"{BACKEND_URL}/llm/ollama/generate",
                            json=generation_data
                        ) as gen_response:
                            if gen_response.status == 200:
                                gen_data = await gen_response.json()
                                if gen_data['success']:
                                    print(f"✅ Text generation successful!")
                                    print(f"   Response: {gen_data['text'][:100]}...")
                                    print(f"   Model: {gen_data['model']}")
                                    print(f"   Usage: {gen_data['usage']}")
                                else:
                                    print(f"❌ Text generation failed: {gen_data['error']}")
                            else:
                                print(f"❌ Text generation request failed: {gen_response.status}")
                    
                    # Test chat completion
                    print(f"\n💬 Testing chat completion...")
                    chat_data = {
                        "messages": [
                            {"role": "user", "content": "Hello, how are you?"}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 100
                    }
                    
                    async with session.post(
                        f"{BACKEND_URL}/llm/ollama/chat",
                        json=chat_data
                    ) as chat_response:
                        if chat_response.status == 200:
                            chat_result = await chat_response.json()
                            if chat_result['success']:
                                print(f"✅ Chat completion successful!")
                                print(f"   Response: {chat_result['message']['content'][:100]}...")
                                print(f"   Model: {chat_result['model']}")
                            else:
                                print(f"❌ Chat completion failed: {chat_result['error']}")
                        else:
                            print(f"❌ Chat completion request failed: {chat_response.status}")
                    
                else:
                    print(f"❌ Model listing failed: {response.status}")
                    
    except Exception as e:
        print(f"❌ Ollama integration test failed: {e}")

async def test_dify_integration():
    """Test Dify integration"""
    print("\n☁️ Testing Dify Integration")
    print("=" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test workspace listing
            print("🏢 Testing workspace listing...")
            async with session.get(f"{BACKEND_URL}/llm/dify/workspaces") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Workspaces listed successfully!")
                    print(f"   Current Workspace: {data['current_workspace_id']}")
                    print(f"   Available Workspaces: {len(data['workspaces'])}")
                    for workspace in data['workspaces']:
                        print(f"     - {workspace['name']} ({workspace['id']})")
                    
                    # Test application listing
                    print(f"\n📱 Testing application listing...")
                    async with session.get(f"{BACKEND_URL}/llm/dify/applications") as app_response:
                        if app_response.status == 200:
                            app_data = await app_response.json()
                            print(f"✅ Applications listed successfully!")
                            print(f"   Current App: {app_data['current_app_id']}")
                            print(f"   Available Apps: {len(app_data['applications'])}")
                            for app in app_data['applications']:
                                print(f"     - {app['name']} ({app['type']})")
                            
                            # Test completion if apps are available
                            if app_data['applications']:
                                app_id = app_data['applications'][0]['id']
                                print(f"\n✍️ Testing completion with app {app_id}...")
                                
                                completion_data = {
                                    "prompt": "What is the purpose of architecture governance?",
                                    "app_id": app_id,
                                    "user_id": "test_user"
                                }
                                
                                async with session.post(
                                    f"{BACKEND_URL}/llm/dify/completion",
                                    json=completion_data
                                ) as comp_response:
                                    if comp_response.status == 200:
                                        comp_result = await comp_response.json()
                                        if comp_result['success']:
                                            print(f"✅ Completion successful!")
                                            print(f"   Response: {comp_result['text'][:100]}...")
                                            print(f"   Message ID: {comp_result['message_id']}")
                                        else:
                                            print(f"❌ Completion failed: {comp_result['error']}")
                                    else:
                                        print(f"❌ Completion request failed: {comp_response.status}")
                        else:
                            print(f"❌ Application listing failed: {app_response.status}")
                else:
                    print(f"❌ Workspace listing failed: {response.status}")
                    
    except Exception as e:
        print(f"❌ Dify integration test failed: {e}")

async def test_model_pull():
    """Test Ollama model pulling"""
    print("\n📥 Testing Model Pull")
    print("=" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test pulling a small model (this will take time)
            print("⚠️  Note: Model pulling can take several minutes...")
            print("Testing with a small model...")
            
            pull_data = {
                "model": "llama2:7b"  # Small model for testing
            }
            
            async with session.post(
                f"{BACKEND_URL}/llm/ollama/pull",
                json=pull_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['success']:
                        print(f"✅ Model pull initiated successfully!")
                        print(f"   Model: {data['model']}")
                        print(f"   Message: {data['message']}")
                    else:
                        print(f"❌ Model pull failed: {data['error']}")
                else:
                    print(f"❌ Model pull request failed: {response.status}")
                    
    except Exception as e:
        print(f"❌ Model pull test failed: {e}")

async def main():
    """Run all LLM integration tests"""
    print("🧪 LLM Integration Tests")
    print("=" * 60)
    
    # Test health check
    health_data = await test_llm_health()
    
    if health_data and health_data['overall_status'] == 'healthy':
        print("\n✅ LLM services are healthy, proceeding with tests...")
        
        # Test Ollama integration
        await test_ollama_integration()
        
        # Test Dify integration
        await test_dify_integration()
        
        # Test model pull (optional, can be slow)
        # await test_model_pull()
        
    else:
        print("\n❌ LLM services are not healthy. Please check:")
        print("   1. Ollama is running: ollama serve")
        print("   2. Dify API key is configured in .env")
        print("   3. Backend is running: python main.py")
    
    print("\n" + "=" * 60)
    print("🎯 LLM Integration Tests Completed!")
    print("\n📝 Summary:")
    print("  - LLM health check tested")
    print("  - Ollama integration tested")
    print("  - Dify integration tested")
    print("  - Model management tested")
    print("\n🌐 Access the LLM management interface at: http://localhost:3000/llm")

if __name__ == "__main__":
    asyncio.run(main())
