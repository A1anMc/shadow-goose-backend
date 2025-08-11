"""
🎯 Shadow Goose Entertainment - Data Environment Configuration System
Senior Data Engineer Implementation: Real vs Test Data Strategy
"""

import os
import logging
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


class DataEnvironment(str, Enum):
    """Data environment enumeration"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class DataSourceType(str, Enum):
    """Data source type enumeration"""

    MOCK = "mock"
    SAMPLE = "sample"
    REAL_API = "real_api"
    DATABASE = "database"
    EXTERNAL_SERVICE = "external_service"


@dataclass
class QualityThresholds:
    """Data quality thresholds by environment"""

    completeness: float
    accuracy: float
    consistency: float
    timeliness: float

    @classmethod
    def get_thresholds(cls, environment: DataEnvironment) -> "QualityThresholds":
        """Get quality thresholds for specific environment"""
        if environment == DataEnvironment.PRODUCTION:
            return cls(
                completeness=0.95, accuracy=0.90, consistency=0.85, timeliness=0.95
            )
        elif environment == DataEnvironment.STAGING:
            return cls(
                completeness=0.90, accuracy=0.85, consistency=0.80, timeliness=0.90
            )
        else:  # DEVELOPMENT, TESTING
            return cls(
                completeness=0.80, accuracy=0.75, consistency=0.70, timeliness=0.80
            )


@dataclass
class PerformanceThresholds:
    """Performance thresholds by environment"""

    api_response_time_ms: int
    data_processing_time_ms: int
    cache_ttl_seconds: int
    max_results_per_page: int

    @classmethod
    def get_thresholds(cls, environment: DataEnvironment) -> "PerformanceThresholds":
        """Get performance thresholds for specific environment"""
        if environment == DataEnvironment.PRODUCTION:
            return cls(
                api_response_time_ms=500,
                data_processing_time_ms=1000,
                cache_ttl_seconds=300,
                max_results_per_page=100,
            )
        else:  # All other environments
            return cls(
                api_response_time_ms=1000,
                data_processing_time_ms=2000,
                cache_ttl_seconds=60,
                max_results_per_page=50,
            )


class DataSourceConfig:
    """Data source configuration management"""

    def __init__(self, environment: str):
        self.environment = DataEnvironment(environment)
        self.use_real_data = self.environment == DataEnvironment.PRODUCTION
        self.data_sources = self._get_data_sources()
        self.quality_thresholds = QualityThresholds.get_thresholds(self.environment)
        self.performance_thresholds = PerformanceThresholds.get_thresholds(
            self.environment
        )

        logger.info(
            f"Data source configuration initialized for environment: {self.environment}"
        )
        logger.info(f"Using real data: {self.use_real_data}")

    def _get_data_sources(self) -> Dict[str, Dict[str, Any]]:
        """Map environment to appropriate data sources"""
        base_sources = {
            "grants": {
                "type": DataSourceType.SAMPLE,
                "path": "./sample_data/grants.json",
                "api_url": None,
                "cache_enabled": True,
                "validation_enabled": True,
            },
            "applications": {
                "type": DataSourceType.SAMPLE,
                "path": "./sample_data/applications.json",
                "api_url": None,
                "cache_enabled": True,
                "validation_enabled": True,
            },
            "users": {
                "type": DataSourceType.SAMPLE,
                "path": "./sample_data/users.json",
                "api_url": None,
                "cache_enabled": True,
                "validation_enabled": True,
            },
            "metrics": {
                "type": DataSourceType.SAMPLE,
                "path": "./sample_data/metrics.json",
                "api_url": None,
                "cache_enabled": True,
                "validation_enabled": True,
            },
        }

        if self.environment == DataEnvironment.PRODUCTION:
            # Production: Real APIs, databases, external services
            return {
                "grants": {
                    "type": DataSourceType.REAL_API,
                    "api_url": os.getenv("GRANTS_API_URL"),
                    "api_key": os.getenv("GRANTS_API_KEY"),
                    "rate_limit": 100,
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "fallback_enabled": True,
                },
                "applications": {
                    "type": DataSourceType.DATABASE,
                    "database_url": os.getenv("DATABASE_URL"),
                    "table_name": "grant_applications",
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "backup_enabled": True,
                },
                "users": {
                    "type": DataSourceType.DATABASE,
                    "database_url": os.getenv("DATABASE_URL"),
                    "table_name": "users",
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "encryption_enabled": True,
                },
                "metrics": {
                    "type": DataSourceType.EXTERNAL_SERVICE,
                    "service_url": os.getenv("METRICS_SERVICE_URL"),
                    "api_key": os.getenv("METRICS_API_KEY"),
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "monitoring_enabled": True,
                },
            }
        elif self.environment == DataEnvironment.STAGING:
            # Staging: Mix of real and sample data for testing
            return {
                "grants": {
                    "type": DataSourceType.REAL_API,
                    "api_url": os.getenv("STAGING_GRANTS_API_URL"),
                    "api_key": os.getenv("STAGING_GRANTS_API_KEY"),
                    "rate_limit": 50,
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "fallback_enabled": True,
                },
                "applications": {
                    "type": DataSourceType.DATABASE,
                    "database_url": os.getenv("STAGING_DATABASE_URL"),
                    "table_name": "grant_applications",
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "backup_enabled": False,
                },
                "users": {
                    "type": DataSourceType.DATABASE,
                    "database_url": os.getenv("STAGING_DATABASE_URL"),
                    "table_name": "users",
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "encryption_enabled": False,
                },
                "metrics": {
                    "type": DataSourceType.SAMPLE,
                    "path": "./sample_data/metrics.json",
                    "cache_enabled": True,
                    "validation_enabled": True,
                    "monitoring_enabled": False,
                },
            }
        else:
            # Development/Testing: Sample data, mocks, test databases
            return base_sources

    def get_source_config(self, source_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for specific data source"""
        return self.data_sources.get(source_name)

    def is_real_data_source(self, source_name: str) -> bool:
        """Check if data source uses real data"""
        source_config = self.get_source_config(source_name)
        if not source_config:
            return False

        return source_config.get("type") in [
            DataSourceType.REAL_API,
            DataSourceType.DATABASE,
            DataSourceType.EXTERNAL_SERVICE,
        ]

    def get_cache_config(self, source_name: str) -> Dict[str, Any]:
        """Get cache configuration for data source"""
        source_config = self.get_source_config(source_name)
        if not source_config:
            return {"enabled": False}

        return {
            "enabled": source_config.get("cache_enabled", False),
            "ttl_seconds": self.performance_thresholds.cache_ttl_seconds,
            "max_size": 1000,
        }

    def get_validation_config(self, source_name: str) -> Dict[str, Any]:
        """Get validation configuration for data source"""
        source_config = self.get_source_config(source_name)
        if not source_config:
            return {"enabled": False}

        return {
            "enabled": source_config.get("validation_enabled", False),
            "thresholds": {
                "completeness": self.quality_thresholds.completeness,
                "accuracy": self.quality_thresholds.accuracy,
                "consistency": self.quality_thresholds.consistency,
                "timeliness": self.quality_thresholds.timeliness,
            },
        }


class EnvironmentManager:
    """Environment detection and management"""

    @staticmethod
    def detect_environment() -> DataEnvironment:
        """Detect current environment from environment variables"""
        env_var = os.getenv("DATA_ENVIRONMENT", "development")

        try:
            return DataEnvironment(env_var.lower())
        except ValueError:
            logger.warning(
                f"Invalid environment '{env_var}', defaulting to development"
            )
            return DataEnvironment.DEVELOPMENT

    @staticmethod
    def is_production() -> bool:
        """Check if current environment is production"""
        return EnvironmentManager.detect_environment() == DataEnvironment.PRODUCTION

    @staticmethod
    def is_staging() -> bool:
        """Check if current environment is staging"""
        return EnvironmentManager.detect_environment() == DataEnvironment.STAGING

    @staticmethod
    def is_development() -> bool:
        """Check if current environment is development"""
        return EnvironmentManager.detect_environment() == DataEnvironment.DEVELOPMENT

    @staticmethod
    def is_testing() -> bool:
        """Check if current environment is testing"""
        return EnvironmentManager.detect_environment() == DataEnvironment.TESTING

    @staticmethod
    def get_environment_info() -> Dict[str, Any]:
        """Get comprehensive environment information"""
        env = EnvironmentManager.detect_environment()

        return {
            "environment": env.value,
            "is_production": env == DataEnvironment.PRODUCTION,
            "is_staging": env == DataEnvironment.STAGING,
            "is_development": env == DataEnvironment.DEVELOPMENT,
            "is_testing": env == DataEnvironment.TESTING,
            "use_real_data": env == DataEnvironment.PRODUCTION,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
        }


# Global configuration instance
current_environment = EnvironmentManager.detect_environment()
data_config = DataSourceConfig(current_environment.value)

# Export configuration for use throughout the application
__all__ = [
    "DataEnvironment",
    "DataSourceType",
    "QualityThresholds",
    "PerformanceThresholds",
    "DataSourceConfig",
    "EnvironmentManager",
    "current_environment",
    "data_config",
]
