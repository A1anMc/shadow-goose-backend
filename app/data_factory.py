"""
🎯 Shadow Goose Entertainment - Data Source Factory Pattern
Senior Data Engineer Implementation: Real vs Test Data Strategy
"""

import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from datetime import datetime

from .config import DataEnvironment, data_config, current_environment
from .grants import Grant, GrantApplication

logger = logging.getLogger(__name__)


class DataSource(ABC):
    """Abstract base class for data sources"""

    @abstractmethod
    async def get_grants(self) -> List[Grant]:
        """Get all grants"""
        pass

    @abstractmethod
    async def get_grant_by_id(self, grant_id: str) -> Optional[Grant]:
        """Get specific grant by ID"""
        pass

    @abstractmethod
    async def search_grants(self, **filters) -> List[Grant]:
        """Search grants with filters"""
        pass

    @abstractmethod
    async def get_applications(self) -> List[GrantApplication]:
        """Get all applications"""
        pass

    @abstractmethod
    async def get_application_by_id(self, application_id: str) -> Optional[GrantApplication]:
        """Get specific application by ID"""
        pass

    @abstractmethod
    async def create_application(self, application_data: Dict[str, Any]) -> GrantApplication:
        """Create new application"""
        pass

    @abstractmethod
    async def update_application(self, application_id: str, updates: Dict[str, Any]) -> bool:
        """Update application"""
        pass


class MockDataSource(DataSource):
    """Mock data source for development and testing"""

    def __init__(self):
        self.grants = self._load_mock_grants()
        self.applications = self._load_mock_applications()
        logger.info("Mock data source initialized")

    def _load_mock_grants(self) -> List[Grant]:
        """Load mock grants data"""
        from .grants import SAMPLE_GRANTS

        mock_grants = []
        for grant_data in SAMPLE_GRANTS:
            try:
                # Convert sample data to new Grant model format
                grant = Grant(
                    id=grant_data["id"],
                    title=grant_data["title"],
                    description=grant_data["description"],
                    amount=grant_data["amount"],
                    deadline=grant_data["deadline"],
                    category=grant_data["category"],
                    organisation=grant_data.get("source", "Unknown Organisation"),
                    eligibility_criteria=grant_data.get("eligibility", []),
                    required_documents=grant_data.get("requirements", []),
                    success_score=grant_data.get("success_score", 0.5)
                )
                mock_grants.append(grant)
            except Exception as e:
                logger.error(f"Error loading mock grant {grant_data.get('title', 'Unknown')}: {e}")

        return mock_grants

    def _load_mock_applications(self) -> List[GrantApplication]:
        """Load mock applications data"""
        mock_applications = []
        # Add sample applications if needed
        return mock_applications

    async def get_grants(self) -> List[Grant]:
        """Get all mock grants"""
        logger.info(f"Retrieved {len(self.grants)} mock grants")
        return self.grants

    async def get_grant_by_id(self, grant_id: str) -> Optional[Grant]:
        """Get specific mock grant by ID"""
        for grant in self.grants:
            if grant.id == grant_id:
                logger.info(f"Retrieved mock grant: {grant.title}")
                return grant
        logger.warning(f"Mock grant not found: {grant_id}")
        return None

    async def search_grants(self, **filters) -> List[Grant]:
        """Search mock grants with filters"""
        results = self.grants.copy()

        # Apply filters
        if filters.get("keywords"):
            keywords = filters["keywords"].lower()
            results = [
                g for g in results
                if keywords in g.title.lower() or keywords in g.description.lower()
            ]

        if filters.get("category"):
            results = [g for g in results if g.category == filters["category"]]

        if filters.get("min_amount"):
            results = [g for g in results if g.amount >= filters["min_amount"]]

        if filters.get("max_amount"):
            results = [g for g in results if g.amount <= filters["max_amount"]]

        logger.info(f"Mock grant search returned {len(results)} results")
        return results

    async def get_applications(self) -> List[GrantApplication]:
        """Get all mock applications"""
        return self.applications

    async def get_application_by_id(self, application_id: str) -> Optional[GrantApplication]:
        """Get specific mock application by ID"""
        for app in self.applications:
            if app.id == application_id:
                return app
        return None

    async def create_application(self, application_data: Dict[str, Any]) -> GrantApplication:
        """Create new mock application"""
        # Implementation for creating applications
        pass

    async def update_application(self, application_id: str, updates: Dict[str, Any]) -> bool:
        """Update mock application"""
        # Implementation for updating applications
        pass


class RealAPIDataSource(DataSource):
    """Real API data source for production"""

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.session = None
        logger.info(f"Real API data source initialized for {api_url}")

    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            import aiohttp
            self.session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self.session

    async def _make_api_call(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        """Make API call to external service"""
        session = await self._get_session()
        url = f"{self.api_url}/{endpoint}"
        
        try:
            if method == "GET":
                async with session.get(url) as response:
                    return await response.json()
            elif method == "POST":
                async with session.post(url, json=data) as response:
                    return await response.json()
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return {}

    async def get_grants(self) -> List[Grant]:
        """Get grants from real API"""
        logger.info(f"Retrieving grants from {self.api_url}")
        data = await self._make_api_call("grants")
        # Convert API response to Grant objects
        return []

    async def get_grant_by_id(self, grant_id: str) -> Optional[Grant]:
        """Get specific grant from real API"""
        logger.info(f"Retrieving grant {grant_id} from {self.api_url}")
        data = await self._make_api_call(f"grants/{grant_id}")
        # Convert API response to Grant object
        return None

    async def search_grants(self, **filters) -> List[Grant]:
        """Search grants in real API"""
        logger.info(f"Searching grants in {self.api_url}")
        # Build query parameters from filters
        return []

    async def get_applications(self) -> List[GrantApplication]:
        """Get applications from real API"""
        logger.info(f"Retrieving applications from {self.api_url}")
        data = await self._make_api_call("applications")
        # Convert API response to GrantApplication objects
        return []

    async def get_application_by_id(self, application_id: str) -> Optional[GrantApplication]:
        """Get specific application from real API"""
        logger.info(f"Retrieving application {application_id} from {self.api_url}")
        data = await self._make_api_call(f"applications/{application_id}")
        # Convert API response to GrantApplication object
        return None

    async def create_application(self, application_data: Dict[str, Any]) -> GrantApplication:
        """Create application in real API"""
        logger.info(f"Creating application in {self.api_url}")
        data = await self._make_api_call("applications", method="POST", data=application_data)
        # Convert API response to GrantApplication object
        return None

    async def update_application(self, application_id: str, updates: Dict[str, Any]) -> bool:
        """Update application in real API"""
        logger.info(f"Updating application {application_id} in {self.api_url}")
        data = await self._make_api_call(f"applications/{application_id}", method="POST", data=updates)
        return True


class DatabaseDataSource(DataSource):
    """Database data source (e.g., PostgreSQL)"""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        logger.info(f"Database data source initialized for {database_url}")

    async def _get_engine(self):
        """Get or create database engine"""
        if self.engine is None:
            from sqlalchemy.ext.asyncio import create_async_engine
            self.engine = create_async_engine(self.database_url)
        return self.engine

    async def get_grants(self) -> List[Grant]:
        """Get grants from database"""
        logger.info(f"Retrieving grants from database: {self.database_url}")
        engine = await self._get_engine()
        # Implement database query
        return []

    async def get_grant_by_id(self, grant_id: str) -> Optional[Grant]:
        """Get specific grant from database"""
        logger.info(f"Retrieving grant {grant_id} from database: {self.database_url}")
        engine = await self._get_engine()
        # Implement database query
        return None

    async def search_grants(self, **filters) -> List[Grant]:
        """Search grants in database"""
        logger.info(f"Searching grants in database: {self.database_url}")
        engine = await self._get_engine()
        # Implement database query with filters
        return []

    async def get_applications(self) -> List[GrantApplication]:
        """Get applications from database"""
        logger.info(f"Retrieving applications from database: {self.database_url}")
        engine = await self._get_engine()
        # Implement database query
        return []

    async def get_application_by_id(self, application_id: str) -> Optional[GrantApplication]:
        """Get specific application from database"""
        logger.info(f"Retrieving application {application_id} from database: {self.database_url}")
        engine = await self._get_engine()
        # Implement database query
        return None

    async def create_application(self, application_data: Dict[str, Any]) -> GrantApplication:
        """Create application in database"""
        logger.info(f"Creating application in database: {self.database_url}")
        engine = await self._get_engine()
        # Implement database insert
        return None

    async def update_application(self, application_id: str, updates: Dict[str, Any]) -> bool:
        """Update application in database"""
        logger.info(f"Updating application {application_id} in database: {self.database_url}")
        engine = await self._get_engine()
        # Implement database update
        return True


class DataSourceFactory:
    """Factory to create appropriate data sources based on environment"""

    @staticmethod
    def create_grant_source(environment: DataEnvironment = None) -> DataSource:
        """Create grant data source for environment"""
        if environment is None:
            environment = current_environment

        if environment == DataEnvironment.PRODUCTION:
            config = data_config.data_sources.get("grants", {})
            return RealAPIDataSource(
                config.get("url", ""), config.get("api_key", "")
            )
        elif environment == DataEnvironment.STAGING:
            config = data_config.data_sources.get("grants", {})
            return RealAPIDataSource(
                config.get("url", ""), config.get("api_key", "")
            )
        else:  # Development, Testing
            return MockDataSource()

    @staticmethod
    def create_application_source(environment: DataEnvironment = None) -> DataSource:
        """Create application data source for environment"""
        if environment is None:
            environment = current_environment

        if environment == DataEnvironment.PRODUCTION:
            config = data_config.data_sources.get("applications", {})
            return RealAPIDataSource(
                config.get("url", ""), config.get("api_key", "")
            )
        elif environment == DataEnvironment.STAGING:
            config = data_config.data_sources.get("applications", {})
            return RealAPIDataSource(
                config.get("url", ""), config.get("api_key", "")
            )
        else:  # Development, Testing
            return MockDataSource()

    @staticmethod
    def create_metrics_source(environment: DataEnvironment = None) -> DataSource:
        """Create metrics data source for environment"""
        if environment is None:
            environment = current_environment

        if environment == DataEnvironment.PRODUCTION:
            config = data_config.data_sources.get("metrics", {})
            return RealAPIDataSource(
                config.get("url", ""), config.get("api_key", "")
            )
        elif environment == DataEnvironment.STAGING:
            config = data_config.data_sources.get("metrics", {})
            return RealAPIDataSource(
                config.get("url", ""), config.get("api_key", "")
            )
        else:  # Development, Testing
            return MockDataSource()


# Global instances for easy access
grant_source = DataSourceFactory.create_grant_source()
application_source = DataSourceFactory.create_application_source()
metrics_source = DataSourceFactory.create_metrics_source()
