# scraping

## Create a virtual environment
``` shell
python3 -m venv myenv
source myenv/bin/activate

# example
pip install -r requirements.txt
```

## Allow execute script
``` shell
# pi
chmod +x /home/dev-team/Desktop/scraping/crontab/pi/*.sh 
```

## Pi Crontab
``` shell
# everyday at 06:00
0 6 * * * /home/dev-team/Desktop/scraping/crontab/pi/baanfinder.sh

# every saturday at 14:00
0 14 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/baania.sh

# every saturday at 15:00
0 15 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/dotproprety.sh

# every saturday at 18:00
0 18 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/interhome.sh

# every saturday at 19:00
0 19 * * 6 /home/dev-team/Desktop/scraping/crontab/pi/kaidee.sh

# every sunday at 14:00
0 14 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/klungbaan.sh

# every sunday at 16:00
0 16 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/terrabkk.sh

# every sunday at 17:00
0 17 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/thaihometown.sh

# every sunday at 19:00
0 19 * * 7 /home/dev-team/Desktop/scraping/crontab/pi/thaihometown_land.sh
```
