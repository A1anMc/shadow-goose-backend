import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class RuleType(Enum):
    PROJECT_APPROVAL = "project_approval"
    GRANT_MATCHING = "grant_matching"
    USER_ACCESS = "user_access"
    NOTIFICATION = "notification"
    WORKFLOW = "workflow"
    COMPLIANCE = "compliance"

class ConditionOperator(Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_EQUAL = "greater_equal"
    LESS_EQUAL = "less_equal"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"
    REGEX = "regex"
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"

class ActionType(Enum):
    SEND_NOTIFICATION = "send_notification"
    UPDATE_STATUS = "update_status"
    REQUIRE_APPROVAL = "require_approval"
    ASSIGN_USER = "assign_user"
    CREATE_TASK = "create_task"
    UPDATE_PROJECT = "update_project"
    LOG_EVENT = "log_event"
    TRIGGER_WORKFLOW = "trigger_workflow"

class RulesEngine:
    def __init__(self):
        self.rules: List[Dict] = []
        self.context: Dict[str, Any] = {}
        self.action_handlers: Dict[str, callable] = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default action handlers"""
        self.action_handlers = {
            ActionType.SEND_NOTIFICATION.value: self._send_notification,
            ActionType.UPDATE_STATUS.value: self._update_status,
            ActionType.REQUIRE_APPROVAL.value: self._require_approval,
            ActionType.ASSIGN_USER.value: self._assign_user,
            ActionType.CREATE_TASK.value: self._create_task,
            ActionType.UPDATE_PROJECT.value: self._update_project,
            ActionType.LOG_EVENT.value: self._log_event,
            ActionType.TRIGGER_WORKFLOW.value: self._trigger_workflow
        }
    
    def add_rule(self, rule: Dict) -> bool:
        """Add a new rule to the engine"""
        try:
            self._validate_rule(rule)
            self.rules.append(rule)
            logger.info(f"Added rule: {rule.get('name', 'unnamed')}")
            return True
        except Exception as e:
            logger.error(f"Failed to add rule: {e}")
            return False
    
    def _validate_rule(self, rule: Dict):
        """Validate rule structure"""
        required_fields = ['name', 'rule_type', 'conditions', 'actions']
        for field in required_fields:
            if field not in rule:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(rule['conditions'], list):
            raise ValueError("Conditions must be a list")
        
        if not isinstance(rule['actions'], list):
            raise ValueError("Actions must be a list")
    
    def evaluate_conditions(self, conditions: List[Dict], context: Dict) -> bool:
        """Evaluate all conditions against the context"""
        for condition in conditions:
            if not self._evaluate_condition(condition, context):
                return False
        return True
    
    def _evaluate_condition(self, condition: Dict, context: Dict) -> bool:
        """Evaluate a single condition"""
        field = condition.get('field')
        operator = condition.get('operator')
        value = condition.get('value')
        
        if field not in context:
            return operator == ConditionOperator.NOT_EXISTS.value
        
        context_value = context[field]
        
        try:
            if operator == ConditionOperator.EQUALS.value:
                return context_value == value
            elif operator == ConditionOperator.NOT_EQUALS.value:
                return context_value != value
            elif operator == ConditionOperator.GREATER_THAN.value:
                return context_value > value
            elif operator == ConditionOperator.LESS_THAN.value:
                return context_value < value
            elif operator == ConditionOperator.GREATER_EQUAL.value:
                return context_value >= value
            elif operator == ConditionOperator.LESS_EQUAL.value:
                return context_value <= value
            elif operator == ConditionOperator.CONTAINS.value:
                return value in context_value
            elif operator == ConditionOperator.NOT_CONTAINS.value:
                return value not in context_value
            elif operator == ConditionOperator.IN.value:
                return context_value in value
            elif operator == ConditionOperator.NOT_IN.value:
                return context_value not in value
            elif operator == ConditionOperator.REGEX.value:
                return bool(re.search(value, str(context_value)))
            elif operator == ConditionOperator.EXISTS.value:
                return field in context
            elif operator == ConditionOperator.NOT_EXISTS.value:
                return field not in context
            else:
                logger.warning(f"Unknown operator: {operator}")
                return False
        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False
    
    def execute_actions(self, actions: List[Dict], context: Dict) -> List[Dict]:
        """Execute all actions and return results"""
        results = []
        for action in actions:
            try:
                result = self._execute_action(action, context)
                results.append({
                    'action': action.get('type'),
                    'success': True,
                    'result': result
                })
            except Exception as e:
                logger.error(f"Action execution failed: {e}")
                results.append({
                    'action': action.get('type'),
                    'success': False,
                    'error': str(e)
                })
        return results
    
    def _execute_action(self, action: Dict, context: Dict) -> Any:
        """Execute a single action"""
        action_type = action.get('type')
        params = action.get('params', {})
        
        if action_type in self.action_handlers:
            return self.action_handlers[action_type](params, context)
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return None
    
    def process_rules(self, context: Dict, rule_types: Optional[List[str]] = None) -> List[Dict]:
        """Process all applicable rules against the context"""
        results = []
        
        for rule in self.rules:
            if rule_types and rule.get('rule_type') not in rule_types:
                continue
            
            if self.evaluate_conditions(rule['conditions'], context):
                action_results = self.execute_actions(rule['actions'], context)
                results.append({
                    'rule_name': rule.get('name'),
                    'rule_type': rule.get('rule_type'),
                    'triggered': True,
                    'actions': action_results
                })
        
        return results
    
    # Default action handlers
    def _send_notification(self, params: Dict, context: Dict) -> Dict:
        """Send notification action"""
        notification_type = params.get('type', 'email')
        recipient = params.get('recipient')
        message = params.get('message', '')
        
        # In a real implementation, this would integrate with email/Slack/etc.
        logger.info(f"Sending {notification_type} notification to {recipient}: {message}")
        
        return {
            'notification_sent': True,
            'type': notification_type,
            'recipient': recipient,
            'message': message
        }
    
    def _update_status(self, params: Dict, context: Dict) -> Dict:
        """Update status action"""
        entity_type = params.get('entity_type')
        entity_id = params.get('entity_id')
        new_status = params.get('status')
        
        logger.info(f"Updating {entity_type} {entity_id} status to {new_status}")
        
        return {
            'status_updated': True,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'new_status': new_status
        }
    
    def _require_approval(self, params: Dict, context: Dict) -> Dict:
        """Require approval action"""
        approver_role = params.get('approver_role', 'admin')
        entity_type = params.get('entity_type')
        entity_id = params.get('entity_id')
        
        logger.info(f"Requiring {approver_role} approval for {entity_type} {entity_id}")
        
        return {
            'approval_required': True,
            'approver_role': approver_role,
            'entity_type': entity_type,
            'entity_id': entity_id
        }
    
    def _assign_user(self, params: Dict, context: Dict) -> Dict:
        """Assign user action"""
        user_id = params.get('user_id')
        role = params.get('role')
        entity_type = params.get('entity_type')
        entity_id = params.get('entity_id')
        
        logger.info(f"Assigning user {user_id} with role {role} to {entity_type} {entity_id}")
        
        return {
            'user_assigned': True,
            'user_id': user_id,
            'role': role,
            'entity_type': entity_type,
            'entity_id': entity_id
        }
    
    def _create_task(self, params: Dict, context: Dict) -> Dict:
        """Create task action"""
        title = params.get('title')
        description = params.get('description', '')
        assignee = params.get('assignee')
        due_date = params.get('due_date')
        
        logger.info(f"Creating task: {title} for {assignee}")
        
        return {
            'task_created': True,
            'title': title,
            'description': description,
            'assignee': assignee,
            'due_date': due_date
        }
    
    def _update_project(self, params: Dict, context: Dict) -> Dict:
        """Update project action"""
        project_id = params.get('project_id')
        updates = params.get('updates', {})
        
        logger.info(f"Updating project {project_id} with {updates}")
        
        return {
            'project_updated': True,
            'project_id': project_id,
            'updates': updates
        }
    
    def _log_event(self, params: Dict, context: Dict) -> Dict:
        """Log event action"""
        event_type = params.get('event_type')
        message = params.get('message', '')
        level = params.get('level', 'info')
        
        logger.info(f"Logging event: {event_type} - {message}")
        
        return {
            'event_logged': True,
            'event_type': event_type,
            'message': message,
            'level': level
        }
    
    def _trigger_workflow(self, params: Dict, context: Dict) -> Dict:
        """Trigger workflow action"""
        workflow_name = params.get('workflow_name')
        workflow_params = params.get('workflow_params', {})
        
        logger.info(f"Triggering workflow: {workflow_name}")
        
        return {
            'workflow_triggered': True,
            'workflow_name': workflow_name,
            'workflow_params': workflow_params
        }
    
    def get_default_rules(self) -> List[Dict]:
        """Get default rules for Shadow Goose"""
        return [
            {
                "name": "High Value Project Approval",
                "rule_type": RuleType.PROJECT_APPROVAL.value,
                "description": "Require admin approval for projects over $10,000",
                "conditions": [
                    {
                        "field": "project_amount",
                        "operator": ConditionOperator.GREATER_THAN.value,
                        "value": 10000
                    },
                    {
                        "field": "user_role",
                        "operator": ConditionOperator.NOT_EQUALS.value,
                        "value": "admin"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.REQUIRE_APPROVAL.value,
                        "params": {
                            "approver_role": "admin",
                            "entity_type": "project",
                            "entity_id": "{project_id}"
                        }
                    },
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "email",
                            "recipient": "admin@shadow-goose.com",
                            "message": "High value project requires approval"
                        }
                    }
                ]
            },
            {
                "name": "Grant Deadline Alert",
                "rule_type": RuleType.NOTIFICATION.value,
                "description": "Send alerts for grants closing within 7 days",
                "conditions": [
                    {
                        "field": "grant_deadline",
                        "operator": ConditionOperator.LESS_EQUAL.value,
                        "value": "{datetime.now() + timedelta(days=7)}"
                    },
                    {
                        "field": "grant_status",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "active"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "slack",
                            "recipient": "#grants",
                            "message": "Grant {grant_name} closes in 7 days"
                        }
                    }
                ]
            },
            {
                "name": "New User Assignment",
                "rule_type": RuleType.USER_ACCESS.value,
                "description": "Assign new users to default projects",
                "conditions": [
                    {
                        "field": "user_role",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "user"
                    },
                    {
                        "field": "user_projects",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": 0
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.ASSIGN_USER.value,
                        "params": {
                            "user_id": "{user_id}",
                            "role": "member",
                            "entity_type": "project",
                            "entity_id": "default"
                        }
                    }
                ]
            },
            {
                "name": "Production Deployment Approval",
                "rule_type": RuleType.WORKFLOW.value,
                "description": "Require admin approval for production deployments",
                "conditions": [
                    {
                        "field": "deployment_environment",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "production"
                    },
                    {
                        "field": "user_role",
                        "operator": ConditionOperator.NOT_EQUALS.value,
                        "value": "admin"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.REQUIRE_APPROVAL.value,
                        "params": {
                            "approver_role": "admin",
                            "entity_type": "deployment",
                            "entity_id": "{deployment_id}"
                        }
                    },
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "slack",
                            "recipient": "#deployments",
                            "message": "Production deployment requires admin approval"
                        }
                    },
                    {
                        "type": ActionType.LOG_EVENT.value,
                        "params": {
                            "event_type": "deployment_approval_required",
                            "message": "Production deployment pending approval",
                            "level": "warning"
                        }
                    }
                ]
            },
            {
                "name": "Staging Auto-Deploy",
                "rule_type": RuleType.WORKFLOW.value,
                "description": "Automatically deploy to staging on main branch push",
                "conditions": [
                    {
                        "field": "branch_name",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "main"
                    },
                    {
                        "field": "deployment_environment",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "staging"
                    },
                    {
                        "field": "commit_message",
                        "operator": ConditionOperator.CONTAINS.value,
                        "value": "feat:"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.TRIGGER_WORKFLOW.value,
                        "params": {
                            "workflow_name": "staging_deploy",
                            "workflow_params": {
                                "environment": "staging",
                                "auto_deploy": True
                            }
                        }
                    },
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "slack",
                            "recipient": "#deployments",
                            "message": "Auto-deploying to staging: {commit_message}"
                        }
                    }
                ]
            },
            {
                "name": "Critical Bug Hotfix",
                "rule_type": RuleType.WORKFLOW.value,
                "description": "Emergency deployment for critical bug fixes",
                "conditions": [
                    {
                        "field": "commit_message",
                        "operator": ConditionOperator.CONTAINS.value,
                        "value": "hotfix:"
                    },
                    {
                        "field": "priority",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "critical"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.TRIGGER_WORKFLOW.value,
                        "params": {
                            "workflow_name": "emergency_deploy",
                            "workflow_params": {
                                "environment": "production",
                                "skip_tests": True,
                                "emergency": True
                            }
                        }
                    },
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "slack",
                            "recipient": "#alerts",
                            "message": "🚨 CRITICAL: Emergency deployment for hotfix"
                        }
                    },
                    {
                        "type": ActionType.LOG_EVENT.value,
                        "params": {
                            "event_type": "emergency_deployment",
                            "message": "Critical hotfix deployment initiated",
                            "level": "critical"
                        }
                    }
                ]
            },
            {
                "name": "Deployment Health Check",
                "rule_type": RuleType.WORKFLOW.value,
                "description": "Monitor deployment health and rollback if needed",
                "conditions": [
                    {
                        "field": "deployment_status",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "failed"
                    },
                    {
                        "field": "deployment_environment",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "production"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.TRIGGER_WORKFLOW.value,
                        "params": {
                            "workflow_name": "rollback_deployment",
                            "workflow_params": {
                                "environment": "production",
                                "reason": "health_check_failed"
                            }
                        }
                    },
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "slack",
                            "recipient": "#alerts",
                            "message": "🚨 DEPLOYMENT FAILED: Initiating rollback"
                        }
                    },
                    {
                        "type": ActionType.LOG_EVENT.value,
                        "params": {
                            "event_type": "deployment_rollback",
                            "message": "Production deployment failed, rolling back",
                            "level": "error"
                        }
                    }
                ]
            },
            {
                "name": "Code Review Required",
                "rule_type": RuleType.WORKFLOW.value,
                "description": "Require code review for non-admin commits",
                "conditions": [
                    {
                        "field": "user_role",
                        "operator": ConditionOperator.NOT_EQUALS.value,
                        "value": "admin"
                    },
                    {
                        "field": "branch_name",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "main"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.REQUIRE_APPROVAL.value,
                        "params": {
                            "approver_role": "admin",
                            "entity_type": "pull_request",
                            "entity_id": "{pr_id}"
                        }
                    },
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "slack",
                            "recipient": "#code-review",
                            "message": "Code review required for main branch commit"
                        }
                    }
                ]
            },
            {
                "name": "Security Scan on Deploy",
                "rule_type": RuleType.COMPLIANCE.value,
                "description": "Run security scans before production deployment",
                "conditions": [
                    {
                        "field": "deployment_environment",
                        "operator": ConditionOperator.EQUALS.value,
                        "value": "production"
                    },
                    {
                        "field": "security_scan_status",
                        "operator": ConditionOperator.NOT_EQUALS.value,
                        "value": "passed"
                    }
                ],
                "actions": [
                    {
                        "type": ActionType.TRIGGER_WORKFLOW.value,
                        "params": {
                            "workflow_name": "security_scan",
                            "workflow_params": {
                                "scan_type": "full",
                                "block_deploy": True
                            }
                        }
                    },
                    {
                        "type": ActionType.SEND_NOTIFICATION.value,
                        "params": {
                            "type": "slack",
                            "recipient": "#security",
                            "message": "Security scan required before production deploy"
                        }
                    }
                ]
            }
        ]
    
    def load_rules_from_file(self, file_path: str) -> bool:
        """Load rules from JSON file"""
        try:
            with open(file_path, 'r') as f:
                rules_data = json.load(f)
                for rule in rules_data:
                    self.add_rule(rule)
            return True
        except Exception as e:
            logger.error(f"Failed to load rules from file: {e}")
            return False
    
    def save_rules_to_file(self, file_path: str) -> bool:
        """Save current rules to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.rules, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save rules to file: {e}")
            return False

# Global rules engine instance
rules_engine = RulesEngine()

# Initialize with default rules
for rule in rules_engine.get_default_rules():
    rules_engine.add_rule(rule) 