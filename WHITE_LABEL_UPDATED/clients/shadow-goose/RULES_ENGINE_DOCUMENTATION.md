# 🎯 Shadow Goose Rules Engine Documentation

## 📋 **Overview**

The Shadow Goose Rules Engine is a comprehensive business logic automation system that allows you to create, manage, and execute JSON-based rules for automated decision-making, workflows, and business processes.

### **Key Features:**
- ✅ **JSON-based Rules**: Easy to create and modify rules
- ✅ **Condition Evaluation**: Multiple operators for complex logic
- ✅ **Action Execution**: Automated actions based on conditions
- ✅ **Rule Types**: Project approval, notifications, user access, workflows
- ✅ **Admin Interface**: Web-based rule management
- ✅ **API Integration**: RESTful API for rule operations

---

## 🏗️ **Architecture**

### **Core Components:**
1. **Rules Engine** (`app/rules_engine.py`)
   - Rule evaluation and execution
   - Condition operators and logic
   - Action handlers and automation

2. **API Endpoints** (`app/main.py`)
   - Rule management (CRUD operations)
   - Rule processing and testing
   - Rule type and operator information

3. **Frontend Interface** (`pages/rules.tsx`)
   - Rule visualization and management
   - Rule creation and editing
   - Statistics and monitoring

---

## 📊 **Rule Structure**

### **Basic Rule Format:**
```json
{
  "name": "Rule Name",
  "rule_type": "project_approval",
  "description": "Rule description",
  "conditions": [
    {
      "field": "project_amount",
      "operator": "greater_than",
      "value": 10000
    }
  ],
  "actions": [
    {
      "type": "require_approval",
      "params": {
        "approver_role": "admin",
        "entity_type": "project",
        "entity_id": "{project_id}"
      }
    }
  ]
}
```

### **Rule Types:**
- **project_approval**: Project creation and approval workflows
- **grant_matching**: Grant recommendation and matching
- **user_access**: User permission and assignment rules
- **notification**: Automated alerts and notifications
- **workflow**: Process automation and triggers
- **compliance**: Regulatory and policy compliance

### **Condition Operators:**
- **equals**: Exact match
- **not_equals**: Not equal to
- **greater_than**: Numeric comparison
- **less_than**: Numeric comparison
- **greater_equal**: Numeric comparison
- **less_equal**: Numeric comparison
- **contains**: String/array contains
- **not_contains**: String/array does not contain
- **in**: Value in list
- **not_in**: Value not in list
- **regex**: Regular expression match
- **exists**: Field exists
- **not_exists**: Field does not exist

### **Action Types:**
- **send_notification**: Email, Slack, or other notifications
- **update_status**: Change entity status
- **require_approval**: Trigger approval workflow
- **assign_user**: Assign user to entity
- **create_task**: Create new task
- **update_project**: Modify project data
- **log_event**: Log system events
- **trigger_workflow**: Start automated workflow

---

## 🚀 **Default Rules**

### **1. High Value Project Approval**
```json
{
  "name": "High Value Project Approval",
  "rule_type": "project_approval",
  "description": "Require admin approval for projects over $10,000",
  "conditions": [
    {
      "field": "project_amount",
      "operator": "greater_than",
      "value": 10000
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
        "entity_type": "project",
        "entity_id": "{project_id}"
      }
    },
    {
      "type": "send_notification",
      "params": {
        "type": "email",
        "recipient": "admin@shadow-goose.com",
        "message": "High value project requires approval"
      }
    }
  ]
}
```

### **2. Grant Deadline Alert**
```json
{
  "name": "Grant Deadline Alert",
  "rule_type": "notification",
  "description": "Send alerts for grants closing within 7 days",
  "conditions": [
    {
      "field": "grant_deadline",
      "operator": "less_equal",
      "value": "{datetime.now() + timedelta(days=7)}"
    },
    {
      "field": "grant_status",
      "operator": "equals",
      "value": "active"
    }
  ],
  "actions": [
    {
      "type": "send_notification",
      "params": {
        "type": "slack",
        "recipient": "#grants",
        "message": "Grant {grant_name} closes in 7 days"
      }
    }
  ]
}
```

### **3. New User Assignment**
```json
{
  "name": "New User Assignment",
  "rule_type": "user_access",
  "description": "Assign new users to default projects",
  "conditions": [
    {
      "field": "user_role",
      "operator": "equals",
      "value": "user"
    },
    {
      "field": "user_projects",
      "operator": "equals",
      "value": 0
    }
  ],
  "actions": [
    {
      "type": "assign_user",
      "params": {
        "user_id": "{user_id}",
        "role": "member",
        "entity_type": "project",
        "entity_id": "default"
      }
    }
  ]
}
```

---

## 🔧 **API Endpoints**

### **Rule Management:**
- `GET /api/rules` - Get all rules (admin only)
- `POST /api/rules` - Create new rule (admin only)
- `GET /api/rules/types` - Get available rule types and operators
- `GET /api/rules/examples` - Get example rules

### **Rule Processing:**
- `POST /api/rules/process` - Process rules against context
- `POST /api/rules/test` - Test rule against context

### **Example Usage:**
```bash
# Get all rules
curl -H "Authorization: Bearer TOKEN" \
  https://shadow-goose-api-staging.onrender.com/api/rules

# Process rules
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"context": {"project_amount": 15000, "user_role": "manager"}}' \
  https://shadow-goose-api-staging.onrender.com/api/rules/process
```

---

## 🎨 **Frontend Interface**

### **Access:**
- URL: https://shadow-goose-web-staging.onrender.com/rules
- Admin access required
- Navigate from Dashboard → "Rules Engine" button

### **Features:**
- **Rule Statistics**: Total rules, rule types, action types
- **Rule Management**: View, create, and manage rules
- **Rule Creation**: Form-based rule creation
- **Rule Testing**: Test rules against contexts

### **Navigation:**
1. Login as admin user (`test` / `test`)
2. Go to Dashboard
3. Click "Rules Engine" button (orange)
4. Manage and create rules

---

## 📈 **Use Cases**

### **1. Project Approval Workflows**
- Automatic approval for low-value projects
- Admin approval required for high-value projects
- Notification to stakeholders on approval decisions

### **2. Grant Management**
- Deadline alerts for upcoming grant deadlines
- Automatic grant matching based on criteria
- Status updates and notifications

### **3. User Management**
- Automatic user assignment to projects
- Role-based access control
- Permission management

### **4. Compliance & Reporting**
- Regulatory compliance checks
- Automated reporting triggers
- Audit trail creation

---

## 🔄 **Integration Examples**

### **Project Creation with Rules:**
```python
# When creating a project, rules are automatically processed
project_data = {
    "name": "New Project",
    "amount": 15000,
    "user_role": "manager"
}

# Rules engine processes the context
context = {
    "project_id": project.id,
    "project_amount": project_data.amount,
    "user_role": current_user.role,
    "project_status": "draft"
}

# Rules are evaluated and actions executed
results = rules_engine.process_rules(context, ["project_approval"])
```

### **Notification Integration:**
```python
# Rules can trigger various notification types
notification_rule = {
    "type": "send_notification",
    "params": {
        "type": "slack",
        "recipient": "#alerts",
        "message": "High-value project created"
    }
}
```

---

## 🛠️ **Development & Testing**

### **Testing Rules:**
```bash
# Test a rule against context
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "rule_data": {
      "name": "Test Rule",
      "rule_type": "project_approval",
      "conditions": [{"field": "amount", "operator": "greater_than", "value": 1000}],
      "actions": [{"type": "send_notification", "params": {"type": "email", "recipient": "test@example.com"}}]
    },
    "context_data": {
      "context": {"amount": 1500}
    }
  }' \
  https://shadow-goose-api-staging.onrender.com/api/rules/test
```

### **Adding Custom Actions:**
```python
# Extend the rules engine with custom actions
def custom_action_handler(params, context):
    # Custom action logic
    return {"custom_action_executed": True}

rules_engine.action_handlers["custom_action"] = custom_action_handler
```

---

## 📊 **Monitoring & Analytics**

### **Rule Execution Metrics:**
- Rules triggered per day
- Action success rates
- Performance metrics
- Error tracking

### **Dashboard Integration:**
- Rule statistics in admin dashboard
- Real-time rule execution status
- Performance monitoring

---

## 🚀 **Future Enhancements**

### **Planned Features:**
- **Visual Rule Builder**: Drag-and-drop rule creation
- **Rule Templates**: Pre-built rule templates
- **Advanced Conditions**: Complex logical operators
- **Scheduled Rules**: Time-based rule execution
- **Rule Versioning**: Rule history and rollback
- **A/B Testing**: Rule performance comparison
- **Machine Learning**: Automated rule optimization

### **Integration Roadmap:**
- **Slack Integration**: Real-time notifications
- **Email Integration**: Automated email workflows
- **Calendar Integration**: Deadline management
- **Reporting Integration**: Automated report generation

---

## 🎯 **Getting Started**

### **Quick Start:**
1. **Access Rules Engine**: Login as admin → Dashboard → Rules Engine
2. **View Default Rules**: See pre-configured rules
3. **Create Test Rule**: Use the form to create a simple rule
4. **Test Rule**: Use the API to test rule execution
5. **Monitor Results**: Check rule execution in logs

### **Next Steps:**
1. **Customize Rules**: Modify default rules for your needs
2. **Add New Rules**: Create rules for specific business processes
3. **Integrate Actions**: Connect with external systems
4. **Monitor Performance**: Track rule effectiveness
5. **Scale Up**: Add more complex rule logic

**The Shadow Goose Rules Engine is now ready for production use!** 🎯
