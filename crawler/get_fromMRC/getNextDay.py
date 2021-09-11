from datetime import datetime, timedelta

def get_time(elm):
    if '[' not in elm:
        date = datetime.strptime(elm, '%a-%b-%d-%H:%M:%S-+0000-%Y')
    else:
        date = datetime.strptime(elm, '[\"melbourne\",%Y,%m,%d]')
    return date

def next_date(date):
    delta = timedelta(days=1)
    date += delta
    return '[\"melbourne\",{}]'.format(date.strftime('%Y,%m,%d'))

date_str = '[\"melbourne\",2016,12,25]'
while True:
    date = get_time(date_str)
    date_str = next_date(date)
    if date == datetime(2017,1,30):
        break
    print(date_str)





'''10000 max
count = 7
while:
    data(100)
    count -= 1
    if count ==0:
        save data 100
        try:
            json 解析
        except:
            last date 
            date = next day
        count = 7'''