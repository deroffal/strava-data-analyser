from datetime import timedelta

from . import data_conversion


def seconds_as_hhmmss(time: int) -> str:
    """
    Convert seconds to hours, minutes and seconds
    :time seconds: the number of seconds
    :return: a string with the number of hours, minutes and seconds (hh:mm:ss)
    """
    td = timedelta(seconds=time)

    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    total_hours = str(days * 24 + hours).zfill(2)
    total_minutes = str(minutes).zfill(2)
    total_seconds = str(seconds).zfill(2)
    return f"{total_hours}:{total_minutes}:{total_seconds}"


def m_as_km(meters: int) -> str:
    """
    Display meters as kilometers
    :param meters: the number of meters
    :return: the conversion (km,mm)
    """
    return f"{round(data_conversion.m_to_km(meters), 2)}km"


def mps_as_kmh(speed: float) -> str:
    """
    Display m/s as km/h
    :param speed: speed in meter per seconde
    :return: speed in kilometer per hour
    """
    return f"{round(data_conversion.mps_to_kmh(speed), 2)}km/h"


def mps_as_minpkm(speed: float) -> str:
    """
    Display m/s as min/km
    :param speed: speed in meter per seconde
    :return: pace in min per kilometer
    """
    pace = data_conversion.mps_to_minpkm(speed)
    minutes = round(pace[0])
    seconds = str(pace[1]).zfill(2)
    return f"{minutes}:{seconds}min/km"


def bpm(rate: int) -> str:
    return f"{round(rate)}bpm"


def m(meters: int) -> str:
    return f"{round(meters)}m"
