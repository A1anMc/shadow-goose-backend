# 🚀 Deployment Checklist
## Quick Checklist to Prevent Deployment Failures

### **Before Every Deployment**

#### **1. Dependency Check (2 minutes)**
```bash
# Python dependencies
pip check
safety check

# Node.js dependencies
npm audit
npm run type-check
```

**✅ Must Pass**: No dependency conflicts or TypeScript errors

#### **2. Build Test (3 minutes)**
```bash
# Python build test
pip install -r requirements.txt
python -c "import app.main"  # Test import

# Node.js build test
npm ci
npm run build
```

**✅ Must Pass**: Both builds complete successfully

#### **3. Runtime Check (1 minute)**
```bash
# Check Python runtime
cat runtime.txt  # Should be python-3.11

# Check Node.js version
node --version   # Should match package.json engines

# Check virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment active"
else
    echo "⚠️ No virtual environment found"
fi
```

**✅ Must Pass**: Runtime versions are compatible

---

### **Critical Issues to Check**

#### **❌ FastAPI + python-multipart Conflict**
```bash
# Check for this pattern in requirements.txt
grep "fastapi==0.111.0" requirements.txt
grep "python-multipart==0.0.6" requirements.txt
```
**Fix**: Use `fastapi==0.78.0` and `python-multipart>=0.0.7`

#### **❌ FastAPI + Pydantic Conflict**
```bash
# Check for this pattern in requirements.txt
grep "fastapi==0.78.0" requirements.txt
grep "pydantic==2.7.4" requirements.txt
```
**Fix**: Use `pydantic==1.10.17`

#### **❌ Python 3.13 + Pydantic Conflict**
```bash
# Check runtime.txt and requirements.txt
cat runtime.txt
grep "pydantic==1.10.13" requirements.txt
```
**Fix**: Use `pydantic==1.10.17` or `python-3.11` in runtime.txt

#### **❌ TypeScript undefined Error**
```bash
# Check for this pattern in TypeScript files
grep -r "setNewComment(undefined)" . --include="*.ts" --include="*.tsx"
```
**Fix**: Use `setNewComment("")` instead

#### **❌ Missing Logger**
```bash
# Check if logger is defined in main.py
grep -n "logger" app/main.py
```
**Fix**: Add `logger = logging.getLogger(__name__)` after imports

---

### **Quick Fix Commands**

#### **Auto-Fix Dependencies**
```bash
bash WHITE_LABEL_UPDATED/scripts/auto-fix-dependencies.sh
```

#### **Auto-Fix TypeScript**
```bash
node WHITE_LABEL_UPDATED/scripts/auto-fix-typescript.js
```

#### **Setup Virtual Environment**
```bash
bash WHITE_LABEL_UPDATED/scripts/setup-virtual-env.sh
```

#### **Run All Checks**
```bash
bash WHITE_LABEL_UPDATED/scripts/check-dependencies.sh
```

---

### **Deployment Steps**

#### **1. Pre-Deployment (5 minutes)**
- [ ] Run dependency checks
- [ ] Run build tests
- [ ] Check runtime compatibility
- [ ] Fix any critical issues

#### **2. Deploy to Staging**
- [ ] Push to staging branch
- [ ] Monitor deployment logs
- [ ] Test health endpoint
- [ ] Verify all features work

#### **3. Deploy to Production**
- [ ] Merge to main branch
- [ ] Monitor deployment logs
- [ ] Test production endpoints
- [ ] Monitor for 24 hours

---

### **Emergency Rollback**

#### **If Deployment Fails**
```bash
# 1. Check deployment logs for specific error
# 2. Identify the issue from checklist above
# 3. Fix the issue locally
# 4. Test the fix
# 5. Redeploy

# If immediate rollback needed
git revert HEAD
git push origin main
```

---

### **Success Criteria**

#### **✅ Deployment Successful When**
- [ ] All dependency checks pass
- [ ] All build tests pass
- [ ] Health endpoint responds with 200
- [ ] Authentication works
- [ ] Core features functional

#### **✅ Ready for Production When**
- [ ] Staging deployment successful
- [ ] All tests passing
- [ ] No critical issues reported
- [ ] Performance acceptable
- [ ] Security scan clean

---

### **Common Issues & Solutions**

| Issue | Detection | Solution |
|-------|-----------|----------|
| Dependency Conflict | `pip check` fails | Run auto-fix script |
| TypeScript Error | `npm run type-check` fails | Run auto-fix script |
| Build Failure | `npm run build` fails | Check for syntax errors |
| Import Error | `python -c "import app.main"` fails | Check for missing imports |
| Runtime Error | App crashes on startup | Check runtime.txt and dependencies |

---

### **Contact & Support**

#### **If Checklist Doesn't Help**
1. **Check the logs**: Look for specific error messages
2. **Run auto-fix scripts**: Try automated solutions
3. **Review documentation**: Check `DEPENDENCY_QUICK_REFERENCE.md`
4. **Contact team**: Alan McCarthy for technical issues

#### **Resources**
- **Full Guide**: `WHITE_LABEL_UPDATED/DEPENDENCY_MANAGEMENT_GUIDE.md`
- **Quick Reference**: `WHITE_LABEL_UPDATED/DEPENDENCY_QUICK_REFERENCE.md`
- **Compatibility Matrix**: `WHITE_LABEL_UPDATED/DEPENDENCY_COMPATIBILITY_MATRIX.md`

---

*This checklist should be used before every deployment to prevent the issues we just encountered.*
