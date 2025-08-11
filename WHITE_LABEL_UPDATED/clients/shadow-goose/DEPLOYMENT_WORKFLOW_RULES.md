# 🚀 Shadow Goose Deployment Workflow Rules

## 📋 **Overview**

The Shadow Goose Deployment Workflow Rules automate CI/CD pipelines, deployment approvals, and commit management. These rules ensure secure, controlled, and automated deployment processes.

### **Key Features:**
- ✅ **Production Deployment Approval**: Admin approval required for production deployments
- ✅ **Staging Auto-Deploy**: Automatic staging deployment on main branch
- ✅ **Critical Bug Hotfix**: Emergency deployment for critical fixes
- ✅ **Deployment Health Check**: Automatic rollback on failure
- ✅ **Code Review Required**: Mandatory review for non-admin commits
- ✅ **Security Scan Integration**: Security checks before production deployment

---

## 🏗️ **Architecture**

### **Core Components:**
1. **Deployment Rules Engine**: Automated deployment decision-making
2. **Commit Workflow Management**: Code review and approval processes
3. **Health Monitoring**: Deployment status tracking and rollback
4. **Security Integration**: Automated security scanning
5. **Notification System**: Slack/email alerts for deployment events

### **Rule Types:**
- **WORKFLOW**: Deployment and commit automation
- **COMPLIANCE**: Security and regulatory compliance
- **NOTIFICATION**: Automated alerts and notifications

---

## 📊 **Deployment Rules**

### **1. Production Deployment Approval**
```json
{
  "name": "Production Deployment Approval",
  "rule_type": "workflow",
  "description": "Require admin approval for production deployments",
  "conditions": [
    {
      "field": "deployment_environment",
      "operator": "equals",
      "value": "production"
    },
    {
      "field": "user_role",
      "operator": "not_equals",
      "value": "admin"
    }
  ],
  "actions": [
    {
      "type": "require_approval",
      "params": {
        "approver_role": "admin",
        "entity_type": "deployment",
        "entity_id": "{deployment_id}"
      }
    },
    {
      "type": "send_notification",
      "params": {
        "type": "slack",
        "recipient": "#deployments",
        "message": "Production deployment requires admin approval"
      }
    },
    {
      "type": "log_event",
      "params": {
        "event_type": "deployment_approval_required",
        "message": "Production deployment pending approval",
        "level": "warning"
      }
    }
  ]
}
```

**Triggers:**
- Production environment deployment
- Non-admin user attempting deployment

**Actions:**
- Require admin approval
- Send Slack notification
- Log approval event

### **2. Staging Auto-Deploy**
```json
{
  "name": "Staging Auto-Deploy",
  "rule_type": "workflow",
  "description": "Automatically deploy to staging on main branch push",
  "conditions": [
    {
      "field": "branch_name",
      "operator": "equals",
      "value": "main"
    },
    {
      "field": "deployment_environment",
      "operator": "equals",
      "value": "staging"
    },
    {
      "field": "commit_message",
      "operator": "contains",
      "value": "feat:"
    }
  ],
  "actions": [
    {
      "type": "trigger_workflow",
      "params": {
        "workflow_name": "staging_deploy",
        "workflow_params": {
          "environment": "staging",
          "auto_deploy": true
        }
      }
    },
    {
      "type": "send_notification",
      "params": {
        "type": "slack",
        "recipient": "#deployments",
        "message": "Auto-deploying to staging: {commit_message}"
      }
    }
  ]
}
```

**Triggers:**
- Main branch push
- Staging environment
- Feature commit message

**Actions:**
- Trigger staging deployment workflow
- Send deployment notification

### **3. Critical Bug Hotfix**
```json
{
  "name": "Critical Bug Hotfix",
  "rule_type": "workflow",
  "description": "Emergency deployment for critical bug fixes",
  "conditions": [
    {
      "field": "commit_message",
      "operator": "contains",
      "value": "hotfix:"
    },
    {
      "field": "priority",
      "operator": "equals",
      "value": "critical"
    }
  ],
  "actions": [
    {
      "type": "trigger_workflow",
      "params": {
        "workflow_name": "emergency_deploy",
        "workflow_params": {
          "environment": "production",
          "skip_tests": true,
          "emergency": true
        }
      }
    },
    {
      "type": "send_notification",
      "params": {
        "type": "slack",
        "recipient": "#alerts",
        "message": "🚨 CRITICAL: Emergency deployment for hotfix"
      }
    },
    {
      "type": "log_event",
      "params": {
        "event_type": "emergency_deployment",
        "message": "Critical hotfix deployment initiated",
        "level": "critical"
      }
    }
  ]
}
```

**Triggers:**
- Hotfix commit message
- Critical priority flag

**Actions:**
- Emergency production deployment
- Skip tests for speed
- Critical alert notification

### **4. Deployment Health Check**
```json
{
  "name": "Deployment Health Check",
  "rule_type": "workflow",
  "description": "Monitor deployment health and rollback if needed",
  "conditions": [
    {
      "field": "deployment_status",
      "operator": "equals",
      "value": "failed"
    },
    {
      "field": "deployment_environment",
      "operator": "equals",
      "value": "production"
    }
  ],
  "actions": [
    {
      "type": "trigger_workflow",
      "params": {
        "workflow_name": "rollback_deployment",
        "workflow_params": {
          "environment": "production",
          "reason": "health_check_failed"
        }
      }
    },
    {
      "type": "send_notification",
      "params": {
        "type": "slack",
        "recipient": "#alerts",
        "message": "🚨 DEPLOYMENT FAILED: Initiating rollback"
      }
    },
    {
      "type": "log_event",
      "params": {
        "event_type": "deployment_rollback",
        "message": "Production deployment failed, rolling back",
        "level": "error"
      }
    }
  ]
}
```

**Triggers:**
- Failed deployment status
- Production environment

**Actions:**
- Trigger rollback workflow
- Send failure alert
- Log rollback event

---

## 📝 **Commit Rules**

### **5. Code Review Required**
```json
{
  "name": "Code Review Required",
  "rule_type": "workflow",
  "description": "Require code review for non-admin commits",
  "conditions": [
    {
      "field": "user_role",
      "operator": "not_equals",
      "value": "admin"
    },
    {
      "field": "branch_name",
      "operator": "equals",
      "value": "main"
    }
  ],
  "actions": [
    {
      "type": "require_approval",
      "params": {
        "approver_role": "admin",
        "entity_type": "pull_request",
        "entity_id": "{pr_id}"
      }
    },
    {
      "type": "send_notification",
      "params": {
        "type": "slack",
        "recipient": "#code-review",
        "message": "Code review required for main branch commit"
      }
    }
  ]
}
```

**Triggers:**
- Non-admin user
- Main branch commit

**Actions:**
- Require admin approval
- Send review notification

### **6. Security Scan on Deploy**
```json
{
  "name": "Security Scan on Deploy",
  "rule_type": "compliance",
  "description": "Run security scans before production deployment",
  "conditions": [
    {
      "field": "deployment_environment",
      "operator": "equals",
      "value": "production"
    },
    {
      "field": "security_scan_status",
      "operator": "not_equals",
      "value": "passed"
    }
  ],
  "actions": [
    {
      "type": "trigger_workflow",
      "params": {
        "workflow_name": "security_scan",
        "workflow_params": {
          "scan_type": "full",
          "block_deploy": true
        }
      }
    },
    {
      "type": "send_notification",
      "params": {
        "type": "slack",
        "recipient": "#security",
        "message": "Security scan required before production deploy"
      }
    }
  ]
}
```

**Triggers:**
- Production deployment
- Security scan not passed

**Actions:**
- Trigger security scan
- Block deployment until passed
- Send security notification

---

## 🔧 **API Endpoints**

### **Deployment Management:**
- `POST /api/deployments` - Create new deployment
- `GET /api/deployments` - Get all deployments (admin only)
- `POST /api/deployments/{id}/status` - Update deployment status

### **Commit Management:**
- `POST /api/commits` - Create new commit
- `GET /api/commits` - Get all commits (admin only)

### **Example Usage:**
```bash
# Create production deployment
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "environment": "production",
    "branch_name": "main",
    "commit_message": "feat: new feature",
    "priority": "normal",
    "security_scan_status": "pending"
  }' \
  https://shadow-goose-api-staging.onrender.com/api/deployments

# Create commit
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "branch_name": "main",
    "commit_message": "feat: add new feature",
    "pr_id": "123"
  }' \
  https://shadow-goose-api-staging.onrender.com/api/commits
```

---

## 🎨 **Frontend Interface**

### **Access:**
- URL: https://shadow-goose-web-staging.onrender.com/deployments
- Admin access required
- Navigate from Dashboard → "Deployments" button

### **Features:**
- **Deployment Management**: Create and track deployments
- **Commit Tracking**: Monitor commit history
- **Status Monitoring**: Real-time deployment status
- **Statistics**: Deployment metrics and analytics

### **Navigation:**
1. Login as admin user (`test` / `test`)
2. Go to Dashboard
3. Click "Deployments" button (indigo)
4. Manage deployments and commits

---

## 📈 **Use Cases**

### **1. Production Deployment Workflow**
```
Developer → Create Deployment → Rules Engine → Admin Approval → Deploy → Health Check
```

### **2. Staging Auto-Deploy**
```
Git Push → Main Branch → Rules Engine → Auto-Deploy Staging → Notification
```

### **3. Emergency Hotfix**
```
Critical Bug → Hotfix Commit → Rules Engine → Emergency Deploy → Alert Team
```

### **4. Security Compliance**
```
Production Deploy → Security Scan → Pass/Fail → Deploy/Block → Log Event
```

---

## 🔄 **Integration Examples**

### **GitHub Actions Integration:**
```yaml
name: Deploy to Staging
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Staging
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"environment": "staging", "branch_name": "main", "commit_message": "${{ github.event.head_commit.message }}"}' \
            ${{ secrets.API_URL }}/api/deployments
```

### **Slack Integration:**
```python
# Rules engine automatically sends notifications
notification_rule = {
    "type": "send_notification",
    "params": {
        "type": "slack",
        "recipient": "#deployments",
        "message": "🚀 Deployment successful: {deployment_id}"
    }
}
```

---

## 🛠️ **Development & Testing**

### **Testing Deployment Rules:**
```bash
# Test production deployment approval
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "deployment_environment": "production",
      "user_role": "developer",
      "commit_message": "feat: new feature"
    }
  }' \
  https://shadow-goose-api-staging.onrender.com/api/rules/process
```

### **Testing Commit Rules:**
```bash
# Test code review requirement
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "branch_name": "main",
      "user_role": "developer",
      "commit_message": "feat: new feature"
    }
  }' \
  https://shadow-goose-api-staging.onrender.com/api/rules/process
```

---

## 📊 **Monitoring & Analytics**

### **Deployment Metrics:**
- Deployment success rate
- Average deployment time
- Rollback frequency
- Security scan pass rate

### **Commit Metrics:**
- Code review compliance
- Commit frequency by user
- Branch protection effectiveness
- PR approval time

---

## 🚀 **Future Enhancements**

### **Planned Features:**
- **Blue-Green Deployments**: Zero-downtime deployment strategy
- **Canary Deployments**: Gradual rollout with monitoring
- **Automated Testing**: Integration with test suites
- **Performance Monitoring**: Real-time performance tracking
- **Cost Optimization**: Resource usage optimization
- **Multi-Environment**: Support for multiple environments

### **Integration Roadmap:**
- **GitHub/GitLab**: Direct repository integration
- **Jenkins/CircleCI**: CI/CD platform integration
- **Kubernetes**: Container orchestration
- **Terraform**: Infrastructure as code
- **Prometheus**: Metrics and monitoring
- **Grafana**: Visualization and dashboards

---

## 🎯 **Getting Started**

### **Quick Start:**
1. **Access Deployments**: Login as admin → Dashboard → Deployments
2. **Create Test Deployment**: Use the form to create a staging deployment
3. **Test Rules**: Create commits and deployments to trigger rules
4. **Monitor Results**: Check rule execution in the interface
5. **Review Logs**: Monitor deployment and commit history

### **Next Steps:**
1. **Configure Environments**: Set up staging and production
2. **Customize Rules**: Modify rules for your workflow
3. **Integrate CI/CD**: Connect with your existing pipeline
4. **Set Up Monitoring**: Configure alerts and dashboards
5. **Train Team**: Educate team on new workflow

**The Shadow Goose Deployment Workflow Rules are now ready for production use!** 🚀
