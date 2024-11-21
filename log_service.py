import logging
import os
from datetime import datetime
import json

class LogService:
    _logger = None

    @staticmethod
    def get_logger():
        if LogService._logger is None:
            LogService._logger = logging.getLogger('flask_api')
            LogService._logger.setLevel(logging.INFO)

            # Apenas configuração para console no Railway
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Formato do log com mais informações para debug
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )
            console_handler.setFormatter(formatter)
            LogService._logger.addHandler(console_handler)

        return LogService._logger

    @staticmethod
    def error(message: str, error: Exception = None):
        logger = LogService.get_logger()
        if error:
            logger.error(f"{message}: {str(error)}")
        else:
            logger.error(message)

    @staticmethod
    def info(message: str):
        logger = LogService.get_logger()
        logger.info(message)

    @staticmethod
    def rate_limit_exceeded(request_path: str, limit: str):
        logger = LogService.get_logger()
        logger.warning(f"Rate limit exceeded for path: {request_path} - Limit: {limit}")

    @staticmethod
    def structured_log(level: str, event: str, data: dict):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'event': event,
            'data': data
        }
        logger = LogService.get_logger()
        getattr(logger, level.lower())(json.dumps(log_entry))
