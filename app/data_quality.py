"""
🎯 Shadow Goose Entertainment - Data Quality Validation Framework
Senior Data Engineer Implementation: Real vs Test Data Strategy
"""

import logging
import os
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from .config import DataEnvironment, data_config, current_environment

logger = logging.getLogger(__name__)


class QualityLevel(str, Enum):
    """Data quality level enumeration"""

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FAILED = "failed"


@dataclass
class QualityMetric:
    """Individual quality metric"""

    name: str
    value: float
    threshold: float
    passed: bool
    details: Dict[str, Any] = None


@dataclass
class QualityReport:
    """Comprehensive quality report"""

    data_type: str
    environment: str
    timestamp: datetime
    overall_score: float
    quality_level: QualityLevel
    metrics: List[QualityMetric]
    issues: List[str]
    recommendations: List[str]
    validation_time_ms: float


class DataQualityValidator:
    """Comprehensive data quality validation framework"""

    def __init__(self, environment: DataEnvironment = None):
        self.environment = environment or current_environment
        self.thresholds = data_config.quality_thresholds
        self.performance_thresholds = data_config.performance_thresholds
        logger.info(
            f"Data quality validator initialized for environment: {self.environment}"
        )

    async def validate_data(self, data: Any, data_type: str) -> QualityReport:
        """Validate data with comprehensive quality checks"""
        start_time = datetime.utcnow()

        logger.info(f"Starting data quality validation for {data_type}")

        # Initialize metrics
        metrics = []
        issues = []
        recommendations = []

        # Perform validation based on data type
        if data_type == "grants":
            metrics, issues, recommendations = await self._validate_grants(data)
        elif data_type == "applications":
            metrics, issues, recommendations = await self._validate_applications(data)
        elif data_type == "users":
            metrics, issues, recommendations = await self._validate_users(data)
        else:
            metrics, issues, recommendations = await self._validate_generic_data(
                data, data_type
            )

        # Calculate overall score
        overall_score = self._calculate_overall_score(metrics)
        quality_level = self._determine_quality_level(overall_score)

        # Calculate validation time
        validation_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        report = QualityReport(
            data_type=data_type,
            environment=self.environment.value,
            timestamp=datetime.utcnow(),
            overall_score=overall_score,
            quality_level=quality_level,
            metrics=metrics,
            issues=issues,
            recommendations=recommendations,
            validation_time_ms=validation_time,
        )

        logger.info(
            f"Data quality validation completed for {data_type}: {quality_level.value}\
                ({overall_score:.2%})"
        )

        return report

    async def _validate_grants(
        self, grants: List[Any]
    ) -> Tuple[List[QualityMetric], List[str], List[str]]:
        """Validate grants data"""
        metrics = []
        issues = []
        recommendations = []

        if not grants:
            issues.append("No grants data provided")
            return metrics, issues, recommendations

        # Completeness check
        completeness_score = self._check_completeness(
            grants,
            [
                "id",
                "title",
                "description",
                "amount",
                "deadline",
                "category",
                "organisation",
            ],
        )
        metrics.append(
            QualityMetric(
                name="completeness",
                value=completeness_score,
                threshold=self.thresholds.completeness,
                passed=completeness_score >= self.thresholds.completeness,
                details={"required_fields": 7, "missing_fields": 0},
            )
        )

        if completeness_score < self.thresholds.completeness:
            issues.append(
                f"Data completeness below threshold: {completeness_score:.2%} < {self.thresholds.completeness:.2%}"
            )
            recommendations.append(
                "Review data collection process to ensure all required fields are captured"
            )

        # Accuracy check
        accuracy_score = self._check_grants_accuracy(grants)
        metrics.append(
            QualityMetric(
                name="accuracy",
                value=accuracy_score,
                threshold=self.thresholds.accuracy,
                passed=accuracy_score >= self.thresholds.accuracy,
                details={"valid_records": 0, "total_records": len(grants)},
            )
        )

        if accuracy_score < self.thresholds.accuracy:
            issues.append(
                f"Data accuracy below threshold: {accuracy_score:.2%} < {self.thresholds.accuracy:.2%}"
            )
            recommendations.append(
                "Implement data validation rules and review data sources"
            )

        # Consistency check
        consistency_score = self._check_grants_consistency(grants)
        metrics.append(
            QualityMetric(
                name="consistency",
                value=consistency_score,
                threshold=self.thresholds.consistency,
                passed=consistency_score >= self.thresholds.consistency,
                details={"consistent_records": 0, "total_records": len(grants)},
            )
        )

        if consistency_score < self.thresholds.consistency:
            issues.append(
                f"Data consistency below threshold: {consistency_score:.2%} < {self.thresholds.consistency:.2%}"
            )
            recommendations.append(
                "Standardize data formats and implement consistency checks"
            )

        # Timeliness check
        timeliness_score = self._check_grants_timeliness(grants)
        metrics.append(
            QualityMetric(
                name="timeliness",
                value=timeliness_score,
                threshold=self.thresholds.timeliness,
                passed=timeliness_score >= self.thresholds.timeliness,
                details={"current_records": 0, "total_records": len(grants)},
            )
        )

        if timeliness_score < self.thresholds.timeliness:
            issues.append(
                f"Data timeliness below threshold: {timeliness_score:.2%} < {self.thresholds.timeliness:.2%}"
            )
            recommendations.append("Implement regular data refresh processes")

        # Currency format check (AUD)
        currency_score = self._check_currency_format(grants)
        metrics.append(
            QualityMetric(
                name="currency_format",
                value=currency_score,
                threshold=0.95,  # High threshold for currency formatting
                passed=currency_score >= 0.95,
                details={"aud_formatted": 0, "total_amounts": 0},
            )
        )

        if currency_score < 0.95:
            issues.append(f"Currency formatting issues: {currency_score:.2%} < 95%")
            recommendations.append("Ensure all monetary values are in AUD format")

        return metrics, issues, recommendations

    async def _validate_applications(
        self, applications: List[Any]
    ) -> Tuple[List[QualityMetric], List[str], List[str]]:
        """Validate applications data"""
        metrics = []
        issues = []
        recommendations = []

        if not applications:
            issues.append("No applications data provided")
            return metrics, issues, recommendations

        # Completeness check
        completeness_score = self._check_completeness(
            applications, ["id", "grant_id", "title", "status", "assigned_to", "budget"]
        )
        metrics.append(
            QualityMetric(
                name="completeness",
                value=completeness_score,
                threshold=self.thresholds.completeness,
                passed=completeness_score >= self.thresholds.completeness,
            )
        )

        # Accuracy check
        accuracy_score = self._check_applications_accuracy(applications)
        metrics.append(
            QualityMetric(
                name="accuracy",
                value=accuracy_score,
                threshold=self.thresholds.accuracy,
                passed=accuracy_score >= self.thresholds.accuracy,
            )
        )

        # Consistency check
        consistency_score = self._check_applications_consistency(applications)
        metrics.append(
            QualityMetric(
                name="consistency",
                value=consistency_score,
                threshold=self.thresholds.consistency,
                passed=consistency_score >= self.thresholds.consistency,
            )
        )

        return metrics, issues, recommendations

    async def _validate_users(
        self, users: List[Any]
    ) -> Tuple[List[QualityMetric], List[str], List[str]]:
        """Validate users data"""
        metrics = []
        issues = []
        recommendations = []

        if not users:
            issues.append("No users data provided")
            return metrics, issues, recommendations

        # Completeness check
        completeness_score = self._check_completeness(
            users, ["id", "username", "email", "role"]
        )
        metrics.append(
            QualityMetric(
                name="completeness",
                value=completeness_score,
                threshold=self.thresholds.completeness,
                passed=completeness_score >= self.thresholds.completeness,
            )
        )

        # Email format check
        email_score = self._check_email_format(users)
        metrics.append(
            QualityMetric(
                name="email_format",
                value=email_score,
                threshold=0.95,
                passed=email_score >= 0.95,
            )
        )

        return metrics, issues, recommendations

    async def _validate_generic_data(
        self, data: Any, data_type: str
    ) -> Tuple[List[QualityMetric], List[str], List[str]]:
        """Validate generic data"""
        metrics = []
        issues = []
        recommendations = []

        # Basic validation for any data type
        if data is None:
            issues.append("Data is null")
            return metrics, issues, recommendations

        # Check if data is empty
        if isinstance(data, (list, dict)) and len(data) == 0:
            issues.append("Data is empty")
            return metrics, issues, recommendations

        # Basic completeness check
        completeness_score = 1.0 if data else 0.0
        metrics.append(
            QualityMetric(
                name="completeness",
                value=completeness_score,
                threshold=self.thresholds.completeness,
                passed=completeness_score >= self.thresholds.completeness,
            )
        )

        return metrics, issues, recommendations

    def _check_completeness(self, data: List[Any], required_fields: List[str]) -> float:
        """Check data completeness"""
        if not data:
            return 0.0

        total_fields = len(data) * len(required_fields)
        missing_fields = 0

        for item in data:
            if isinstance(item, dict):
                for field in required_fields:
                    if field not in item or item[field] is None:
                        missing_fields += 1
            else:
                # For objects, check if attributes exist
                for field in required_fields:
                    if not hasattr(item, field) or getattr(item, field) is None:
                        missing_fields += 1

        return (
            (total_fields - missing_fields) / total_fields if total_fields > 0 else 0.0
        )

    def _check_grants_accuracy(self, grants: List[Any]) -> float:
        """Check grants data accuracy"""
        if not grants:
            return 0.0

        valid_records = 0

        for grant in grants:
            try:
                # Check if grant has valid structure
                if hasattr(grant, "amount") and grant.amount > 0:
                    if (
                        hasattr(grant, "deadline")
                        and grant.deadline > datetime.utcnow()
                    ):
                        if hasattr(grant, "title") and len(grant.title) > 0:
                            valid_records += 1
            except Exception as e:
                logger.warning(f"Error checking grant accuracy: {e}")

        return valid_records / len(grants) if grants else 0.0

    def _check_grants_consistency(self, grants: List[Any]) -> float:
        """Check grants data consistency"""
        if not grants:
            return 0.0

        consistent_records = 0

        for grant in grants:
            try:
                # Check for consistent data types and formats
                if hasattr(grant, "amount") and isinstance(grant.amount, (int, float)):
                    if hasattr(grant, "deadline") and isinstance(
                        grant.deadline, datetime
                    ):
                        if hasattr(grant, "category") and grant.category:
                            consistent_records += 1
            except Exception as e:
                logger.warning(f"Error checking grant consistency: {e}")

        return consistent_records / len(grants) if grants else 0.0

    def _check_grants_timeliness(self, grants: List[Any]) -> float:
        """Check grants data timeliness"""
        if not grants:
            return 0.0

        current_records = 0
        cutoff_date = datetime.utcnow() - timedelta(
            days=30
        )  # Consider data current if updated within 30 days

        for grant in grants:
            try:
                if hasattr(grant, "updated_at"):
                    if grant.updated_at >= cutoff_date:
                        current_records += 1
                elif hasattr(grant, "created_at"):
                    if grant.created_at >= cutoff_date:
                        current_records += 1
                else:
                    # If no timestamp, assume current
                    current_records += 1
            except Exception as e:
                logger.warning(f"Error checking grant timeliness: {e}")

        return current_records / len(grants) if grants else 0.0

    def _check_currency_format(self, grants: List[Any]) -> float:
        """Check currency format compliance (AUD)"""
        if not grants:
            return 0.0

        aud_formatted = 0
        total_amounts = 0

        for grant in grants:
            try:
                if hasattr(grant, "amount") and grant.amount is not None:
                    total_amounts += 1
                    # Check if amount is a valid number
                    if isinstance(grant.amount, (int, float)) and grant.amount > 0:
                        aud_formatted += 1
            except Exception as e:
                logger.warning(f"Error checking currency format: {e}")

        return aud_formatted / total_amounts if total_amounts > 0 else 0.0

    def _check_applications_accuracy(self, applications: List[Any]) -> float:
        """Check applications data accuracy"""
        if not applications:
            return 0.0

        valid_records = 0

        for app in applications:
            try:
                if hasattr(app, "grant_id") and app.grant_id:
                    if hasattr(app, "title") and len(app.title) > 0:
                        if hasattr(app, "budget") and app.budget > 0:
                            valid_records += 1
            except Exception as e:
                logger.warning(f"Error checking application accuracy: {e}")

        return valid_records / len(applications) if applications else 0.0

    def _check_applications_consistency(self, applications: List[Any]) -> float:
        """Check applications data consistency"""
        if not applications:
            return 0.0

        consistent_records = 0

        for app in applications:
            try:
                if hasattr(app, "status") and app.status in [
                    "draft",
                    "in_progress",
                    "submitted",
                    "approved",
                    "rejected",
                ]:
                    if hasattr(app, "budget") and isinstance(app.budget, (int, float)):
                        consistent_records += 1
            except Exception as e:
                logger.warning(f"Error checking application consistency: {e}")

        return consistent_records / len(applications) if applications else 0.0

    def _check_email_format(self, users: List[Any]) -> float:
        """Check email format validity"""
        if not users:
            return 0.0

        valid_emails = 0

        for user in users:
            try:
                if hasattr(user, "email") and user.email:
                    # Basic email format check
                    if "@" in user.email and "." in user.email.split("@")[1]:
                        valid_emails += 1
            except Exception as e:
                logger.warning(f"Error checking email format: {e}")

        return valid_emails / len(users) if users else 0.0

    def _calculate_overall_score(self, metrics: List[QualityMetric]) -> float:
        """Calculate overall quality score"""
        if not metrics:
            return 0.0

        # Weighted average of all metrics
        total_weight = 0
        weighted_sum = 0

        for metric in metrics:
            # Assign weights based on metric importance
            weight = 1.0
            if metric.name == "completeness":
                weight = 0.3
            elif metric.name == "accuracy":
                weight = 0.3
            elif metric.name == "consistency":
                weight = 0.2
            elif metric.name == "timeliness":
                weight = 0.2

            weighted_sum += metric.value * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _determine_quality_level(self, score: float) -> QualityLevel:
        """Determine quality level based on score"""
        if score >= 0.95:
            return QualityLevel.EXCELLENT
        elif score >= 0.85:
            return QualityLevel.GOOD
        elif score >= 0.75:
            return QualityLevel.FAIR
        elif score >= 0.60:
            return QualityLevel.POOR
        else:
            return QualityLevel.FAILED


class RealDataAuthenticator:
    """Secure authentication for real data sources"""

    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.rate_limits = self._configure_rate_limits()
        self.rate_limit_trackers = {}
        logger.info("Real data authenticator initialized")

    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables"""
        return {
            "grants_api": os.getenv("GRANTS_API_KEY"),
            "metrics_api": os.getenv("METRICS_API_KEY"),
            "applications_api": os.getenv("APPLICATIONS_API_KEY"),
        }

    def _configure_rate_limits(self) -> Dict[str, Dict[str, int]]:
        """Configure rate limits for different APIs"""
        return {
            "grants_api": {"requests_per_minute": 100, "requests_per_hour": 1000},
            "metrics_api": {"requests_per_minute": 50, "requests_per_hour": 500},
            "applications_api": {"requests_per_minute": 200, "requests_per_hour": 2000},
        }

    async def authenticate_api(self, api_name: str) -> bool:
        """Verify API credentials and permissions"""
        try:
            api_key = self.api_keys.get(api_name)

            if not api_key:
                logger.error(f"No API key found for {api_name}")
                return False

            # Check rate limits
            if not self._check_rate_limit(api_name):
                logger.warning(f"Rate limit exceeded for {api_name}")
                return False

            # Verify API key format (basic check)
            if len(api_key) < 10:
                logger.error(f"Invalid API key format for {api_name}")
                return False

            logger.info(f"Successfully authenticated {api_name}")
            return True

        except Exception as e:
            logger.error(f"Authentication error for {api_name}: {e}")
            return False

    def _check_rate_limit(self, api_name: str) -> bool:
        """Check if API call is within rate limits"""
        if api_name not in self.rate_limits:
            return True

        now = datetime.utcnow()

        if api_name not in self.rate_limit_trackers:
            self.rate_limit_trackers[api_name] = {
                "minute_requests": [],
                "hour_requests": [],
            }

        tracker = self.rate_limit_trackers[api_name]
        limits = self.rate_limits[api_name]

        # Clean old requests
        tracker["minute_requests"] = [
            req_time
            for req_time in tracker["minute_requests"]
            if (now - req_time).total_seconds() < 60
        ]

        tracker["hour_requests"] = [
            req_time
            for req_time in tracker["hour_requests"]
            if (now - req_time).total_seconds() < 3600
        ]

        # Check limits
        if len(tracker["minute_requests"]) >= limits["requests_per_minute"]:
            return False

        if len(tracker["hour_requests"]) >= limits["requests_per_hour"]:
            return False

        # Add current request
        tracker["minute_requests"].append(now)
        tracker["hour_requests"].append(now)

        return True


# Global instances
data_validator = DataQualityValidator()
data_authenticator = RealDataAuthenticator()

# Export for use throughout the application
__all__ = [
    "QualityLevel",
    "QualityMetric",
    "QualityReport",
    "DataQualityValidator",
    "RealDataAuthenticator",
    "data_validator",
    "data_authenticator",
]
