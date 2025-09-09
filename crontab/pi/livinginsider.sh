#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron livinginsider is working" >> /home/dev-team/Desktop/scraping/logs/cron.livinginsider-$(date +\%Y-\%m-\%d).log 2>&1
python livinginsider_V2.py >> "/home/dev-team/Desktop/scraping/logs/cron.livinginsider-${DATE}.log" 2>&1
