#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron thaihometown_land is working" >> /home/dev-team/Desktop/scraping/logs/cron.thaihometown_land-$(date +\%Y-\%m-\%d).log 2>&1
python thaihometown_land.py >> "/home/dev-team/Desktop/scraping/logs/cron.thaihometown_land-${DATE}.log" 2>&1
