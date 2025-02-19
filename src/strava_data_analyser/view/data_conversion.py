from datetime import timedelta
import math


# distance
def m_to_km(meters: float) -> float:
    """
    meters to kilometers conversion
    :param meters: a distance in meters
    :return: the distance in kilometers
    """
    return meters / 1_000


# speed / pace
def mps_to_kmh(mps: float) -> float:
    """
    meters per second to kilometers per hour conversion
    :param mps: a speed in m/s
    :return: the speed in km/h
    """
    return mps * 3.6


def mps_to_minpkm(mps: float) -> tuple:
    """
    meters per second to minutes per kilometer convertion
    :param mps: a speed in m/s
    :return: the pace in min/km
    """
    min_dec_per_km = 60 / mps_to_kmh(mps)

    sec_dec, minutes = math.modf(min_dec_per_km)

    seconds = round(sec_dec * 60)
    return minutes, seconds


# time
def seconds_to_hh_mm_ss(time: int) -> tuple:
    """
    Convert seconds to hours, minutes and seconds
    :time seconds: the number of seconds
    :return: (hours, minutes, seconds)
    """
    td = timedelta(seconds=time)

    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days * 24 + hours, minutes, seconds
