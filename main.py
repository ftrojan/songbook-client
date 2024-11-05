import logging
import songbook


logging.basicConfig(level="INFO")
logging.info("started")
local_dir = "/Users/filip/Downloads/songbook"
songbook.sync(local_dir=None)
logging.info("completed")
