# 🚀 Shadow Goose - Quick UAT Test

## ⚡ Immediate Testing (Can be done now)

### **1. Branding Verification**
**Test URL:** https://shadow-goose-web-staging.onrender.com

**✅ Expected Results:**
- [ ] Page loads without errors
- [ ] "Shadow Goose Entertainment" displays correctly
- [ ] Colors: Primary #1A1A1A, Accent #FF6600
- [ ] Fonts: Poppins (headings), Open Sans (body)
- [ ] Responsive design works on mobile/desktop

### **2. API Health Check**
**Test URLs:**
- [ ] https://shadow-goose-api-staging.onrender.com/health
- [ ] https://shadow-goose-web-staging.onrender.com/api/health

**✅ Expected Results:**
- [ ] Both return `{"status":"ok"}`
- [ ] Response time <200ms

### **3. Cross-Browser Testing**
**Test these browsers:**
- [ ] Chrome (desktop & mobile)
- [ ] Safari (desktop & mobile)
- [ ] Firefox (desktop)
- [ ] Edge (desktop)

### **4. Mobile Responsiveness**
**Test on:**
- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] iPad (Safari)
- [ ] Various screen sizes

## 🧪 Manual Test Scenarios

### **Scenario 1: First-Time User**
1. Visit staging URL
2. Verify branding loads correctly
3. Check mobile responsiveness
4. Test page load speed

### **Scenario 2: Admin User (Alan McCarthy)**
1. Login with Google Workspace credentials (alanmccarthy00@gmail.com)
2. Access admin dashboard
3. Test user management features
4. Verify analytics access

### **Scenario 3: Managing Director (Ursula Searle)**
1. Login with Google Workspace credentials (ursula@shadow-goose.com)
2. Create a new project
3. Assign team members
4. Test project management features

### **Scenario 4: Managing Director (Ash Dorman)**
1. Login with Google Workspace credentials (ash@shadow-goose.com)
2. Create content projects
3. Manage stakeholder coordination
4. Test content management features

### **Scenario 5: Creative Director (Shamita Siva)**
1. Login with Google Workspace credentials (shamita@shadow-goose.com)
2. Manage creative content
3. Coordinate creative workflows
4. Test content management features

### **Scenario 6: Operations Officer (Mish Rep)**
1. Login with Google Workspace credentials (mish@shadow-goose.com)
2. View assigned operational tasks
3. Manage data and processes
4. Test operational workflows

## 📱 Mobile Testing Checklist

### **iPhone Testing:**
- [ ] Safari browser works correctly
- [ ] Touch interactions responsive
- [ ] Text readable without zooming
- [ ] Navigation intuitive

### **Android Testing:**
- [ ] Chrome browser works correctly
- [ ] Touch interactions responsive
- [ ] Text readable without zooming
- [ ] Navigation intuitive

### **Tablet Testing:**
- [ ] iPad Safari works correctly
- [ ] Landscape and portrait modes
- [ ] Touch interactions responsive
- [ ] Content properly scaled

## 🐛 Common Issues to Watch For

### **Critical Issues:**
- [ ] Page doesn't load
- [ ] Branding not displaying
- [ ] API errors
- [ ] Security vulnerabilities

### **Medium Priority:**
- [ ] Slow page load times
- [ ] Mobile layout issues
- [ ] Cross-browser compatibility
- [ ] Authentication problems

### **Low Priority:**
- [ ] Minor styling issues
- [ ] Console warnings
- [ ] Performance optimizations

## 📊 Test Results Template

```
**Test Date:** [Date]
**Tester:** [Name]
**Environment:** Staging
**Browser/Device:** [Details]

**Results:**
✅ Passed: [List passed tests]
❌ Failed: [List failed tests]
⚠️ Issues: [List issues found]

**Overall Status:** [Pass/Fail/Needs Improvement]
**Recommendation:** [Go/No-Go for production]
```

## 🚨 Immediate Action Items

**If Issues Found:**
1. **Document:** Use bug report template
2. **Prioritize:** Critical > Medium > Low
3. **Escalate:** Contact Alan McCarthy for critical issues
4. **Track:** Add to UAT tracking spreadsheet

**If All Tests Pass:**
1. **Sign-off:** Complete UAT checklist
2. **Schedule:** Production deployment
3. **Prepare:** Team onboarding materials
4. **Plan:** Go-live celebration! 🎉

## 👥 Shadow Goose Team Contact Info

**Primary Contact:**
- **Alan McCarthy** (Impact Director) - alanmccarthy00@gmail.com

**Test Users:**
- **Ursula Searle** (Managing Director) - ursula@shadow-goose.com
- **Ash Dorman** (Managing Director) - ash@shadow-goose.com
- **Shamita Siva** (Creative Director) - shamita@shadow-goose.com
- **Mish Rep** (Operations Officer) - mish@shadow-goose.com

**Support Channel:** Slack #dev-uat
