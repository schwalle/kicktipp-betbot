
import datetime as dt
import re


def to_timedelta(tdstr: str):
    """
    Create a timedelta object by format string

    tdstr - The timedelta amount given as <amount>[unit], e.g. 10m, 2h or 4d
            [unit] can be one of {m - Minutes,h - Hours ,d - Days]
    """
    deltas = {'m': dt.timedelta(minutes=1), 'h': dt.timedelta(
        hours=1), 'd': dt.timedelta(days=1)}
    incmatch = re.match(r'(\d+)([m|h|d])', tdstr)
    if not incmatch:
        raise ValueError("Wrong delta string: "+tdstr)

    return deltas.get(incmatch.group(2))*int(incmatch.group(1))


def is_before_dealine(deltatodeadline: str, deadline: dt.datetime, now=dt.datetime.now()):
    delta = to_timedelta(deltatodeadline)
    return now <= deadline and deadline - now <= delta


def timedelta_tostring(td: dt.timedelta):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hm = '{:02}:{:02}'.format(int(hours), int(minutes))
    if(td.days > 0):
        return '{0} {1} and {2}'.format(td.days, "days" if td.days > 1 else "day", hm)
    else:
        return hm
