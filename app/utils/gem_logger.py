from loguru import logger

logger.info('Setup logger from loguru library.')


def setup_file_logger(log_file_path, log_level):
    logger.add(log_file_path, level=log_level, rotation="1 day")
    logger.info(f'log into file `{log_file_path}`' )

