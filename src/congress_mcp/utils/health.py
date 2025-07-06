"""
Health check utilities for Congress API Explorer.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from .logging import logger
from .config import settings


class HealthStatus(Enum):
    """Health status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Individual health check result."""
    
    name: str
    status: HealthStatus
    message: str = ""
    response_time_ms: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemHealth:
    """Overall system health status."""
    
    status: HealthStatus
    checks: List[HealthCheck] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "uptime_seconds": self.uptime_seconds,
            "checks": [
                {
                    "name": check.name,
                    "status": check.status.value,
                    "message": check.message,
                    "response_time_ms": check.response_time_ms,
                    "timestamp": check.timestamp.isoformat(),
                    "metadata": check.metadata
                }
                for check in self.checks
            ]
        }


class HealthChecker:
    """
    System health checker for Congress API Explorer.
    """
    
    def __init__(self):
        self.settings = settings
        self.start_time = time.time()
        self._cached_health: Optional[SystemHealth] = None
        self._cache_expiry: Optional[datetime] = None
        self._cache_duration = timedelta(seconds=30)  # Cache for 30 seconds
    
    async def check_health(self, force_refresh: bool = False) -> SystemHealth:
        """
        Perform comprehensive health check.
        
        Args:
            force_refresh: Force refresh of cached health status
            
        Returns:
            SystemHealth object with overall status and individual checks
        """
        # Return cached result if available and not expired
        if not force_refresh and self._cached_health and self._cache_expiry:
            if datetime.now() < self._cache_expiry:
                return self._cached_health
        
        logger.info("Performing health check...")
        
        checks = []
        
        # Check 1: Basic system health
        checks.append(await self._check_system_health())
        
        # Check 2: Configuration health
        checks.append(await self._check_configuration_health())
        
        # Check 3: API connectivity
        checks.append(await self._check_api_connectivity())
        
        # Check 4: Rate limiting status
        checks.append(await self._check_rate_limiting())
        
        # Check 5: Cache health
        checks.append(await self._check_cache_health())
        
        # Determine overall status
        overall_status = self._determine_overall_status(checks)
        
        # Calculate uptime
        uptime = time.time() - self.start_time
        
        # Create health object
        health = SystemHealth(
            status=overall_status,
            checks=checks,
            uptime_seconds=uptime
        )
        
        # Cache the result
        self._cached_health = health
        self._cache_expiry = datetime.now() + self._cache_duration
        
        logger.info(f"Health check completed. Overall status: {overall_status.value}")
        return health
    
    async def _check_system_health(self) -> HealthCheck:
        """Check basic system health."""
        try:
            start_time = time.time()
            
            # Basic system checks
            import psutil
            
            # Check memory usage
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            response_time = (time.time() - start_time) * 1000
            
            if memory.percent > 90:
                return HealthCheck(
                    name="system",
                    status=HealthStatus.UNHEALTHY,
                    message=f"High memory usage: {memory.percent:.1f}%",
                    response_time_ms=response_time,
                    metadata={
                        "memory_percent": memory.percent,
                        "cpu_percent": cpu_percent
                    }
                )
            elif memory.percent > 70:
                return HealthCheck(
                    name="system",
                    status=HealthStatus.DEGRADED,
                    message=f"Moderate memory usage: {memory.percent:.1f}%",
                    response_time_ms=response_time,
                    metadata={
                        "memory_percent": memory.percent,
                        "cpu_percent": cpu_percent
                    }
                )
            else:
                return HealthCheck(
                    name="system",
                    status=HealthStatus.HEALTHY,
                    message=f"System healthy - Memory: {memory.percent:.1f}%, CPU: {cpu_percent:.1f}%",
                    response_time_ms=response_time,
                    metadata={
                        "memory_percent": memory.percent,
                        "cpu_percent": cpu_percent
                    }
                )
                
        except Exception as e:
            return HealthCheck(
                name="system",
                status=HealthStatus.UNKNOWN,
                message=f"Unable to check system health: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _check_configuration_health(self) -> HealthCheck:
        """Check configuration health."""
        try:
            start_time = time.time()
            
            # Check required configuration
            issues = []
            
            if not self.settings.congress_api_key:
                issues.append("Congress API key not configured")
            
            if not self.settings.congress_api_base_url:
                issues.append("Congress API base URL not configured")
            
            response_time = (time.time() - start_time) * 1000
            
            if issues:
                return HealthCheck(
                    name="configuration",
                    status=HealthStatus.UNHEALTHY,
                    message=f"Configuration issues: {', '.join(issues)}",
                    response_time_ms=response_time,
                    metadata={"issues": issues}
                )
            else:
                return HealthCheck(
                    name="configuration",
                    status=HealthStatus.HEALTHY,
                    message="Configuration valid",
                    response_time_ms=response_time
                )
                
        except Exception as e:
            return HealthCheck(
                name="configuration",
                status=HealthStatus.UNKNOWN,
                message=f"Unable to check configuration: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _check_api_connectivity(self) -> HealthCheck:
        """Check Congress API connectivity."""
        try:
            start_time = time.time()
            
            # Import here to avoid circular imports
            from ..api import CongressAPIClient
            
            # Create temporary client
            client = CongressAPIClient()
            
            try:
                # Test basic API connectivity
                current_congress = await client.get_current_congress()
                
                response_time = (time.time() - start_time) * 1000
                
                if response_time > 5000:  # 5 seconds
                    status = HealthStatus.DEGRADED
                    message = f"API responsive but slow ({response_time:.0f}ms)"
                else:
                    status = HealthStatus.HEALTHY
                    message = f"API connectivity healthy ({response_time:.0f}ms)"
                
                return HealthCheck(
                    name="api_connectivity",
                    status=status,
                    message=message,
                    response_time_ms=response_time,
                    metadata={"current_congress": current_congress}
                )
                
            finally:
                await client.close()
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                name="api_connectivity",
                status=HealthStatus.UNHEALTHY,
                message=f"API connectivity failed: {str(e)}",
                response_time_ms=response_time,
                metadata={"error": str(e)}
            )
    
    async def _check_rate_limiting(self) -> HealthCheck:
        """Check rate limiting status."""
        try:
            start_time = time.time()
            
            # Import here to avoid circular imports
            from ..api import rate_limiter
            
            status_info = rate_limiter.get_rate_limit_status()
            
            response_time = (time.time() - start_time) * 1000
            
            # Check if we're close to rate limits
            warnings = []
            for window, info in status_info.items():
                usage_percent = (info['used'] / info['limit']) * 100
                if usage_percent > 90:
                    warnings.append(f"{window} window at {usage_percent:.1f}%")
                elif usage_percent > 70:
                    warnings.append(f"{window} window at {usage_percent:.1f}%")
            
            if warnings:
                if any("90" in w for w in warnings):
                    status = HealthStatus.UNHEALTHY
                    message = f"Rate limit critical: {', '.join(warnings)}"
                else:
                    status = HealthStatus.DEGRADED
                    message = f"Rate limit warning: {', '.join(warnings)}"
            else:
                status = HealthStatus.HEALTHY
                message = "Rate limiting healthy"
            
            return HealthCheck(
                name="rate_limiting",
                status=status,
                message=message,
                response_time_ms=response_time,
                metadata=status_info
            )
            
        except Exception as e:
            return HealthCheck(
                name="rate_limiting",
                status=HealthStatus.UNKNOWN,
                message=f"Unable to check rate limiting: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _check_cache_health(self) -> HealthCheck:
        """Check cache health."""
        try:
            start_time = time.time()
            
            # Import here to avoid circular imports
            from ..utils.cache import cache_manager
            
            # Test cache operations
            test_key = "health_check_test"
            test_value = {"timestamp": datetime.now().isoformat()}
            
            # Test set
            await cache_manager.set(test_key, test_value, ttl=60)
            
            # Test get
            cached_value = await cache_manager.get(test_key)
            
            # Test delete
            await cache_manager.delete(test_key)
            
            response_time = (time.time() - start_time) * 1000
            
            if cached_value is None:
                return HealthCheck(
                    name="cache",
                    status=HealthStatus.DEGRADED,
                    message="Cache not retaining values",
                    response_time_ms=response_time
                )
            
            return HealthCheck(
                name="cache",
                status=HealthStatus.HEALTHY,
                message="Cache operations healthy",
                response_time_ms=response_time,
                metadata={"cache_type": cache_manager.cache_type}
            )
            
        except Exception as e:
            return HealthCheck(
                name="cache",
                status=HealthStatus.UNHEALTHY,
                message=f"Cache operations failed: {str(e)}",
                metadata={"error": str(e)}
            )
    
    def _determine_overall_status(self, checks: List[HealthCheck]) -> HealthStatus:
        """Determine overall system health status from individual checks."""
        if not checks:
            return HealthStatus.UNKNOWN
        
        # Count status occurrences
        status_counts = {}
        for check in checks:
            status_counts[check.status] = status_counts.get(check.status, 0) + 1
        
        # Determine overall status
        if status_counts.get(HealthStatus.UNHEALTHY, 0) > 0:
            return HealthStatus.UNHEALTHY
        elif status_counts.get(HealthStatus.DEGRADED, 0) > 0:
            return HealthStatus.DEGRADED
        elif status_counts.get(HealthStatus.UNKNOWN, 0) > 0:
            return HealthStatus.UNKNOWN
        else:
            return HealthStatus.HEALTHY
    
    def get_uptime(self) -> float:
        """Get system uptime in seconds."""
        return time.time() - self.start_time
    
    def get_uptime_formatted(self) -> str:
        """Get formatted uptime string."""
        uptime = self.get_uptime()
        
        days = int(uptime // (24 * 3600))
        hours = int((uptime % (24 * 3600)) // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"


# Global health checker instance
health_checker = HealthChecker()