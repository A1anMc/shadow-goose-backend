# 🔍 **INVESTIGATION METHODOLOGY & QUALITY ASSURANCE**

## **🎯 Root Cause Analysis Framework**

### **1. Start with the Obvious**
- **Check the most common failure points first**
- **Syntax errors** → **Import errors** → **Dependencies** → **Logic errors**
- **Always verify basic functionality before diving deep**

### **2. Work Backwards**
- **If endpoint X fails, trace back through the dependency chain**
- **Frontend** → **API** → **Database** → **Environment** → **Configuration**
- **Identify the exact point of failure in the chain**

### **3. Divide and Conquer**
- **Test components individually to isolate issues**
- **Separate concerns**: Backend logic, API endpoints, frontend rendering
- **Isolate variables**: Test one change at a time

### **4. Document Everything**
- **Every test, every error, every fix - document it all**
- **Create detailed logs** of investigation steps
- **Maintain knowledge base** of common issues and solutions

### **5. Assume Nothing**
- **Don't assume something works just because it should**
- **Validate every assumption** with actual testing
- **Test edge cases** and error conditions

---

## **🔧 Systematic Debugging Process**

### **Layer by Layer Testing**
```bash
# 1. Database Layer
python -c "from app.database import get_db; print('✅ Database OK')"

# 2. API Layer
python -c "from app.main import app; print('✅ API OK')"

# 3. Endpoints Layer
curl -s https://api.example.com/health

# 4. Frontend Layer
curl -s https://app.example.com | head -5
```

### **Error Message Analysis**
- **Parse error messages carefully** - they often contain the solution
- **Look for specific error codes** and stack traces
- **Search for similar errors** in documentation and forums

### **Version Control Investigation**
- **Check if recent changes introduced the issue**
- **Use git bisect** to find the exact commit causing problems
- **Review recent pull requests** and merges

### **Environment Differences**
- **Compare local vs deployed behavior**
- **Check environment variables** and configuration
- **Verify dependency versions** match across environments

---

## **🛡️ Advanced Quality Assurance**

### **Proactive Prevention Rules**

#### **1. Import Validation**
```python
# Always test imports before using new modules
try:
    from new_module import new_function
    print("✅ Import successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    # Handle gracefully or provide alternative
```

#### **2. Syntax Pre-check**
```bash
# Run compilation tests before deployment
python -m py_compile app/main.py
python -m py_compile app/grants.py
echo "✅ All files compile successfully"
```

#### **3. Dependency Mapping**
```python
# Maintain a clear dependency graph
DEPENDENCY_MAP = {
    "grants": ["pydantic", "fastapi", "logging"],
    "main": ["grants", "rules_engine", "jwt"],
    "frontend": ["react", "typescript", "tailwind"]
}
```

#### **4. Error Pattern Recognition**
```python
# Learn from previous errors to prevent future ones
ERROR_PATTERNS = {
    "ModuleNotFoundError": "Check import paths and dependencies",
    "ValidationError": "Verify data types and required fields",
    "ConnectionError": "Check network and service availability"
}
```

#### **5. Graceful Degradation**
```python
# Systems should work even if some components fail
try:
    result = critical_function()
except Exception as e:
    logger.warning(f"Critical function failed: {e}")
    result = fallback_function()  # Provide alternative
```

### **Code Quality Enforcement**

#### **No Magic Numbers**
```python
# Use constants and configuration files
GRANT_AMOUNT_MIN = 1000.00
GRANT_AMOUNT_MAX = 100000.00
SUCCESS_SCORE_MIN = 0.0
SUCCESS_SCORE_MAX = 1.0

# Instead of: if amount > 1000 and amount < 100000
if GRANT_AMOUNT_MIN <= amount <= GRANT_AMOUNT_MAX:
    # Process grant
```

#### **Consistent Naming**
```python
# Follow established naming conventions religiously
# Python: snake_case for variables and functions
grant_amount = 50000.00
def calculate_success_score():
    pass

# TypeScript: camelCase for variables, PascalCase for interfaces
const grantAmount = 50000.00;
interface GrantApplication {
    id: string;
    title: string;
}
```

#### **Function Length**
```python
# Keep functions under 50 lines when possible
def process_grant_application(application_data):
    """Process a grant application - keep focused and concise"""
    # Validate input
    validated_data = validate_application_data(application_data)

    # Process business logic
    result = apply_business_rules(validated_data)

    # Return result
    return result
```

#### **Comment Quality**
```python
# Comments should explain WHY, not WHAT
# BAD: "Loop through grants"
# GOOD: "Filter grants by user preferences to improve recommendation accuracy"
for grant in grants:
    if grant.category in user_preferences:
        recommendations.append(grant)
```

#### **Error Messages**
```python
# Make them actionable and specific
# BAD: "Error occurred"
# GOOD: "Grant amount must be between AUD $1,000.00 and AUD $100,000.00. Current value: AUD $50.00"

def validate_grant_amount(amount):
    if not (GRANT_AMOUNT_MIN <= amount <= GRANT_AMOUNT_MAX):
        raise ValueError(
            f"Grant amount must be between {format_currency(GRANT_AMOUNT_MIN)} "
            f"and {format_currency(GRANT_AMOUNT_MAX)}. "
            f"Current value: {format_currency(amount)}"
        )
```

---

## **📊 Quality Metrics Dashboard**

### **Investigation Success Metrics**
- **Time to Resolution**: Track how long issues take to resolve
- **Root Cause Accuracy**: Measure how often we identify the correct root cause
- **Prevention Rate**: Track how many issues are prevented vs. fixed

### **Quality Assurance Metrics**
- **Code Coverage**: Maintain high test coverage
- **Error Rate**: Monitor and reduce error rates over time
- **Performance**: Track response times and system performance

---

## **🎯 Implementation Checklist**

### **For Every Issue Investigation:**
- [ ] **Start with obvious checks** (syntax, imports, basic functionality)
- [ ] **Document the investigation process** step by step
- [ ] **Test each component individually** to isolate the problem
- [ ] **Trace the dependency chain** backwards from the failure point
- [ ] **Validate all assumptions** with actual testing
- [ ] **Document the solution** for future reference

### **For Every Code Change:**
- [ ] **Run syntax pre-checks** before deployment
- [ ] **Validate all imports** work correctly
- [ ] **Follow naming conventions** consistently
- [ ] **Keep functions focused** and under 50 lines
- [ ] **Add meaningful comments** explaining the WHY
- [ ] **Provide actionable error messages**
- [ ] **Test graceful degradation** scenarios

---

## **🚀 Continuous Improvement**

### **Regular Reviews**
- **Weekly**: Review investigation methodology effectiveness
- **Monthly**: Update error patterns and prevention strategies
- **Quarterly**: Refine quality assurance processes

### **Knowledge Sharing**
- **Document common issues** and their solutions
- **Share investigation techniques** across the team
- **Maintain a troubleshooting guide** for the system

**This methodology ensures we maintain the highest quality standards while efficiently resolving any issues that arise.**
