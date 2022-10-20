import contextlib
import logging
from time import time


@contextlib.contextmanager
def timing(message: str):
    start_time = time()
    logging.info(f"Started {message}.")
    yield
    logging.info(f"Finished {message} in {time() - start_time}")
