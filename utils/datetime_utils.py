import calendar
from datetime import datetime, date, timedelta

from django.utils import timezone

utc_tz = timezone.utc
local_tz = timezone.get_current_timezone()

_days_in_month = (
    (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
    (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
)


def now(tz=None):
    tz = tz if tz else local_tz
    return datetime.now(tz=tz)


def max_datetime(tz=None):
    tz = tz or local_tz
    return datetime(9999, 12, 1, tzinfo=tz)


def datetime_to_timestamp(dt):
    if dt is None:
        return None
    if isinstance(dt, datetime):
        pass
    elif isinstance(dt, date):
        dt = datetime.strptime(str(dt), '%Y-%m-%d')
        dt.replace(tzinfo=local_tz)
    return dt.timestamp()


dtt = datetime_to_timestamp


def timestamp_to_datetime(timestamp, tz=None):
    tz = tz if tz else local_tz
    return datetime.fromtimestamp(timestamp, tz=tz)


ttd = timestamp_to_datetime


def convert_tz(dt, tz=local_tz):
    return ttd(dtt(dt), tz=tz)


def addmonths(begindate, months):
    n = begindate.year * 12 + begindate.month - 1
    n = n + months
    ryear = int(n / 12)
    rmonth = n % 12 + 1
    rday = begindate.day

    days_in_month = _days_in_month[1 if calendar.isleap(ryear) else 0]
    if rday > days_in_month[rmonth]:
        rday = days_in_month[rmonth]

    return begindate.replace(year=ryear, month=rmonth, day=rday)


def clean_section(ttype, section):
    begin_time, end_time = section.split(',')
    if begin_time:
        begin_time = timestamp_to_datetime(float(begin_time))
    if end_time:
        end_time = timestamp_to_datetime(float(end_time))
    if ttype in ['week', 'month', 'year']:
        begin_time, end_time = exchange_section(
            ttype, begin_time, end_time)
    return [begin_time, end_time]


def exchange_section(ttype, stime, etime):
    oneday = int(3600 * 24)
    if ttype == 'year':
        return [stime.replace(
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        ), etime]
    if ttype == "month":
        stamp = datetime_to_timestamp(stime)
        stamp = stamp - oneday * (stime.day - 1)
        return timestamp_to_datetime(stamp), etime
    else:
        stime = stime + timedelta(days=-stime.weekday())
        return stime, etime


if __name__ == '__main__':
    import django

    django.setup()

    dt = now(utc_tz)
    print(dt)
    timestamp = datetime_to_timestamp(dt)
    print(timestamp)
    print(timestamp_to_datetime(timestamp))
    print(timestamp_to_datetime(timestamp, tz=utc_tz))
    print(addmonths(datetime.now(), 1))
    print(addmonths(datetime(2016, 1, 31, 0, 0, 0), 1))
