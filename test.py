import reic_function as fn
from datetime import datetime, timedelta

# date = datetime.today().strftime('%Y-%m-%d') # auto
date = datetime(2025, 9, 8).strftime('%Y-%m-%d') # manual
web="baania"
fn.check_data(date, web)
# fn.send_message(date, web)