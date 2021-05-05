import datetime



def dateVerify(day,month,year):
  
  try:
    if (month<1 or month>12):
      pass
    elif (day<1 and day>31):
      pass
    else:
    print(datetime.date(year,month,day))
  except ValueError: