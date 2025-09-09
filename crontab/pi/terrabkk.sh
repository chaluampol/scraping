#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron terrabkk is working" >> /home/dev-team/Desktop/scraping/logs/cron.terrabkk-$(date +\%Y-\%m-\%d).log 2>&1
python terrabkk.py >> "/home/dev-team/Desktop/scraping/logs/cron.terrabkk-${DATE}.log" 2>&1
