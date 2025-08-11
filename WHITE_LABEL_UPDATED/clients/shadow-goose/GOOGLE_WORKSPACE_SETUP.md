# 🔐 Shadow Goose Entertainment - Google Workspace Setup

## 📋 Team Access Requirements

### **Primary Admin Access:**
- **Alan McCarthy** (Impact Director) - alanmccarthy00@gmail.com
  - **Role:** Full admin access
  - **Permissions:** User management, system administration, analytics

### **Management Access:**
- **Ursula Searle** (Managing Director) - ursula@shadow-goose.com
  - **Role:** Manager access
  - **Permissions:** Project management, team coordination, production oversight

- **Ash Dorman** (Managing Director) - ash@shadow-goose.com
  - **Role:** Manager access
  - **Permissions:** Project management, content creation, stakeholder coordination

### **Creative Access:**
- **Shamita Siva** (Creative Director) - shamita@shadow-goose.com
  - **Role:** Manager access
  - **Permissions:** Content management, creative workflows, project coordination

### **Operations Access:**
- **Mish Rep** (Operations Officer) - mish@shadow-goose.com
  - **Role:** User access
  - **Permissions:** Operational workflows, data management, process efficiency

## 🔧 Google Workspace Setup Steps

### **Step 1: Domain Verification**
- [ ] Verify shadow-goose.com domain ownership
- [ ] Set up Google Workspace for shadow-goose.com
- [ ] Configure DNS records for Google Workspace

### **Step 2: User Account Creation**
- [ ] Create Google Workspace accounts for all team members
- [ ] Set up email addresses:
  - alanmccarthy00@gmail.com (Alan McCarthy - Admin)
  - ursula@shadow-goose.com
  - ash@shadow-goose.com
  - shamita@shadow-goose.com
  - mish@shadow-goose.com

### **Step 3: SSO Configuration**
- [ ] Configure Google Workspace SSO for NavImpact platform
- [ ] Set up OAuth 2.0 credentials
- [ ] Configure redirect URIs for staging and production
- [ ] Test SSO login flow

### **Step 4: Security Settings**
- [ ] Enable 2-factor authentication (MFA)
- [ ] Set password policy (min 12 characters)
- [ ] Configure session timeout (90-day rotation)
- [ ] Set up admin alerts and monitoring

## 🚀 NavImpact Platform Integration

### **Environment Variables to Set:**
```
# Google Workspace SSO Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://shadow-goose-web-staging.onrender.com/auth/google/callback
GOOGLE_REDIRECT_URI_PROD=https://shadow-goose-web.onrender.com/auth/google/callback

# User Management
ADMIN_EMAILS=alanmccarthy00@gmail.com,ursula@shadow-goose.com,ash@shadow-goose.com
MANAGER_EMAILS=shamita@shadow-goose.com
USER_EMAILS=mish@shadow-goose.com
```

### **SSO Endpoints to Configure:**
- **Staging:** https://shadow-goose-web-staging.onrender.com/auth/google
- **Production:** https://shadow-goose-web.onrender.com/auth/google

## 📧 Email Templates for Team Invitations

### **Admin User Invitation (Alan McCarthy):**
```
Subject: Welcome to Shadow Goose Entertainment - NavImpact Platform Access

Hi Alan,

Welcome to the Shadow Goose Entertainment NavImpact platform!

Your access details:
- Email: alanmccarthy00@gmail.com
- Role: Impact Director (Admin)
- Platform: https://shadow-goose-web-staging.onrender.com
- SSO: Google Workspace login

Please log in with your Google Workspace credentials to access the admin dashboard.

Best regards,
Shadow Goose Entertainment Team
```

### **Manager User Invitations (Ursula, Ash, Shamita):**
```
Subject: Welcome to Shadow Goose Entertainment - NavImpact Platform Access

Hi [Name],

Welcome to the Shadow Goose Entertainment NavImpact platform!

Your access details:
- Email: [email]@shadow-goose.com
- Role: [Role] (Manager)
- Platform: https://shadow-goose-web-staging.onrender.com
- SSO: Google Workspace login

Please log in with your Google Workspace credentials to access project management features.

Best regards,
Shadow Goose Entertainment Team
```

### **User Invitation (Mish Rep):**
```
Subject: Welcome to Shadow Goose Entertainment - NavImpact Platform Access

Hi Mish,

Welcome to the Shadow Goose Entertainment NavImpact platform!

Your access details:
- Email: mish@shadow-goose.com
- Role: Operations Officer (User)
- Platform: https://shadow-goose-web-staging.onrender.com
- SSO: Google Workspace login

Please log in with your Google Workspace credentials to access operational workflows.

Best regards,
Shadow Goose Entertainment Team
```

## 🔍 Testing Checklist

### **SSO Testing:**
- [ ] All users can log in with Google Workspace credentials
- [ ] Role-based access control working correctly
- [ ] Session management and timeout functioning
- [ ] Logout functionality working
- [ ] Password policy enforcement active

### **User Management Testing:**
- [ ] Admin can view all users
- [ ] Admin can manage user roles
- [ ] Admin can create/edit/delete users
- [ ] Users can update their profiles
- [ ] Email notifications working

### **Security Testing:**
- [ ] 2FA enforcement working
- [ ] Session timeout functioning
- [ ] Secure token handling
- [ ] CORS configuration correct
- [ ] No security vulnerabilities

## 📞 Support Contacts

**For Google Workspace Issues:**
- **Primary:** Alan McCarthy (alanmccarthy00@gmail.com)
- **Backup:** Shadow Goose IT Support

**For NavImpact Platform Issues:**
- **Primary:** Alan McCarthy (alanmccarthy00@gmail.com)
- **Slack:** #dev-uat channel
- **SLA:** 1 business day response

## 🎯 Next Steps

1. **Provide Google Workspace Admin Access** to set up accounts
2. **Configure SSO credentials** for NavImpact platform
3. **Send team invitations** with login instructions
4. **Begin UAT testing** with real user accounts
5. **Monitor and support** during testing phase

**Ready to proceed with Google Workspace setup!** 🚀
