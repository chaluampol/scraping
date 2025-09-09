#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron homemarket is working" >> /home/dev-team/Desktop/scraping/logs/cron.homemarket-$(date +\%Y-\%m-\%d).log 2>&1
python homemarket2.py >> "/home/dev-team/Desktop/scraping/logs/cron.homemarket-${DATE}.log" 2>&1
