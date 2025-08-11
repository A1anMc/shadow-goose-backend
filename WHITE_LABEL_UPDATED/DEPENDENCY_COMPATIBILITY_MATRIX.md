# 🔗 Dependency Compatibility Matrix
## Version Compatibility Guide for Shadow Goose Platform

### **Overview**
This matrix shows compatible versions of key dependencies to prevent conflicts during deployment.

---

## 🐍 **Python Framework Compatibility**

### **FastAPI Compatibility Matrix**

| FastAPI Version | Pydantic Version | Python Version | Python-Multipart | Starlette | Status |
|-----------------|------------------|----------------|------------------|-----------|--------|
| 0.78.0 | 1.10.17 | 3.11 | >=0.0.7 | 0.19.1 | ✅ **Recommended** |
| 0.79.0 | 1.10.17 | 3.11 | >=0.0.7 | 0.20.0 | ✅ Compatible |
| 0.80.0 | 1.10.17 | 3.11 | >=0.0.7 | 0.21.0 | ✅ Compatible |
| 0.111.0 | 2.7.4 | 3.13 | >=0.0.7 | 0.37.2 | ❌ **Conflicts** |

### **Pydantic Version Compatibility**

| Pydantic Version | Python Compatible | FastAPI Compatible | SQLAlchemy Compatible | Status |
|------------------|-------------------|-------------------|----------------------|--------|
| 1.10.17 | 3.7 - 3.11 | 0.78.0 - 0.80.0 | 2.0.23 | ✅ **Recommended** |
| 1.10.13 | 3.7 - 3.11 | 0.78.0 - 0.80.0 | 2.0.23 | ⚠️ **Python 3.13 Issues** |
| 2.0.0 | 3.7+ | 0.100.0+ | 2.0.23 | ⚠️ Breaking Changes |
| 2.7.4 | 3.7+ | 0.100.0+ | 2.0.23 | ❌ **Conflicts with FastAPI 0.78.0** |

---

## 🔧 **Core Dependencies**

### **Production-Ready Combinations**

#### **Combination 1: Stable Production**
```txt
fastapi==0.78.0
pydantic==1.10.17
python-multipart>=0.0.7
uvicorn[standard]==0.30.0
sqlalchemy==2.0.23
PyJWT==2.8.0
```
**Status**: ✅ **Recommended for Production**

#### **Combination 2: Latest Stable**
```txt
fastapi==0.80.0
pydantic==1.10.13
python-multipart>=0.0.7
uvicorn[standard]==0.30.0
sqlalchemy==2.0.23
PyJWT==2.8.0
```
**Status**: ✅ **Compatible**

#### **Combination 3: Development Testing**
```txt
fastapi==0.111.0
pydantic==2.7.4
python-multipart>=0.0.7
uvicorn[standard]==0.30.0
sqlalchemy==2.0.23
PyJWT==2.8.0
```
**Status**: ⚠️ **Requires Code Migration**

---

## 🚨 **Known Conflicts & Solutions**

### **Conflict 1: Python 3.13 + Pydantic 1.10.13**
**Error**: `TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'`

**Solution**: Use Pydantic 1.10.17 and Python 3.11
```txt
# In requirements.txt, change:
pydantic==1.10.13
# To:
pydantic==1.10.17

# Add runtime.txt:
python-3.11
```

### **Conflict 2: FastAPI 0.78.0 + Pydantic 2.7.4**
**Error**: `fastapi 0.78.0 depends on pydantic!=1.7, !=1.7.1, !=1.7.2, !=1.7.3, !=1.8, !=1.8.1, <2.0.0 and >=1.6.2`

**Solution**: Use Pydantic 1.10.17
```txt
# Change this:
pydantic==2.7.4

# To this:
pydantic==1.10.17
```

### **Conflict 2: FastAPI 0.111.0 + python-multipart 0.0.6**
**Error**: `fastapi 0.111.0 depends on python-multipart>=0.0.7`

**Solution**: Use python-multipart >=0.0.7
```txt
# Change this:
python-multipart==0.0.6

# To this:
python-multipart>=0.0.7
```

### **Conflict 3: SQLAlchemy + Pydantic Version Mismatch**
**Error**: SQLAlchemy integration issues with Pydantic 2.x

**Solution**: Use compatible versions
```txt
# For Pydantic 1.x:
sqlalchemy==2.0.23

# For Pydantic 2.x:
sqlalchemy==2.0.23
# Plus additional configuration required
```

---

## 📋 **Dependency Update Checklist**

### **Before Updating Dependencies**

- [ ] **Check compatibility matrix** for target versions
- [ ] **Review breaking changes** in changelogs
- [ ] **Test in development** environment first
- [ ] **Update one major dependency** at a time
- [ ] **Run full test suite** after each update
- [ ] **Check security vulnerabilities** with `safety check`
- [ ] **Verify deployment** in staging environment

### **During Update Process**

- [ ] **Create backup** of current requirements.txt
- [ ] **Update dependencies** incrementally
- [ ] **Run dependency conflict check** with `pip check`
- [ ] **Test all functionality** thoroughly
- [ ] **Check performance impact**
- [ ] **Update documentation** if needed

### **After Update**

- [ ] **Deploy to staging** first
- [ ] **Monitor for errors** in logs
- [ ] **Test all endpoints** and features
- [ ] **Check performance metrics**
- [ ] **Update compatibility matrix** if needed
- [ ] **Document any breaking changes**

---

## 🛠️ **Automated Tools**

### **Pre-Update Validation**
```bash
# Check current dependencies
pip check

# Check for conflicts
pipdeptree --warn silence

# Security check
safety check

# Test current setup
pytest
```

### **Update Process**
```bash
# Interactive update
pip-review --local --interactive

# Automatic update (use with caution)
pip-review --local --auto

# Generate new requirements
pip freeze > requirements.txt.new
```

### **Post-Update Validation**
```bash
# Verify no conflicts
pip check

# Run tests
pytest

# Security check
safety check

# Performance test
# (implement your performance tests)
```

---

## 📊 **Version Tracking**

### **Current Production Versions**
```txt
fastapi==0.78.0
pydantic==1.10.17
python-multipart>=0.0.7
uvicorn[standard]==0.30.0
sqlalchemy==2.0.23
PyJWT==2.8.0
```

### **Last Updated**: 2025-01-11
### **Next Review**: 2025-02-11

---

## 🎯 **Best Practices**

### **Version Pinning Strategy**
1. **Production**: Use exact versions (`==`)
2. **Development**: Use compatible ranges (`>=`, `<`)
3. **Testing**: Use latest versions (no pinning)

### **Update Frequency**
- **Security updates**: Immediately
- **Minor versions**: Monthly
- **Major versions**: Quarterly
- **Framework updates**: Semi-annually

### **Testing Strategy**
- **Unit tests**: After every dependency change
- **Integration tests**: After major updates
- **Performance tests**: After framework updates
- **Security tests**: After every update

---

## 📞 **Support & Resources**

### **Useful Commands**
```bash
# Check compatibility
pip check

# View dependency tree
pipdeptree

# Check for updates
pip list --outdated

# Security check
safety check

# Interactive updates
pip-review --local --interactive
```

### **Documentation Links**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Python Package Index](https://pypi.org/)

---

*This matrix should be updated whenever new versions are tested or conflicts are discovered.*
