#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron thaihometown is working" >> /home/dev-team/Desktop/scraping/logs/cron.thaihometown-$(date +\%Y-\%m-\%d).log 2>&1
python thaihometown.py >> "/home/dev-team/Desktop/scraping/logs/cron.thaihometown-${DATE}.log" 2>&1
