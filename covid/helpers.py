
import datetime as datetime


def parsedate(input: str) -> datetime.datetime:
    """
    Parses the John Hopkins format into a datetime object
    This *should* be '%m/%d/%y', but for some reason using that format
    makes datetime expect an actual time

    :param input:
    :return:
    """

    inputt = input.replace("/","-")
    return datetime.datetime.strptime(inputt, "%m-%d-%y")

def date_fmt(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d")