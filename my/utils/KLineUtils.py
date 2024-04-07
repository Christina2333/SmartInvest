import datetime


def get_time(time):
    dt = datetime.datetime.fromtimestamp(time/1000)
    formatted_date_str = dt.strftime('%Y%m%d')
    return int(formatted_date_str)


if __name__ == '__main__':
    id = 'SH688303'
    id = id.replace('SH', '').replace('SZ', '')
    print(id)