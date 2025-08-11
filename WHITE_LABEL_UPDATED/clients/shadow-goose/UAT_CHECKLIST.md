# 🧪 Shadow Goose Entertainment - UAT Checklist

## 📋 UAT Overview
- **Environment:** Staging (https://shadow-goose-web-staging.onrender.com)
- **Timeline:** 15–22 September 2025
- **Triage Channel:** Slack #dev-uat
- **Primary Contact:** Alan McCarthy (Impact Director)

## 👥 Test Users

### **Admin User: Alan McCarthy**
- **Email:** alanmccarthy00@gmail.com
- **Role:** Impact Director
- **Access Level:** Full admin privileges
- **Testing Focus:** System administration, user management, analytics

### **Manager User: Ursula Searle**
- **Email:** ursula@shadow-goose.com
- **Role:** Managing Director
- **Access Level:** Create/edit projects, manage team
- **Testing Focus:** Project management, team coordination, production oversight

### **Manager User: Ash Dorman**
- **Email:** ash@shadow-goose.com
- **Role:** Managing Director
- **Access Level:** Create/edit projects, manage team
- **Testing Focus:** Project management, content creation, stakeholder coordination

### **Creative User: Shamita Siva**
- **Email:** shamita@shadow-goose.com
- **Role:** Creative Director
- **Access Level:** Create/edit projects, manage creative content
- **Testing Focus:** Content management, creative workflows, project coordination

### **Operations User: Mish Rep**
- **Email:** mish@shadow-goose.com
- **Role:** Operations Officer
- **Access Level:** View/edit assigned items, operational tasks
- **Testing Focus:** Operational workflows, data management, process efficiency

## ✅ UAT Test Categories

### **1. Branding & UI/UX**
- [ ] **Branding Display**
  - [ ] "Shadow Goose Entertainment" appears correctly
  - [ ] Colors match brand guidelines (Primary #1A1A1A, Accent #FF6600)
  - [ ] Fonts display correctly (Poppins headings, Open Sans body)
  - [ ] Logo/favicon displays properly

- [ ] **Responsive Design**
  - [ ] Mobile optimization (test on iPhone, Android)
  - [ ] Tablet optimization (test on iPad)
  - [ ] Desktop optimization (test on Mac, Windows)
  - [ ] Cross-browser compatibility (Chrome, Safari, Firefox, Edge)

### **2. Authentication & Access**
- [ ] **Google Workspace SSO**
  - [ ] Login with Google Workspace credentials
  - [ ] Role-based access control (Admin, Manager, User)
  - [ ] Password policy enforcement (min 12 chars, MFA)
  - [ ] Session management and timeout

- [ ] **User Management**
  - [ ] Admin can create/edit/delete users
  - [ ] Role assignment and permissions
  - [ ] User profile management

### **3. Core Functionality**
- [ ] **Grant Management**
  - [ ] Create new grant applications
  - [ ] Edit existing grant entries
  - [ ] Grant status tracking
  - [ ] Document upload/management

- [ ] **Project Management**
  - [ ] Create new projects
  - [ ] Assign team members
  - [ ] Project timeline tracking
  - [ ] Milestone management

### **4. Performance & Technical**
- [ ] **API Performance**
  - [ ] API latency <200ms (as per acceptance criteria)
  - [ ] Database connection stability
  - [ ] Health check endpoints responding

- [ ] **Security**
  - [ ] Data encryption in transit
  - [ ] Secure session handling
  - [ ] CORS configuration working
  - [ ] No security vulnerabilities

### **5. Integrations**
- [ ] **Slack Integration**
  - [ ] Notifications to #dev-uat channel
  - [ ] Error reporting and alerts
  - [ ] User activity notifications

- [ ] **Notion Integration** (Shadow Goose HQ)
  - [ ] Data sync between platforms
  - [ ] Document sharing
  - [ ] Project updates

### **6. Analytics & Monitoring**
- [ ] **Frontend Analytics**
  - [ ] User behavior tracking
  - [ ] Page view analytics
  - [ ] Performance metrics

- [ ] **Sentry Monitoring**
  - [ ] Error tracking and reporting
  - [ ] Performance monitoring
  - [ ] Alert notifications to Alan McCarthy

## 🐛 Bug Reporting Template

**Bug Report Format:**
```
**Environment:** Staging
**User Role:** [Admin/Manager/User]
**Browser:** [Chrome/Safari/Firefox/Edge]
**Device:** [Desktop/Mobile/Tablet]
**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
**Expected Result:** [What should happen]
**Actual Result:** [What actually happened]
**Priority:** [High/Medium/Low]
**Screenshots:** [If applicable]
```

## 📊 UAT Success Criteria

### **Must-Have (Critical)**
- [ ] All users can log in successfully
- [ ] Branding displays correctly across all devices
- [ ] API response time <200ms
- [ ] No critical security vulnerabilities
- [ ] Core grant management features work

### **Should-Have (Important)**
- [ ] Mobile optimization working
- [ ] Integrations (Slack, Notion) functional
- [ ] Analytics tracking active
- [ ] User management working

### **Nice-to-Have (Optional)**
- [ ] Advanced reporting features
- [ ] Custom dashboard configurations
- [ ] Bulk import/export functionality

## 🚨 Escalation Process

**For Critical Issues:**
1. **Immediate:** Contact Alan McCarthy (alanmccarthy00@gmail.com)
2. **Slack:** Post in #dev-uat with @here
3. **Response Time:** 1 business day SLA

**For Non-Critical Issues:**
1. **Document:** Add to bug tracking
2. **Prioritize:** Based on impact and effort
3. **Schedule:** Fix in next sprint

## 📅 UAT Schedule

**Week 1 (15-19 September):**
- **Day 1:** Branding & UI/UX testing
- **Day 2:** Authentication & user management
- **Day 3:** Core functionality testing
- **Day 4:** Performance & security testing
- **Day 5:** Integration testing

**Week 2 (20-22 September):**
- **Day 6:** Analytics & monitoring
- **Day 7:** Final regression testing
- **Day 8:** UAT sign-off and go-live preparation

## ✅ UAT Sign-Off Checklist

- [ ] All critical bugs resolved
- [ ] Performance criteria met
- [ ] Security audit passed
- [ ] User acceptance confirmed
- [ ] Production deployment ready
- [ ] Support documentation complete

**UAT Sign-Off By:** Alan McCarthy (Impact Director)
**Date:** [To be completed]
**Status:** [In Progress/Complete]
