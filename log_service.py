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

            # Configuração para salvar em arquivo
            log_path = os.getenv('LOG_PATH', 'api.log')
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.INFO)

            # Configuração para console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Formato do log
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            LogService._logger.addHandler(file_handler)
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