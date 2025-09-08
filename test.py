import reic_function as fn
from datetime import datetime, timedelta

# date = datetime.today().strftime('%Y-%m-%d') # auto
date = datetime(2025, 9, 9).strftime('%Y-%m-%d') # manual
web="livinginsider"
fn.send_message(date, web)