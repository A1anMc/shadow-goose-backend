# ⚡ Dependency Management Quick Reference
## Fast Commands & Solutions for Common Issues

### **🚨 Emergency Fixes**

#### **Dependency Conflict Detected**
```bash
# Quick fix for common conflicts
pip check
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### **Build Failing on Render**
```bash
# Check requirements.txt for conflicts
pip check requirements.txt

# Test locally before deploying
pip install -r requirements.txt
python -m pytest
```

#### **Security Vulnerability Found**
```bash
# Install and run safety check
pip install safety
safety check

# Update vulnerable packages
pip install --upgrade package_name
```

---

## 🔧 **Daily Commands**

### **Check Dependencies**
```bash
# Check for conflicts
pip check

# View dependency tree
pipdeptree

# Check for outdated packages
pip list --outdated

# Security check
safety check
```

### **Update Dependencies**
```bash
# Interactive update (recommended)
pip install pip-review
pip-review --local --interactive

# Update specific package
pip install --upgrade package_name

# Generate new requirements
pip freeze > requirements.txt.new
```

### **Test Dependencies**
```bash
# Run tests
pytest

# Test with coverage
pytest --cov=.

# Performance test
python -c "import time; start=time.time(); [i*2 for i in range(10000)]; print(f'Time: {time.time()-start:.3f}s')"
```

---

## 📋 **Common Issues & Solutions**

### **Issue 1: FastAPI + Pydantic Conflict**
**Error**: `fastapi depends on pydantic<2.0.0 but pydantic==2.7.4 is installed`

**Solution**:
```txt
# In requirements.txt, change:
pydantic==2.7.4
# To:
pydantic==1.10.17
```

### **Issue 2: Python-Multipart Version**
**Error**: `fastapi depends on python-multipart>=0.0.7`

**Solution**:
```txt
# In requirements.txt, change:
python-multipart==0.0.6
# To:
python-multipart>=0.0.7
```

### **Issue 3: SQLAlchemy Integration**
**Error**: SQLAlchemy model validation issues

**Solution**:
```txt
# Use compatible versions:
sqlalchemy==2.0.23
pydantic==1.10.13
```

---

## 🎯 **Recommended Production Stack**

```txt
# Core Framework
fastapi==0.78.0
pydantic==1.10.17
python-multipart>=0.0.7
uvicorn[standard]==0.30.0

# Database
sqlalchemy==2.0.23

# Authentication
PyJWT==2.8.0
passlib[bcrypt]==1.7.4

# Security
email-validator==2.1.0
python-jose[cryptography]==3.3.0

# Monitoring
psutil==5.9.6
prometheus-client==0.19.0
structlog==23.2.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
```

---

## 🚀 **Deployment Checklist**

### **Before Deploying**
- [ ] `pip check` - No conflicts
- [ ] `safety check` - No vulnerabilities
- [ ] `pytest` - All tests pass
- [ ] `pip list --outdated` - Review updates

### **After Deploying**
- [ ] Check deployment logs
- [ ] Test health endpoint
- [ ] Verify all API endpoints
- [ ] Monitor error rates

---

## 📞 **Quick Help**

### **Scripts Available**
```bash
# Check dependencies
./WHITE_LABEL_UPDATED/scripts/check-dependencies.sh

# Update dependencies
./WHITE_LABEL_UPDATED/scripts/update-dependencies.sh

# Test dependencies
./WHITE_LABEL_UPDATED/scripts/test-dependencies.sh
```

### **Documentation**
- **Full Guide**: `WHITE_LABEL_UPDATED/DEPENDENCY_MANAGEMENT_GUIDE.md`
- **Compatibility Matrix**: `WHITE_LABEL_UPDATED/DEPENDENCY_COMPATIBILITY_MATRIX.md`
- **GitHub Actions**: `.github/workflows/dependency-management.yml`

### **Emergency Contacts**
- **Technical Lead**: Alan McCarthy
- **Documentation**: Check the guides above
- **GitHub Issues**: Create issue for persistent problems

---

## 💡 **Pro Tips**

### **Prevent Conflicts**
1. **Always test locally** before pushing
2. **Use exact versions** in production
3. **Update one package** at a time
4. **Keep compatibility matrix** updated

### **Automate Everything**
1. **GitHub Actions** run weekly checks
2. **Pre-commit hooks** catch conflicts
3. **CI/CD pipeline** validates dependencies
4. **Automated testing** after updates

### **Monitor Continuously**
1. **Security alerts** for vulnerabilities
2. **Dependency updates** notifications
3. **Build failure** alerts
4. **Performance monitoring** after updates

---

*This quick reference should be updated whenever new common issues are discovered.*
