import logging


def set_log_level(log_level: str):
    """Set the log level for the Python logging system.

    This function allows you to configure the log level for the Python logging system.
    The log level determines which log messages will be displayed. Log levels are
    defined as strings and are case-insensitive.

    Args:
        log_level (str): The desired log level. It should be one of the following strings:
            - 'DEBUG': Detailed debugging information.
            - 'INFO': Informational messages.
            - 'WARNING': Warning messages.
            - 'ERROR': Error messages.
            - 'CRITICAL': Critical error messages.

    Raises:
        ValueError: If the provided log level is not a valid log level string.

    Example:
        To set the log level to 'DEBUG', you can call the function as follows:
        set_log_level('DEBUG')

    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log_level)
    logging.basicConfig(level=numeric_level)
