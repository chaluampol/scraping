#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron ddproperty is working" >> /home/dev-team/Desktop/scraping/logs/cron.ddproperty-$(date +\%Y-\%m-\%d).log 2>&1
python ddproperty_v4.py >> "/home/dev-team/Desktop/scraping/logs/cron.ddproperty-${DATE}.log" 2>&1
