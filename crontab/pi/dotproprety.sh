#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron dotproprety is working" >> /home/dev-team/Desktop/scraping/logs/cron.dotproprety-$(date +\%Y-\%m-\%d).log 2>&1
python dotproprety.py >> "/home/dev-team/Desktop/scraping/logs/cron.dotproprety-${DATE}.log" 2>&1
