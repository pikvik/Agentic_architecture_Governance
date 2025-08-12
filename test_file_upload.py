#!/usr/bin/env python3
"""
Test script for file upload functionality
"""

import asyncio
import aiohttp
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"

async def test_file_upload():
    """Test file upload functionality"""
    print("🚀 Testing File Upload Functionality")
    print("=" * 50)
    
    # Create a test file
    test_content = """
    Architecture Document Test
    
    This is a test architecture document containing:
    - Microservices architecture
    - API Gateway pattern
    - Database components
    - Security considerations
    
    Components identified:
    - User Service
    - Order Service
    - Payment Service
    - API Gateway
    - Database Cluster
    
    Architecture Patterns:
    - Microservices Pattern
    - Event-Driven Architecture
    - CQRS Pattern
    
    Decisions:
    - Chosen to use microservices for scalability
    - Selected API Gateway for centralized routing
    - Opted for event-driven communication
    """
    
    test_file_path = Path("test_architecture.txt")
    with open(test_file_path, "w") as f:
        f.write(test_content)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test file upload endpoint
            print("📤 Testing file upload...")
            
            with open(test_file_path, "rb") as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename='test_architecture.txt')
                data.add_field('architecture_domain', 'solution')
                data.add_field('description', 'Test architecture document')
                data.add_field('project_id', 'test_project')
                
                async with session.post(f"{BACKEND_URL}/files/upload", data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ File upload successful!")
                        print(f"   File ID: {result['file_id']}")
                        print(f"   Filename: {result['filename']}")
                        print(f"   File Type: {result['file_type']}")
                        print(f"   File Size: {result['file_size']} bytes")
                        print(f"   Status: {result['status']}")
                        
                        file_id = result['file_id']
                        
                        # Test file listing
                        print("\n📋 Testing file listing...")
                        async with session.get(f"{BACKEND_URL}/files") as list_response:
                            if list_response.status == 200:
                                files_result = await list_response.json()
                                print(f"✅ File listing successful!")
                                print(f"   Total files: {files_result['total']}")
                            else:
                                print(f"❌ File listing failed: {list_response.status}")
                        
                        # Test file validation
                        print("\n🔍 Testing file validation...")
                        validation_data = {
                            "file_id": file_id,
                            "validation_rules": ["architecture_consistency", "security_compliance"],
                            "compliance_frameworks": ["ISO_27001", "TOGAF"],
                            "quality_standards": ["AWS_Well_Architected"],
                            "priority": "high"
                        }
                        
                        async with session.post(
                            f"{BACKEND_URL}/files/{file_id}/validate",
                            json=validation_data
                        ) as validation_response:
                            if validation_response.status == 200:
                                validation_result = await validation_response.json()
                                print(f"✅ File validation successful!")
                                print(f"   Validation Status: {validation_result['validation_status']}")
                                print(f"   Compliance Score: {validation_result['compliance_score']}")
                                print(f"   Quality Score: {validation_result['quality_score']}")
                            else:
                                print(f"❌ File validation failed: {validation_response.status}")
                        
                        # Test file deletion
                        print("\n🗑️ Testing file deletion...")
                        async with session.delete(f"{BACKEND_URL}/files/{file_id}") as delete_response:
                            if delete_response.status == 200:
                                delete_result = await delete_response.json()
                                print(f"✅ File deletion successful!")
                                print(f"   Message: {delete_result['message']}")
                            else:
                                print(f"❌ File deletion failed: {delete_response.status}")
                        
                    else:
                        error_text = await response.text()
                        print(f"❌ File upload failed: {response.status}")
                        print(f"   Error: {error_text}")
    
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
    
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()
            print(f"\n🧹 Cleaned up test file: {test_file_path}")

async def test_supported_formats():
    """Test supported file formats"""
    print("\n📄 Testing Supported File Formats")
    print("=" * 50)
    
    supported_formats = [
        ("test.pdf", "application/pdf"),
        ("test.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("test.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
        ("test.png", "image/png"),
        ("test.jpg", "image/jpeg"),
        ("test.svg", "image/svg+xml"),
    ]
    
    async with aiohttp.ClientSession() as session:
        for filename, content_type in supported_formats:
            print(f"Testing {filename}...")
            
            # Create a simple test file
            test_content = f"Test content for {filename}"
            test_file_path = Path(filename)
            
            try:
                with open(test_file_path, "w") as f:
                    f.write(test_content)
                
                with open(test_file_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field('file', f, filename=filename)
                    
                    async with session.post(f"{BACKEND_URL}/files/upload", data=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            print(f"  ✅ {filename} - Upload successful")
                        else:
                            error_text = await response.text()
                            print(f"  ❌ {filename} - Upload failed: {error_text}")
            
            except Exception as e:
                print(f"  ❌ {filename} - Error: {e}")
            
            finally:
                # Clean up
                if test_file_path.exists():
                    test_file_path.unlink()

async def main():
    """Run all tests"""
    print("🧪 File Upload System Tests")
    print("=" * 60)
    
    # Test basic file upload functionality
    await test_file_upload()
    
    # Test supported formats
    await test_supported_formats()
    
    print("\n" + "=" * 60)
    print("🎯 File Upload Tests Completed!")
    print("\n📝 Summary:")
    print("  - File upload endpoint tested")
    print("  - File listing endpoint tested")
    print("  - File validation endpoint tested")
    print("  - File deletion endpoint tested")
    print("  - Supported formats verified")
    print("\n🌐 Access the file upload interface at: http://localhost:3000/upload")

if __name__ == "__main__":
    asyncio.run(main())
