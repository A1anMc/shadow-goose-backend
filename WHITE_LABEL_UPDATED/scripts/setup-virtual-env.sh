#!/bin/bash

# Virtual Environment Setup Script
# Part of the deployment safety system

set -e

echo "🐍 Setting up Python Virtual Environment..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment already exists
if [ -d "venv" ]; then
    print_warning "Virtual environment 'venv' already exists"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Removing existing virtual environment..."
        rm -rf venv
    else
        print_status "Using existing virtual environment"
        exit 0
    fi
fi

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    print_status "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt

    # Verify installation
    print_status "Verifying installation..."
    if pip check; then
        print_success "All dependencies installed successfully!"
    else
        print_error "Dependency conflicts detected!"
        print_status "Running auto-fix..."
        bash WHITE_LABEL_UPDATED/scripts/auto-fix-dependencies.sh
    fi
else
    print_warning "No requirements.txt found"
    print_status "Installing basic development tools..."
    pip install pre-commit safety pipdeptree
fi

# Install pre-commit hooks
print_status "Installing pre-commit hooks..."
pre-commit install

# Create activation script
cat > activate-venv.sh << 'EOF'
#!/bin/bash
# Virtual Environment Activation Script
echo "🐍 Activating Python Virtual Environment..."

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
    echo "📦 Python: $(python --version)"
    echo "📦 Pip: $(pip --version)"
    echo ""
    echo "To deactivate, run: deactivate"
else
    echo "❌ Virtual environment not found"
    echo "Run: bash WHITE_LABEL_UPDATED/scripts/setup-virtual-env.sh"
fi
EOF

chmod +x activate-venv.sh

# Create deactivation reminder
cat > deactivate-venv.sh << 'EOF'
#!/bin/bash
# Virtual Environment Deactivation Script
echo "🐍 Deactivating Python Virtual Environment..."
deactivate
echo "✅ Virtual environment deactivated"
EOF

chmod +x deactivate-venv.sh

# Create environment info
cat > venv-info.txt << EOF
Virtual Environment Information
===============================
Created: $(date)
Python Version: $(python --version)
Pip Version: $(pip --version)
Location: $(pwd)/venv

Activation Commands:
- Source: source venv/bin/activate
- Script: ./activate-venv.sh

Deactivation:
- Command: deactivate
- Script: ./deactivate-venv.sh

Pre-commit hooks: ✅ Installed
Dependencies: ✅ Installed
EOF

print_success "Virtual environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Or use the script: ./activate-venv.sh"
echo "3. Install additional packages: pip install <package>"
echo "4. Update requirements.txt: pip freeze > requirements.txt"
echo ""
echo "📚 Documentation:"
echo "- Virtual environment info: cat venv-info.txt"
echo "- Safety rules: WHITE_LABEL_UPDATED/DEPLOYMENT_SAFETY_RULES.md"
echo "- Quick reference: WHITE_LABEL_UPDATED/DEPENDENCY_QUICK_REFERENCE.md"
