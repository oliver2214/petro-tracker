from datetime import timedelta, datetime


def get_date(date_str):
    if date_str:
        # Преобразование условного "2000-01-01" в datetime(2000, 1, 1)
        return datetime(*[int(el) for el in date_str.split("-")])
    else:
        # Если дата не указана, устанавливается по умолчанию предыдущий день
        return datetime.now() - timedelta(days=1)
