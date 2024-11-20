import logging
import os
from datetime import datetime

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