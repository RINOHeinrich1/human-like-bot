import logging

import logging

def setup_logger(log_file='onir_linkedin.log'):
    logger = logging.getLogger("onir_logger")
    logger.setLevel(logging.INFO)

    # Évite les handlers dupliqués si le logger est appelé plusieurs fois
    if not logger.handlers:
        fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        logger.addHandler(fh)

    return logger

