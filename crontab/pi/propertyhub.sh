#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron propertyhub is working" >> /home/dev-team/Desktop/scraping/logs/cron.propertyhub-$(date +\%Y-\%m-\%d).log 2>&1
python propertyhub.py >> "/home/dev-team/Desktop/scraping/logs/cron.propertyhub-${DATE}.log" 2>&1
