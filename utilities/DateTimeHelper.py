import datetime


def abctest1():
    abc = datetime.datetime.strptime("2018-09-10", StdDateFormat)

    print(abc.timestamp())
    print(datetime.datetime.now().timestamp())

    print(abc)

    print(datetime.datetime.now().strftime(StdDateTimeFormat))

    # datetime.datetime.now().timestamp()

    abc1 = datetime.datetime.fromtimestamp(1536508800.0)
    print(abc1.strftime(StdDateTimeFormat))


def today():
    return datetime.datetime.now().strftime(StdDateTimeFormat)


def date1_before_date2(date1: str, date2: str):
    time1 = datetime.datetime.strptime(date1, StdDateFormat).timestamp()
    time2 = datetime.datetime.strptime(date2, StdDateFormat).timestamp()

    return time1 <= time2


def date_length(date1: str, date2: str):
    time1 = datetime.datetime.strptime(date1, StdDateFormat).timestamp()
    time2 = datetime.datetime.strptime(date2, StdDateFormat).timestamp()

    days = int((time2 - time1) / 3600 / 24)

    return days


def date_length_today(date: str):
    nowDate = datetime.datetime.now().strftime(StdDateFormat)

    return date_length(date, nowDate)


def date_before_today(date: str):
    time = datetime.datetime.strptime(date, StdDateFormat).timestamp()

    now = datetime.datetime.now().timestamp()

    return time < now


def date_fmt_test():
    data1 = "2015-03-02 09:35:00"
    data2 = "2015-03-02"

    time1 = datetime.datetime.strptime(data1, StdDateTimeFormat)

    time2 = datetime.datetime.strptime(data2, StdDateFormat)

    print(time1)
    print(time2)


def format_date(strings):
    return datetime.datetime.strptime(strings, "%Y%m%d").strftime(StdDateFormat)


StdDateTimeFormat = "%Y-%m-%d %H:%M:%S"
StdDateFormat = "%Y-%m-%d"
StdDateEditFormat = "yyyy-MM-dd"

# date_fmt_test()

# # Entry for testing
if __name__ == "__main__":
    # abc()

    abc = datetime.datetime.strptime("20180910", "%Y%m%d").strftime(StdDateFormat)
    print(abc)
