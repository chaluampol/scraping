#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron bangkokassets is working" >> /home/dev-team/Desktop/scraping/logs/cron.bangkokassets-$(date +\%Y-\%m-\%d).log 2>&1
python bangkokassets.py >> "/home/dev-team/Desktop/scraping/logs/cron.bangkokassets-${DATE}.log" 2>&1
