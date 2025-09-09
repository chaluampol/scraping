#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron klungbaan is working" >> /home/dev-team/Desktop/scraping/logs/cron.klungbaan-$(date +\%Y-\%m-\%d).log 2>&1
python klungbaan.py >> "/home/dev-team/Desktop/scraping/logs/cron.klungbaan-${DATE}.log" 2>&1
