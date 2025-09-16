import reic_function as fn
from datetime import datetime

# date = datetime.today().strftime('%Y-%m-%d') # auto
date = datetime(2025, 9, 14).strftime('%Y-%m-%d') # manual
web="livinginsider"

# chack data.
fn.check_data(date, web)

# send line message.
fn.send_message(date, web)

# get google drive refresh token.
fn.get_gdrive_refresh_token()

# upload files to google drive.
fn.upload_processing(date, web)