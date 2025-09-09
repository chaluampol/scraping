#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron kaidee is working" >> /home/dev-team/Desktop/scraping/logs/cron.kaidee-$(date +\%Y-\%m-\%d).log 2>&1
python kaidee_V3.py >> "/home/dev-team/Desktop/scraping/logs/cron.kaidee-${DATE}.log" 2>&1
