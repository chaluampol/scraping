# scraping

Create a virtual environment
``` shell
python3 -m venv .venv
source .venv/bin/activate

# example
pip install -r requirements.txt
```

Pi Crontab
``` shell
# everyday at 06:00
0 6 * * * /home/dev-team/Desktop/scraping/crontab/pi/baanfinder.sh

# everyday saturday at 14:00
0 14 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/baania.sh

# everyday saturday at 15:00
# 0 15 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/dotproprety.sh

# everyday saturday at 18:00
0 18 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/interhome.sh

# everyday saturday at 19:00
0 19 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/kaidee.sh

# everyday sunday at 14:00
0 14 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/klungbaan.sh

# everyday sunday at 16:00
# 0 16 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/terrabkk.sh

# everyday sunday at 17:00
0 17 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/thaihometown.sh

# everyday sunday at 19:00
0 19 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/thaihometown_land.sh
```
