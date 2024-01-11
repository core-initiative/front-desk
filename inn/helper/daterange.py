from datetime import timedelta, date, datetime

def daterange(start_date: datetime, end_date: datetime) -> list[date]:
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)