
import datetime as dt
import re

def to_timedelta(tdstr:str):
    """
    Increment a datetime by an amount passed as string.
   
    tdstr - The timedelta amount given as <amount>[unit], e.g.
            [unit] can be one of {m - Minutes,h - Hours ,d - Days]
    """
    deltas = {'m': dt.timedelta(minutes=1), 'h':dt.timedelta(hours=1), 'd':dt.timedelta(days=1)}
    incmatch = re.match(r'(\d+)([m|h|d])', tdstr)
    if not incmatch:
        raise ValueError("Wrong delta string: "+tdstr)

    return deltas.get(incmatch.group(2))*int(incmatch.group(1))
    

def is_before_dealine(deltatodeadline:str, deadline:dt.datetime, now=dt.datetime.now()):
    delta = to_timedelta(deltatodeadline)
    return now <= deadline and deadline - now <= delta
