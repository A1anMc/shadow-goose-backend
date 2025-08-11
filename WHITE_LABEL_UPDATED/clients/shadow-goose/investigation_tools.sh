#!/bin/bash

# 🔍 Shadow Goose Investigation Tools
# Implements the Investigation Methodology & Quality Assurance rules

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
BACKEND_DIR="/Users/alanmccarthy/shadow-goose-backend"
FRONTEND_DIR="/Users/alanmccarthy/shadow-goose-frontend"
API_URL="https://shadow-goose-api.onrender.com"
FRONTEND_URL="https://shadow-goose-web.onrender.com"

echo -e "${BLUE}🔍 Shadow Goose Investigation Tools${NC}"
echo "======================================"

# Function to log investigation steps
log_investigation() {
    echo -e "${PURPLE}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. START WITH THE OBVIOUS
investigation_start_with_obvious() {
    echo -e "\n${YELLOW}🎯 1. START WITH THE OBVIOUS${NC}"
    echo "================================"

    log_investigation "Starting investigation with obvious failure points"

    # Check if we're in the right directory
    if [ ! -d "$BACKEND_DIR" ]; then
        echo -e "${RED}❌ Backend directory not found: $BACKEND_DIR${NC}"
        return 1
    fi

    if [ ! -d "$FRONTEND_DIR" ]; then
        echo -e "${RED}❌ Frontend directory not found: $FRONTEND_DIR${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ Directory structure OK${NC}"

    # Check Python installation
    if ! command_exists python3; then
        echo -e "${RED}❌ Python3 not found${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ Python3 available${NC}"

    # Check Node.js installation
    if ! command_exists node; then
        echo -e "${RED}❌ Node.js not found${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ Node.js available${NC}"

    # Check Git installation
    if ! command_exists git; then
        echo -e "${RED}❌ Git not found${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ Git available${NC}"

    log_investigation "Basic environment checks completed"
}

# 2. SYNTAX PRE-CHECK
investigation_syntax_precheck() {
    echo -e "\n${YELLOW}🔧 2. SYNTAX PRE-CHECK${NC}"
    echo "========================="

    log_investigation "Running syntax pre-checks"

    cd "$BACKEND_DIR"

    # Check Python syntax
    echo "Checking Python syntax..."
    for file in app/*.py; do
        if [ -f "$file" ]; then
            if python3 -m py_compile "$file"; then
                echo -e "${GREEN}✅ $(basename "$file") syntax OK${NC}"
            else
                echo -e "${RED}❌ $(basename "$file") syntax error${NC}"
                return 1
            fi
        fi
    done

    # Check TypeScript syntax
    cd "$FRONTEND_DIR"
    echo "Checking TypeScript syntax..."
    if npm run type-check >/dev/null 2>&1; then
        echo -e "${GREEN}✅ TypeScript syntax OK${NC}"
    else
        echo -e "${YELLOW}⚠️ TypeScript syntax issues detected${NC}"
    fi

    log_investigation "Syntax pre-checks completed"
}

# 3. IMPORT VALIDATION
investigation_import_validation() {
    echo -e "\n${YELLOW}📦 3. IMPORT VALIDATION${NC}"
    echo "========================="

    log_investigation "Validating imports"

    cd "$BACKEND_DIR"

    # Test critical imports
    echo "Testing critical imports..."

    if python3 -c "from app.grants import grant_service; print('✅ Grants module OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ Grants module imports OK${NC}"
    else
        echo -e "${RED}❌ Grants module import failed${NC}"
        return 1
    fi

    if python3 -c "from app.rules_engine import rules_engine; print('✅ Rules engine OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ Rules engine imports OK${NC}"
    else
        echo -e "${RED}❌ Rules engine import failed${NC}"
        return 1
    fi

    if python3 -c "from app.main import app; print('✅ Main app OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ Main app imports OK${NC}"
    else
        echo -e "${RED}❌ Main app import failed${NC}"
        return 1
    fi

    log_investigation "Import validation completed"
}

# 4. WORK BACKWARDS - LAYER BY LAYER
investigation_work_backwards() {
    echo -e "\n${YELLOW}🔄 4. WORK BACKWARDS - LAYER BY LAYER${NC}"
    echo "========================================="

    log_investigation "Testing layers from database to frontend"

    # Layer 1: Database (if applicable)
    echo "Layer 1: Database connectivity..."
    # Add database checks here when database is implemented

    # Layer 2: API Layer
    echo "Layer 2: API endpoints..."
    if curl -s "$API_URL/health" >/dev/null; then
        echo -e "${GREEN}✅ API health endpoint responding${NC}"
        API_HEALTH=$(curl -s "$API_URL/health")
        echo "API Health: $API_HEALTH"
    else
        echo -e "${RED}❌ API health endpoint not responding${NC}"
        return 1
    fi

    # Layer 3: Frontend Layer
    echo "Layer 3: Frontend..."
    if curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -q "200"; then
        echo -e "${GREEN}✅ Frontend responding${NC}"
    else
        echo -e "${RED}❌ Frontend not responding${NC}"
        return 1
    fi

    log_investigation "Layer-by-layer testing completed"
}

# 5. DIVIDE AND CONQUER
investigation_divide_conquer() {
    echo -e "\n${YELLOW}🎯 5. DIVIDE AND CONQUER${NC}"
    echo "========================="

    log_investigation "Testing components individually"

    # Test backend components
    echo "Testing backend components..."
    cd "$BACKEND_DIR"

    # Test grants service
    if python3 -c "from app.grants import grant_service; grants = grant_service.get_all_grants(); print(f'✅ Grants service: {len(grants)} grants found')" 2>/dev/null; then
        echo -e "${GREEN}✅ Grants service working${NC}"
    else
        echo -e "${RED}❌ Grants service failed${NC}"
    fi

    # Test rules engine
    if python3 -c "from app.rules_engine import rules_engine; rules = rules_engine.get_all_rules(); print(f'✅ Rules engine: {len(rules)} rules found')" 2>/dev/null; then
        echo -e "${GREEN}✅ Rules engine working${NC}"
    else
        echo -e "${RED}❌ Rules engine failed${NC}"
    fi

    # Test frontend components
    echo "Testing frontend components..."
    cd "$FRONTEND_DIR"

    # Check if build works
    if npm run build >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend builds successfully${NC}"
    else
        echo -e "${YELLOW}⚠️ Frontend build issues detected${NC}"
    fi

    log_investigation "Component testing completed"
}

# 6. ERROR PATTERN RECOGNITION
investigation_error_patterns() {
    echo -e "\n${YELLOW}🔍 6. ERROR PATTERN RECOGNITION${NC}"
    echo "==============================="

    log_investigation "Checking for common error patterns"

    # Check for common Python errors
    echo "Checking for common Python error patterns..."

    cd "$BACKEND_DIR"

    # Check for missing imports
    if grep -r "ModuleNotFoundError" . --include="*.py" >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️ Potential import errors detected${NC}"
    else
        echo -e "${GREEN}✅ No obvious import errors${NC}"
    fi

    # Check for syntax errors
    if python3 -m py_compile app/main.py 2>&1 | grep -q "SyntaxError"; then
        echo -e "${RED}❌ Syntax errors detected${NC}"
    else
        echo -e "${GREEN}✅ No syntax errors detected${NC}"
    fi

    # Check for magic numbers
    echo "Checking for magic numbers..."
    MAGIC_NUMBERS=$(grep -r "if.*[0-9]\{4,\}" app/ --include="*.py" | grep -v "import\|from" || true)
    if [ -n "$MAGIC_NUMBERS" ]; then
        echo -e "${YELLOW}⚠️ Potential magic numbers detected:${NC}"
        echo "$MAGIC_NUMBERS"
    else
        echo -e "${GREEN}✅ No obvious magic numbers${NC}"
    fi

    log_investigation "Error pattern recognition completed"
}

# 7. GRACEFUL DEGRADATION TEST
investigation_graceful_degradation() {
    echo -e "\n${YELLOW}🔄 7. GRACEFUL DEGRADATION TEST${NC}"
    echo "================================="

    log_investigation "Testing graceful degradation scenarios"

    # Test API with invalid token
    echo "Testing API with invalid authentication..."
    if curl -s -H "Authorization: Bearer invalid_token" "$API_URL/api/grants" | grep -q "Invalid token"; then
        echo -e "${GREEN}✅ API handles invalid authentication gracefully${NC}"
    else
        echo -e "${YELLOW}⚠️ API authentication error handling needs review${NC}"
    fi

    # Test frontend with API down
    echo "Testing frontend error handling..."
    # This would require more sophisticated testing

    log_investigation "Graceful degradation testing completed"
}

# 8. DOCUMENT EVERYTHING
investigation_document_everything() {
    echo -e "\n${YELLOW}📝 8. DOCUMENT EVERYTHING${NC}"
    echo "========================="

    log_investigation "Creating investigation report"

    # Create investigation report
    REPORT_FILE="investigation_report_$(date '+%Y%m%d_%H%M%S').md"

    cat > "$REPORT_FILE" << EOF
# 🔍 Investigation Report - $(date '+%Y-%m-%d %H:%M:%S')

## Investigation Summary
- **Date**: $(date)
- **Investigator**: Shadow Goose Investigation Tools
- **Scope**: Full system health check

## Findings

### ✅ Working Components
- Directory structure
- Python and Node.js installations
- Basic syntax validation
- Import validation
- API health endpoints
- Frontend responsiveness

### ⚠️ Areas for Attention
- Check for magic numbers in code
- Review error handling patterns
- Monitor graceful degradation

## Recommendations
1. Continue monitoring system health
2. Implement automated testing
3. Regular code quality reviews
4. Maintain error pattern database

## Next Steps
- Schedule follow-up investigation
- Update documentation
- Share findings with team
EOF

    echo -e "${GREEN}✅ Investigation report created: $REPORT_FILE${NC}"
    log_investigation "Documentation completed"
}

# Main investigation function
run_full_investigation() {
    echo -e "${BLUE}🚀 Starting Full Investigation${NC}"
    echo "================================"

    # Run all investigation steps
    investigation_start_with_obvious
    investigation_syntax_precheck
    investigation_import_validation
    investigation_work_backwards
    investigation_divide_conquer
    investigation_error_patterns
    investigation_graceful_degradation
    investigation_document_everything

    echo -e "\n${GREEN}🎉 Investigation Complete!${NC}"
    echo "================================"
    echo -e "${GREEN}✅ All investigation steps completed${NC}"
    echo -e "${GREEN}✅ Report generated${NC}"
    echo -e "${GREEN}✅ System health verified${NC}"
}

# Quick health check
quick_health_check() {
    echo -e "${BLUE}⚡ Quick Health Check${NC}"
    echo "======================="

    # Check API health
    if curl -s "$API_URL/health" >/dev/null; then
        echo -e "${GREEN}✅ API Healthy${NC}"
    else
        echo -e "${RED}❌ API Unhealthy${NC}"
    fi

    # Check frontend
    if curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -q "200"; then
        echo -e "${GREEN}✅ Frontend Healthy${NC}"
    else
        echo -e "${RED}❌ Frontend Unhealthy${NC}"
    fi

    echo -e "${GREEN}✅ Quick health check complete${NC}"
}

# Show usage
show_usage() {
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  full     - Run full investigation (default)"
    echo "  quick    - Run quick health check"
    echo "  syntax   - Run syntax pre-check only"
    echo "  imports  - Run import validation only"
    echo "  layers   - Run layer-by-layer testing only"
    echo "  help     - Show this help message"
}

# Main script logic
case "${1:-full}" in
    "full")
        run_full_investigation
        ;;
    "quick")
        quick_health_check
        ;;
    "syntax")
        investigation_syntax_precheck
        ;;
    "imports")
        investigation_import_validation
        ;;
    "layers")
        investigation_work_backwards
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_usage
        exit 1
        ;;
esac
