#!/bin/bash
cd /home/dev-team/Desktop/scraping/
python3 -m venv myenv
source myenv/bin/activate

DATE=$(date +'%Y-%m-%d')

echo "$(date) cron hongpak is working" >> /home/dev-team/Desktop/scraping/logs/cron.hongpak-$(date +\%Y-\%m-\%d).log 2>&1
python hongpak.py >> "/home/dev-team/Desktop/scraping/logs/cron.hongpak-${DATE}.log" 2>&1
