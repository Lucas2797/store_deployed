import datetime


def generate_order_id():
    date_str = datetime.date.today().strftime('%d%m%Y') + str(datetime.datetime.now().time())[:5]
    return date_str