# Written by: Milanesa-chan (@DevMilanesa)
import datetime, time, threading, ip_updater, apscheduler

from apscheduler.schedulers.background import BackgroundScheduler

def main():
	print("\n{} Updating...".format(datetime.datetime.now()))
	ip_updater.updateAllZones()

main()
scheduler = BackgroundScheduler()
scheduler.add_job(main, "interval", minutes=30)
scheduler.start()

try:
        # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()