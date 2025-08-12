#!/usr/bin/env python3
"""
Setup script for the Agentic AI Swarm system
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install Python dependencies"""
    # Determine the correct pip command
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_config_file():
    """Create configuration file from template"""
    config_file = Path(".env")
    config_template = Path("config.env.example")
    
    if config_file.exists():
        print("✅ Configuration file already exists")
        return True
    
    if config_template.exists():
        shutil.copy(config_template, config_file)
        print("✅ Configuration file created from template")
        print("⚠️  Please edit .env file with your API keys and settings")
        return True
    else:
        print("❌ Configuration template not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data", "reports"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")
    return True

def run_tests():
    """Run system tests"""
    print("🧪 Running system tests...")
    
    # Determine the correct python command
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} test_system.py", "Running system tests")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your API keys and configuration")
    print("2. Start the application:")
    print("   - For development: python main.py")
    print("   - For production: docker-compose up -d")
    print("3. Access the web dashboard at: http://localhost:8000")
    print("4. View API documentation at: http://localhost:8000/docs")
    print("\n📚 Documentation:")
    print("- README.md: Project overview and usage")
    print("- API docs: http://localhost:8000/docs (when running)")
    print("\n🔧 Configuration:")
    print("- .env: Environment variables and API keys")
    print("- config.env.example: Configuration template")
    print("\n🐳 Docker:")
    print("- docker-compose up -d: Start all services")
    print("- docker-compose down: Stop all services")
    print("- docker-compose logs: View logs")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🚀 Agentic AI Swarm - Setup Script")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create configuration file
    if not create_config_file():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Run tests (optional)
    print("\n🧪 Would you like to run system tests? (y/n): ", end="")
    response = input().lower().strip()
    if response in ['y', 'yes']:
        run_tests()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
