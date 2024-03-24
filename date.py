from datetime import datetime, date

converted = datetime.strptime("01/02/2006 16:30:00", '%d/%m/%Y %H:%M:%S')

date_time_now =  str(datetime.now().strftime('%d/%m/%y %H:%M:%S'))
date_time_now_changed = datetime.strptime(date_time_now, '%d/%m/%y %H:%M:%S')

print(converted)
print(date_time_now_changed)

if converted < date_time_now_changed:
    print("hello")