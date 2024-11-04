import logging
import songbook


logging.basicConfig(level="INFO")
logging.info("started")
local_dir = "/storage/emulated/0/Download/songbook"
local_dir = "/Users/filip/Downloads/songbook"
songbook.sync(local_dir)
logging.info("completed")
