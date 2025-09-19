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
# everyday at 05:00
0 5 * * * /home/dev-team/Desktop/scraping/crontab/pi/baanfinder.sh

# every tuesday at 14:30
30 14 * * * /home/dev-team/Desktop/scraping/crontab/pi/thaihometown.sh

# everyday at 18:00
0 18 * * * /home/dev-team/Desktop/scraping/crontab/pi/livinginsider.sh

# every monday at 14:00
0 14 * * 1 /home/dev-team/Desktop/scraping/crontab/pi/baania.sh

# every monday at 15:00
0 15 * * 1 /home/dev-team/Desktop/scraping/crontab/pi/dotproprety.sh

# every monday at 18:00
0 18 * * 1 /home/dev-team/Desktop/scraping/crontab/pi/interhome.sh

# every monday at 19:00
0 19 * * 1 /home/dev-team/Desktop/scraping/crontab/pi/kaidee.sh

# every tuesday at 14:00
0 14 * * 2 /home/dev-team/Desktop/scraping/crontab/pi/klungbaan.sh

# every tuesday at 16:00
0 16 * * 2 /home/dev-team/Desktop/scraping/crontab/pi/terrabkk.sh

# every tuesday at 19:00
# 0 19 * * 2 /home/dev-team/Desktop/scraping/crontab/pi/thaihometown_land.sh
```
