#!/bin/bash

# 🧪 Dependency Testing Script
# This script tests dependencies and generates comprehensive reports

set -e

echo "🧪 Testing dependencies and generating reports..."
echo "=================================================="

# Create reports directory
mkdir -p reports

# Run tests
echo "1. Running test suite..."
if command -v pytest &> /dev/null; then
    pytest --cov=. --cov-report=html:reports/coverage --cov-report=term-missing tests/ || {
        echo "❌ Tests failed!"
        exit 1
    }
    echo "✅ Tests completed successfully"
else
    echo "⚠️  pytest not found - skipping tests"
fi

# Security check
echo ""
echo "2. Running security vulnerability check..."
if command -v safety &> /dev/null; then
    safety check --json > reports/security-report.json 2>/dev/null || {
        echo "⚠️  Security issues found - check reports/security-report.json"
    }
    safety check --full-report > reports/security-report.txt 2>/dev/null || true
    echo "✅ Security check completed"
else
    echo "Installing safety..."
    pip install safety
    safety check --json > reports/security-report.json 2>/dev/null || {
        echo "⚠️  Security issues found - check reports/security-report.json"
    }
    safety check --full-report > reports/security-report.txt 2>/dev/null || true
    echo "✅ Security check completed"
fi

# Dependency tree
echo ""
echo "3. Generating dependency tree..."
if command -v pipdeptree &> /dev/null; then
    pipdeptree --json > reports/dependency-tree.json
    pipdeptree > reports/dependency-tree.txt
    echo "✅ Dependency tree generated"
else
    echo "Installing pipdeptree..."
    pip install pipdeptree
    pipdeptree --json > reports/dependency-tree.json
    pipdeptree > reports/dependency-tree.txt
    echo "✅ Dependency tree generated"
fi

# Outdated packages
echo ""
echo "4. Checking for outdated packages..."
pip list --outdated > reports/outdated-packages.txt 2>/dev/null || {
    echo "No outdated packages found" > reports/outdated-packages.txt
}
echo "✅ Outdated packages report generated"

# Package info
echo ""
echo "5. Generating package information..."
pip list --format=json > reports/installed-packages.json
pip list > reports/installed-packages.txt
echo "✅ Package information generated"

# Performance check
echo ""
echo "6. Running performance check..."
if command -v psutil &> /dev/null; then
    python -c "
import psutil
import json
import time

# Simple performance test
start_time = time.time()
for i in range(1000):
    _ = i * 2
end_time = time.time()

performance_data = {
    'cpu_percent': psutil.cpu_percent(),
    'memory_percent': psutil.virtual_memory().percent,
    'test_duration_ms': (end_time - start_time) * 1000
}

with open('reports/performance-report.json', 'w') as f:
    json.dump(performance_data, f, indent=2)
"
    echo "✅ Performance check completed"
else
    echo "⚠️  psutil not available - skipping performance check"
fi

# Generate summary report
echo ""
echo "7. Generating summary report..."
cat > reports/summary-report.md << EOF
# Dependency Test Summary Report

Generated on: $(date)

## Test Results
- **Tests**: $(if [ -f reports/coverage/index.html ]; then echo "✅ Passed"; else echo "❌ Failed or not run"; fi)
- **Security**: $(if [ -s reports/security-report.json ]; then echo "⚠️  Issues found"; else echo "✅ Clean"; fi)
- **Dependencies**: $(if [ -s reports/dependency-tree.json ]; then echo "✅ Analyzed"; else echo "❌ Failed"; fi)

## Files Generated
- \`coverage/\` - Test coverage report
- \`security-report.json\` - Security vulnerabilities (JSON)
- \`security-report.txt\` - Security vulnerabilities (Text)
- \`dependency-tree.json\` - Dependency tree (JSON)
- \`dependency-tree.txt\` - Dependency tree (Text)
- \`outdated-packages.txt\` - List of outdated packages
- \`installed-packages.json\` - Installed packages (JSON)
- \`installed-packages.txt\` - Installed packages (Text)
- \`performance-report.json\` - Performance metrics (if available)

## Recommendations
1. Review security vulnerabilities in \`security-report.txt\`
2. Update outdated packages listed in \`outdated-packages.txt\`
3. Check test coverage in \`coverage/index.html\`
4. Review dependency tree for potential conflicts

EOF

echo "✅ Summary report generated"

echo ""
echo "✅ Dependency testing complete!"
echo "=================================================="
echo ""
echo "📋 Reports generated in 'reports/' directory:"
ls -la reports/
echo ""
echo "📊 View coverage report: open reports/coverage/index.html"
echo "🔍 Review security issues: cat reports/security-report.txt"
echo "📋 Check outdated packages: cat reports/outdated-packages.txt"
