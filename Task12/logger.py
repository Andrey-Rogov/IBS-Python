import logging
import sys

logger = logging.getLogger()

formatter = logging.Formatter(fmt="[%(asctime)s]  {%(filename)s: %(lineno)d} %(levelname)s | %(exec_time)f | %(http_method)s | %(url)s | %(status_code)d |",
                              datefmt="%Y-%m-%d %H:%M:%S")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
