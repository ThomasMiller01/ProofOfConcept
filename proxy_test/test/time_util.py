from datetime import datetime
import pytz


def getCurrentDatetime():
    """Helper function for getting the current datetime from the "Europe/Berlin" timezone.

    :return: current datetime from the "Europe/Berlin" timezone
    :rtype: datetime.datetime
    """
    return datetime.now(pytz.timezone("Europe/Berlin"))
