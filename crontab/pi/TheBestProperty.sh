#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron TheBestProperty is working" >> /home/dev-team/Desktop/scraping/logs/cron.TheBestProperty-$(date +\%Y-\%m-\%d).log 2>&1
python TheBestProperty.py >> "/home/dev-team/Desktop/scraping/logs/cron.TheBestProperty-${DATE}.log" 2>&1
