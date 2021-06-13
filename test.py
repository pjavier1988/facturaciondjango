import datetime
from dateutil.relativedelta import relativedelta

current_date = datetime.datetime.now()
old_date = current_date + relativedelta(months=-8)

print (current_date)
print (old_date)
print (str(old_date.strftime('%A')))
