#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron interhome is working" >> /home/dev-team/Desktop/scraping/logs/cron.interhome-$(date +\%Y-\%m-\%d).log 2>&1
python interhome.py >> "/home/dev-team/Desktop/scraping/logs/cron.interhome-${DATE}.log" 2>&1
