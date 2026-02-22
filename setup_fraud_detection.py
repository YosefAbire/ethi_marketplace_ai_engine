#!/usr/bin/env python3
"""
Complete setup script for the Ethiopian Marketplace Fraud Detection System.
This script sets up the entire fraud detection system from scratch.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def check_requirements():
    """Check if required tools are installed."""
    print("🔍 Checking requirements...")
    
    requirements = [
        ("python", "python --version"),
        ("pip", "pip --version"),
        ("node", "node --version"),
        ("npm", "npm --version")
    ]
    
    missing = []
    for name, command in requirements:
        try:
            subprocess.run(command, shell=True, check=True, 
                         capture_output=True, text=True)
            print(f"   ✅ {name} is installed")
        except subprocess.CalledProcessError:
            print(f"   ❌ {name} is not installed")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing requirements: {', '.join(missing)}")
        print("Please install the missing requirements and try again.")
        return False
    
    print("✅ All requirements are satisfied")
    return True

def setup_backend():
    """Set up the backend fraud detection system."""
    print("\n📦 Setting up backend fraud detection system...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", 
                      "Installing Python dependencies", cwd=backend_dir):
        return False
    
    # Set up fraud detection database tables
    if not run_command("python setup_fraud_detection.py", 
                      "Setting up fraud detection database", cwd=backend_dir):
        return False
    
    # Test fraud detection system
    if not run_command("python test_fraud_detection.py", 
                      "Testing fraud detection system", cwd=backend_dir):
        print("⚠️  Fraud detection tests failed, but continuing setup...")
    
    return True

def setup_frontend():
    """Set up the frontend fraud detection components."""
    print("\n🎨 Setting up frontend fraud detection components...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install Node.js dependencies
    if not run_command("npm install", 
                      "Installing Node.js dependencies", cwd=frontend_dir):
        return False
    
    # Build frontend
    if not run_command("npm run build", 
                      "Building frontend", cwd=frontend_dir):
        print("⚠️  Frontend build failed, but continuing...")
    
    return True

def create_env_file():
    """Create or update .env file with fraud detection settings."""
    print("\n⚙️  Configuring environment variables...")
    
    env_file = Path("backend/.env")
    env_content = []
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.readlines()
    
    # Add fraud detection specific settings
    fraud_settings = [
        "# Fraud Detection Settings\n",
        "FRAUD_DETECTION_ENABLED=true\n",
        "FRAUD_SCAN_INTERVAL=3600\n",  # 1 hour
        "FRAUD_ALERT_THRESHOLD=70\n",
        "FRAUD_AUTO_RESOLVE=false\n",
        "\n"
    ]
    
    # Check if fraud settings already exist
    has_fraud_settings = any("FRAUD_DETECTION_ENABLED" in line for line in env_content)
    
    if not has_fraud_settings:
        env_content.extend(fraud_settings)
        
        with open(env_file, 'w') as f:
            f.writelines(env_content)
        
        print("✅ Environment variables configured")
    else:
        print("✅ Environment variables already configured")
    
    return True

def create_documentation():
    """Create fraud detection documentation."""
    print("\n📚 Creating fraud detection documentation...")
    
    docs_content = """# Ethiopian Marketplace Fraud Detection System

## Overview
The fraud detection system uses AI to identify and prevent fraudulent activities in the Ethiopian marketplace. It monitors pricing patterns, transaction behaviors, inventory changes, and coordinated attacks.

## Features
- **Real-time Fraud Detection**: Monitors transactions as they happen
- **Pricing Manipulation Detection**: Identifies abnormal price changes
- **Transaction Pattern Analysis**: Detects wash trading and artificial inflation
- **Inventory Fraud Detection**: Identifies phantom inventory and stock manipulation
- **Coordinated Attack Detection**: Finds coordinated fraud across multiple accounts
- **Ethiopian Market Context**: Understands seasonal patterns and cultural factors

## API Endpoints

### Fraud Detection
- `POST /fraud/scan` - Run fraud detection scan
- `GET /fraud/alerts` - Get active fraud alerts
- `GET /fraud/alerts/{id}` - Get alert details
- `PUT /fraud/alerts/{id}/status` - Update alert status
- `GET /fraud/statistics` - Get fraud statistics
- `POST /fraud/check-transaction` - Check transaction for fraud
- `POST /fraud/ask` - Natural language fraud queries

### Usage Examples

#### Run Fraud Scan
```bash
curl -X POST http://localhost:8000/fraud/scan \\
  -H "Content-Type: application/json" \\
  -d '{"scan_type": "full"}'
```

#### Get Active Alerts
```bash
curl http://localhost:8000/fraud/alerts?risk_level=high&limit=10
```

#### Check Transaction
```bash
curl -X POST http://localhost:8000/fraud/check-transaction \\
  -H "Content-Type: application/json" \\
  -d '{
    "transaction_id": "TXN-001",
    "user_id": "user123",
    "product": "Premium Teff",
    "amount": 500.0
  }'
```

## Frontend Integration
The fraud detection dashboard is available at `/fraud` in the main application. It provides:
- Real-time fraud alerts
- Risk assessment dashboard
- Alert investigation tools
- Fraud statistics and trends

## Ethiopian Market Context
The system understands Ethiopian market patterns including:
- Seasonal pricing for teff, coffee, honey, and other traditional products
- Holiday demand patterns (Meskel, Timkat, Fasika)
- Regional price variations
- Traditional trading practices

## Configuration
Fraud detection settings can be configured in the `.env` file:
- `FRAUD_DETECTION_ENABLED`: Enable/disable fraud detection
- `FRAUD_SCAN_INTERVAL`: How often to run scans (seconds)
- `FRAUD_ALERT_THRESHOLD`: Risk score threshold for alerts
- `FRAUD_AUTO_RESOLVE`: Automatically resolve low-confidence alerts

## Monitoring
The system provides comprehensive monitoring through:
- Real-time alerts
- Statistical dashboards
- Investigation tools
- Audit trails

For more information, see the technical documentation in the codebase.
"""
    
    docs_file = Path("FRAUD_DETECTION_GUIDE.md")
    with open(docs_file, 'w') as f:
        f.write(docs_content)
    
    print("✅ Documentation created: FRAUD_DETECTION_GUIDE.md")
    return True

def main():
    """Main setup function."""
    print("🚀 Ethiopian Marketplace Fraud Detection System Setup")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        sys.exit(1)
    
    # Configure environment
    if not create_env_file():
        print("\n❌ Environment configuration failed")
        sys.exit(1)
    
    # Create documentation
    if not create_documentation():
        print("\n❌ Documentation creation failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 FRAUD DETECTION SYSTEM SETUP COMPLETE!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Start the backend server:")
    print("   cd backend && python api/main.py")
    print("\n2. Start the frontend development server:")
    print("   cd frontend && npm run dev")
    print("\n3. Access the fraud detection dashboard:")
    print("   http://localhost:3000 -> Navigate to 'Fraud Detection'")
    print("\n4. Test the fraud detection API:")
    print("   curl -X POST http://localhost:8000/fraud/scan")
    print("\n5. Read the documentation:")
    print("   cat FRAUD_DETECTION_GUIDE.md")
    print("\n🔒 Your Ethiopian marketplace is now protected by AI-powered fraud detection!")

if __name__ == "__main__":
    main()