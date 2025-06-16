#!/usr/bin/env python3
"""
RecipeSnap Setup Script
Installs and configures the entire RecipeSnap application.
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run a command and return True if successful."""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if required software is installed."""
    requirements = {
        'python': 'python --version',
        'node': 'node --version',
        'npm': 'npm --version'
    }
    
    print("Checking system requirements...")
    for name, command in requirements.items():
        if not run_command(command):
            print(f"Error: {name} is not installed or not in PATH")
            return False
    
    return True

def setup_backend():
    """Set up the Python backend."""
    print("\n" + "="*50)
    print("Setting up backend...")
    print("="*50)
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", cwd="backend"):
        print("Failed to install Python dependencies")
        return False
    
    # Download AI models
    if not run_command("python start.py", cwd="backend"):
        print("Failed to download AI models")
        return False
    
    return True

def setup_frontend():
    """Set up the Next.js frontend."""
    print("\n" + "="*50)
    print("Setting up frontend...")
    print("="*50)
    
    # Install Node dependencies
    if not run_command("npm install", cwd="frontend"):
        print("Failed to install Node.js dependencies")
        return False
    
    return True

def create_start_scripts():
    """Create convenient start scripts."""
    print("\n" + "="*50)
    print("Creating start scripts...")
    print("="*50)
    
    # Create backend start script
    backend_script = """#!/bin/bash
cd backend
python main.py
"""
    
    frontend_script = """#!/bin/bash
cd frontend
npm run dev
"""
    
    # Windows batch files
    backend_bat = """@echo off
cd backend
python main.py
"""
    
    frontend_bat = """@echo off
cd frontend
npm run dev
"""
    
    scripts = [
        ("start-backend.sh", backend_script),
        ("start-frontend.sh", frontend_script),
        ("start-backend.bat", backend_bat),
        ("start-frontend.bat", frontend_bat)
    ]
    
    for filename, content in scripts:
        with open(filename, 'w') as f:
            f.write(content)
        
        # Make shell scripts executable on Unix systems
        if filename.endswith('.sh') and platform.system() != 'Windows':
            os.chmod(filename, 0o755)
    
    print("✓ Start scripts created")
    return True

def main():
    """Main setup function."""
    print("RecipeSnap Setup")
    print("=" * 50)
    print("This will install and configure the RecipeSnap application.")
    print("Please ensure you have Python 3.8+, Node.js 16+, and npm installed.")
    print()
    
    # Check requirements
    if not check_requirements():
        print("\nSetup failed: Missing requirements")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\nSetup failed: Backend setup error")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\nSetup failed: Frontend setup error")
        sys.exit(1)
    
    # Create start scripts
    if not create_start_scripts():
        print("\nWarning: Failed to create start scripts")
    
    print("\n" + "="*50)
    print("🎉 Setup completed successfully!")
    print("="*50)
    print()
    print("To start the application:")
    print("1. Backend:  python start-backend.py  (or start-backend.sh)")
    print("2. Frontend: npm run dev --prefix frontend  (or start-frontend.sh)")
    print()
    print("Then open http://localhost:3000 in your browser")
    print()
    print("Note: The backend will run on http://localhost:8000")

if __name__ == "__main__":
    main() 