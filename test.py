import re
import datetime

time = datetime.datetime.strptime("02-01", "%m-%d")
curr_time = datetime.datetime.now().strftime("%m-%d")
curr_time = datetime.datetime.strptime(curr_time, "%m-%d")
if (curr_time - time).days == 1:
    print("aaa")
else:
    print("bbb")
