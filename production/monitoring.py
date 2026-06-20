import time
import psutil
import platform
from datetime import datetime
import threading


class HealthMonitor:
    """
    Production Monitoring System for AI Backend (MYTHOS V4)
    """

    def __init__(self, service_name: str = "MYTHOS_V4"):
        self.service_name = service_name
        self.start_time = time.time()
        self.lock = threading.Lock()

    # ==================================
    # SYSTEM HEALTH
    # ==================================
    def system_health(self):
        with self.lock:
            return {
                "service": self.service_name,
                "status": self._get_status(),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "uptime_seconds": self._uptime(),

                "system": {
                    "os": platform.system(),
                    "cpu_usage": psutil.cpu_percent(interval=0.5),
                    "memory_usage": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage('/').percent
                }
            }

    # ==================================
    # SERVICE HEALTH CHECK
    # ==================================
    def service_health(self, services: dict):
        """
        services = {
            "ai": ai_router.health_check(),
            "db": postgres_health(),
            "billing": stripe_health()
        }
        """

        results = {}

        for name, service in services.items():

            try:
                status = "unknown"

                if isinstance(service, dict):
                    status = service.get("status", "unknown")

                elif isinstance(service, bool):
                    status = "healthy" if service else "unhealthy"

                elif isinstance(service, str):
                    status = service

                results[name] = {
                    "status": status,
                    "checked": True,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

            except Exception as e:
                results[name] = {
                    "status": "error",
                    "checked": False,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

        return results

    # ==================================
    # FULL HEALTH REPORT
    # ==================================
    def full_report(self, services: dict):

        services_health = self.service_health(services)

        overall_status = self._calculate_overall_status(services_health)

        return {
            "system": self.system_health(),
            "services": services_health,
            "overall_status": overall_status,
            "recommendation": self._get_recommendation(overall_status),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    # ==================================
    # SIMPLE PING CHECK
    # ==================================
    def ping(self):
        return {
            "pong": True,
            "service": self.service_name,
            "time": datetime.utcnow().isoformat() + "Z"
        }

    # ==================================
    # INTERNAL HELPERS
    # ==================================
    def _uptime(self):
        return int(time.time() - self.start_time)

    def _get_status(self):
        cpu = psutil.cpu_percent(interval=0.3)
        memory = psutil.virtual_memory().percent

        if cpu > 90 or memory > 90:
            return "critical"
        elif cpu > 75 or memory > 75:
            return "degraded"
        return "healthy"

    def _calculate_overall_status(self, services: dict):
        if not services:
            return "unknown"

        statuses = [s.get("status", "unknown") for s in services.values()]

        if "error" in statuses:
            return "critical"
        if "unhealthy" in statuses:
            return "degraded"

        return "healthy"

    def _get_recommendation(self, status: str):
        if status == "healthy":
            return "All systems operational"
        elif status == "degraded":
            return "Monitor system load and services"
        elif status == "critical":
            return "Immediate attention required"
        else:
            return "Status unknown"
