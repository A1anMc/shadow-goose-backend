#!/bin/bash

# Auto-Fix Dependency Conflicts
# Automatically detects and fixes common dependency conflicts

set -e

echo "🔧 Auto-Fixing Dependency Conflicts..."
echo "=================================================="

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to fix Python dependency conflicts
fix_python_dependencies() {
    print_status "Checking Python dependencies..."

    if [ ! -f "requirements.txt" ]; then
        print_warning "No requirements.txt found, skipping Python dependency check"
        return 0
    fi

    # Check for dependency conflicts
    if pip check 2>&1 | grep -q "conflict"; then
        print_warning "Python dependency conflicts detected, attempting to fix..."

        # Create backup
        cp requirements.txt requirements.txt.backup
        print_status "Created backup: requirements.txt.backup"

        # Common fixes for known conflicts
        local fixes_applied=0

        # Fix 1: FastAPI + python-multipart conflict
        if grep -q "fastapi==0.111.0" requirements.txt; then
            print_status "Fixing FastAPI version conflict..."
            sed -i '' 's/fastapi==0.111.0/fastapi==0.78.0/' requirements.txt
            fixes_applied=$((fixes_applied + 1))
        fi

        # Fix 2: Pydantic version conflict
        if grep -q "pydantic==2.7.4" requirements.txt; then
            print_status "Fixing Pydantic version conflict..."
            sed -i '' 's/pydantic==2.7.4/pydantic==1.10.17/' requirements.txt
            fixes_applied=$((fixes_applied + 1))
        fi

        # Fix 3: python-multipart version conflict
        if grep -q "python-multipart==0.0.6" requirements.txt; then
            print_status "Fixing python-multipart version conflict..."
            sed -i '' 's/python-multipart==0.0.6/python-multipart>=0.0.7/' requirements.txt
            fixes_applied=$((fixes_applied + 1))
        fi

        # Fix 4: Pydantic 1.10.13 Python 3.13 conflict
        if grep -q "pydantic==1.10.13" requirements.txt; then
            print_status "Fixing Pydantic Python 3.13 compatibility..."
            sed -i '' 's/pydantic==1.10.13/pydantic==1.10.17/' requirements.txt
            fixes_applied=$((fixes_applied + 1))
        fi

        # Verify fix
        if pip check >/dev/null 2>&1; then
            print_success "Python dependency conflicts resolved! ($fixes_applied fixes applied)"
            return 0
        else
            print_error "Failed to resolve Python dependency conflicts"
            print_status "Restoring backup..."
            cp requirements.txt.backup requirements.txt
            return 1
        fi
    else
        print_success "No Python dependency conflicts found"
        return 0
    fi
}

# Function to fix Node.js dependency conflicts
fix_nodejs_dependencies() {
    print_status "Checking Node.js dependencies..."

    if [ ! -f "package.json" ]; then
        print_warning "No package.json found, skipping Node.js dependency check"
        return 0
    fi

    # Check for vulnerabilities
    if npm audit 2>&1 | grep -q "vulnerabilities"; then
        print_warning "Node.js vulnerabilities detected, attempting to fix..."

        # Create backup
        cp package.json package.json.backup
        cp package-lock.json package-lock.json.backup 2>/dev/null || true
        print_status "Created backup: package.json.backup"

        # Try to fix vulnerabilities
        if npm audit fix --force; then
            print_success "Node.js vulnerabilities fixed!"
            return 0
        else
            print_warning "Some vulnerabilities could not be automatically fixed"
            return 0
        fi
    else
        print_success "No Node.js vulnerabilities found"
        return 0
    fi
}

# Function to check runtime compatibility
check_runtime_compatibility() {
    print_status "Checking runtime compatibility..."

    # Check Python runtime
    if [ -f "runtime.txt" ]; then
        local python_version=$(cat runtime.txt | grep -o 'python-[0-9.]*')
        print_status "Python runtime specified: $python_version"

        # Check if runtime is compatible with dependencies
        if [[ "$python_version" == "python-3.13" ]]; then
            if grep -q "pydantic==1.10.13" requirements.txt; then
                print_warning "Python 3.13 detected with incompatible Pydantic version"
                print_status "Updating runtime.txt to Python 3.11..."
                echo "python-3.11" > runtime.txt
                print_success "Runtime updated to Python 3.11"
            fi
        fi
    fi

    # Check Node.js runtime
    if [ -f "package.json" ]; then
        local node_version=$(node --version 2>/dev/null || echo "unknown")
        print_status "Current Node.js version: $node_version"

        # Check engines field
        if grep -q '"engines"' package.json; then
            local required_version=$(grep -o '"node": "[^"]*"' package.json | cut -d'"' -f4)
            print_status "Required Node.js version: $required_version"
        fi
    fi
}

# Function to run tests after fixes
run_tests() {
    print_status "Running tests to verify fixes..."

    local test_passed=true

    # Python tests
    if [ -f "requirements.txt" ]; then
        print_status "Running Python tests..."
        if command_exists pytest; then
            if pytest --tb=short >/dev/null 2>&1; then
                print_success "Python tests passed"
            else
                print_warning "Python tests failed"
                test_passed=false
            fi
        else
            print_warning "pytest not found, skipping Python tests"
        fi
    fi

    # Node.js tests
    if [ -f "package.json" ]; then
        print_status "Running Node.js tests..."
        if npm test >/dev/null 2>&1; then
            print_success "Node.js tests passed"
        else
            print_warning "Node.js tests failed"
            test_passed=false
        fi
    fi

    if [ "$test_passed" = true ]; then
        print_success "All tests passed!"
        return 0
    else
        print_warning "Some tests failed, manual review may be needed"
        return 1
    fi
}

# Function to generate report
generate_report() {
    local report_file="dependency-fix-report.txt"

    cat > "$report_file" << EOF
Dependency Fix Report
====================
Generated: $(date)
Repository: $(git remote get-url origin 2>/dev/null || echo "unknown")

Summary:
- Python dependencies: $(if pip check >/dev/null 2>&1; then echo "✅ OK"; else echo "❌ Issues"; fi)
- Node.js dependencies: $(if npm audit >/dev/null 2>&1; then echo "✅ OK"; else echo "❌ Issues"; fi)
- Runtime compatibility: ✅ Checked

Backup files created:
$(ls -la *.backup 2>/dev/null || echo "No backup files")

Recommendations:
1. Review the changes made
2. Test the application thoroughly
3. Commit changes if everything works
4. Update documentation if needed

EOF

    print_success "Report generated: $report_file"
}

# Main execution
main() {
    print_status "Starting dependency conflict auto-fix..."

    local python_fixed=false
    local nodejs_fixed=false

    # Fix Python dependencies
    if fix_python_dependencies; then
        python_fixed=true
    fi

    # Fix Node.js dependencies
    if fix_nodejs_dependencies; then
        nodejs_fixed=true
    fi

    # Check runtime compatibility
    check_runtime_compatibility

    # Run tests if fixes were applied
    if [ "$python_fixed" = true ] || [ "$nodejs_fixed" = true ]; then
        print_status "Fixes applied, running tests..."
        run_tests
    fi

    # Generate report
    generate_report

    echo ""
    echo "=================================================="
    print_success "Dependency conflict auto-fix completed!"
    echo ""
    echo "Next steps:"
    echo "1. Review the changes made"
    echo "2. Test your application"
    echo "3. Commit changes if everything works"
    echo "4. Deploy to staging for verification"
}

# Run main function
main "$@"
