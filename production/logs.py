# production/logs.py

import os
import json
from datetime import datetime


class Logger:

    def __init__(
        self,
        log_file="mythos_logs.jsonl"
    ):

        self.log_file = log_file

    def _write(
        self,
        level,
        source,
        message,
        extra=None
    ):

        log_entry = {

            "timestamp":
                datetime.now()
                .isoformat(),

            "level":
                level,

            "source":
                source,

            "message":
                message,

            "extra":
                extra or {}
        }

        try:

            with open(
                self.log_file,
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    json.dumps(
                        log_entry,
                        ensure_ascii=False
                    )
                    + "\n"
                )

        except Exception as error:

            print(
                f"Log Error: {error}"
            )

    def info(
        self,
        source,
        message,
        extra=None
    ):

        self._write(
            "INFO",
            source,
            message,
            extra
        )

    def warning(
        self,
        source,
        message,
        extra=None
    ):

        self._write(
            "WARNING",
            source,
            message,
            extra
        )

    def error(
        self,
        source,
        message,
        extra=None
    ):

        self._write(
            "ERROR",
            source,
            message,
            extra
        )

    def ai_request(
        self,
        model,
        prompt_length
    ):

        self.info(

            source="AI_REQUEST",

            message=(
                f"Model={model}"
            ),

            extra={
                "prompt_length":
                prompt_length
            }
        )

    def ai_response(
        self,
        model,
        response_length
    ):

        self.info(

            source="AI_RESPONSE",

            message=(
                f"Model={model}"
            ),

            extra={
                "response_length":
                response_length
            }
        )

    def system_start(self):

        self.info(

            source="SYSTEM",

            message=(
                "Mythos AI started"
            )
        )

    def system_stop(self):

        self.info(

            source="SYSTEM",

            message=(
                "Mythos AI stopped"
            )
        )

    def read_recent(
        self,
        limit=50
    ):

        if not os.path.exists(
            self.log_file
        ):

            return []

        try:

            with open(
                self.log_file,
                "r",
                encoding="utf-8"
            ) as file:

                lines = file.readlines()

            results = []

            for line in lines[-limit:]:

                try:
                    results.append(
                        json.loads(line)
                    )

                except:
                    pass

            return results

        except Exception:

            return []


if __name__ == "__main__":

    logger = Logger()

    logger.system_start()

    logger.info(
        "TEST",
        "Logger working"
    )

    logger.ai_request(
        "openai",
        150
    )

    logger.ai_response(
        "openai",
        500
    )

    print(
        logger.read_recent(10)
        )
