#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron propertyscout is working" >> /home/dev-team/Desktop/scraping/logs/cron.propertyscout-$(date +\%Y-\%m-\%d).log 2>&1
python propertyscout.py >> "/home/dev-team/Desktop/scraping/logs/cron.propertyscout-${DATE}.log" 2>&1
