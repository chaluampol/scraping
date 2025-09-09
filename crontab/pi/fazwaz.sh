#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron fazwaz is working" >> /home/dev-team/Desktop/scraping/logs/cron.fazwaz-$(date +\%Y-\%m-\%d).log 2>&1
python fazwaz.py >> "/home/dev-team/Desktop/scraping/logs/cron.fazwaz-${DATE}.log" 2>&1
