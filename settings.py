import os


ROOT_FOLDER = os.path.dirname(__file__)
TEMP_FOLDER = os.path.join(ROOT_FOLDER, "temp")

# 60 * 5 --> 5 minutes
EXPIRATION_TIME = 60 * 60 * 24 * 2  # 2 days
CHUNK_SIZE = 1024 * 1024

IS_DEV_ENVIRONMENT = False
try:
    import __dev__

    IS_DEV_ENVIRONMENT = True
except ImportError:
    pass

if not os.path.exists(TEMP_FOLDER):
    os.mkdir(TEMP_FOLDER)
