#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron baania is working" >> /home/dev-team/Desktop/scraping/logs/cron.baania-$(date +\%Y-\%m-\%d).log 2>&1
python baania.py >> "/home/dev-team/Desktop/scraping/logs/cron.baania-${DATE}.log" 2>&1
