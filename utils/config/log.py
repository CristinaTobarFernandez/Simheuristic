import logging
class ConfigLog():
    def __init__(self):
        pass

    @staticmethod
    def config():
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO)
