# production/health.py

import os
import platform
from datetime import datetime


class HealthChecker:

    def __init__(self):

        self.services = {}

    def register_service(
        self,
        name,
        service
    ):

        self.services[name] = service

    def check_environment(self):

        return {

            "python_version":
                platform.python_version(),

            "platform":
                platform.platform(),

            "timestamp":
                datetime.now()
                .isoformat()
        }

    def check_api_keys(self):

        return {

            "openai":
                bool(
                    os.getenv(
                        "OPENAI_API_KEY"
                    )
                ),

            "gemini":
                bool(
                    os.getenv(
                        "GEMINI_API_KEY"
                    )
                ),

            "claude":
                bool(
                    os.getenv(
                        "CLAUDE_API_KEY"
                    )
                ),

            "perplexity":
                bool(
                    os.getenv(
                        "PERPLEXITY_API_KEY"
                    )
                )
        }

    def check_services(self):

        results = {}

        for (
            name,
            service
        ) in self.services.items():

            try:

                if hasattr(
                    service,
                    "health_check"
                ):

                    results[name] = (
                        service
                        .health_check()
                    )

                else:

                    results[name] = (
                        "No health_check"
                    )

            except Exception as error:

                results[name] = (
                    f"Error: {error}"
                )

        return results

    def full_health_report(self):

        return {

            "status":
                "running",

            "environment":
                self.check_environment(),

            "api_keys":
                self.check_api_keys(),

            "services":
                self.check_services()
        }


if __name__ == "__main__":

    checker = HealthChecker()

    report = (
        checker
        .full_health_report()
    )

    print(report)
