# Quick Test Script - Shadow Goose

## 🚀 **5-Minute System Verification**

### **Step 1: Backend API Test**
```bash
# Test API health
curl -s https://shadow-goose-api-staging.onrender.com/health
# Expected: {"status":"ok","version":"4.2.0"}

# Test database status
curl -s https://shadow-goose-api-staging.onrender.com/api/database-status
# Expected: {"database_url_configured":true,"database_url_length":107,"ready_for_database_integration":true}
```

### **Step 2: Frontend Test**
```bash
# Test frontend accessibility
curl -s -o /dev/null -w "Frontend Status: %{http_code}\n" https://shadow-goose-web-staging.onrender.com
# Expected: Frontend Status: 200

# Test login page
curl -s https://shadow-goose-web-staging.onrender.com/login | grep -o "Shadow Goose Entertainment"
# Expected: Shadow Goose Entertainment
```

### **Step 3: Manual Testing**
1. **Open Browser**: https://shadow-goose-web-staging.onrender.com
2. **Click "Sign In"**
3. **Login**: username: `test`, password: `test`
4. **Verify Dashboard**: Should show "Welcome, test (admin)"
5. **Test User Management**: Click purple "User Management" button
6. **Test Project Creation**: Click "Create New Project"

### **Step 4: API Testing**
```bash
# Test login API
curl -X POST https://shadow-goose-api-staging.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
# Expected: {"access_token":"...","token_type":"bearer","user":{...}}

# Test projects API (replace TOKEN with actual token)
curl -H "Authorization: Bearer TOKEN" \
  https://shadow-goose-api-staging.onrender.com/api/projects
# Expected: {"projects":[...]}
```

---

## ✅ **Success Criteria**

### **All Tests Pass = System Ready for UAT**
- [ ] Backend API responds with v4.2.0
- [ ] Database status shows configured
- [ ] Frontend loads successfully
- [ ] Login page displays branding
- [ ] Manual login works
- [ ] Dashboard displays correctly
- [ ] User management accessible (admin only)
- [ ] Project creation works

### **If Any Test Fails**
1. Check deployment status on Render
2. Verify environment variables
3. Check GitHub for latest code
4. Contact support if needed

---

## 🎯 **Ready for Phase 4: UAT**

**System Status**: ✅ **READY**
**Next Action**: Begin UAT testing with the comprehensive checklist
**Timeline**: 5-8 days to production go-live
