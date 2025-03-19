import logging


def handle_exceptions(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as ex:
            error_str = (f"Excepcion en {type(self).__name__}::{func.__name__}(): {str(ex)}")
            logging.error(error_str)
            raise Exception(error_str)
    return wrapper
