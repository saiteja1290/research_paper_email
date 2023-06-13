import schedule
import time

def printing():
    print("Hey")


schedule.every(10).seconds.do(printing)


while 1:
    schedule.run_pending()
    time.sleep(1)