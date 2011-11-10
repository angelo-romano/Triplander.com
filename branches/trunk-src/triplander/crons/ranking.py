import os
import sys

os.putenv('DJANGO_SETTINGS_MODULE','triplander.settings')
sys.path.append('/home/angelo/workspace')

from triplander.cron import *

#s = generate_rankings(range=(sys.argv[1],sys.argv[2]))
#s = generate_panoramio_rankings(range=(sys.argv[1],sys.argv[2]))
#s = generate_requested_rankings(range=(sys.argv[1],sys.argv[2]))
#s = generate_yahootravel_rankings(range=(sys.argv[1],sys.argv[2]))
s = update_all_ratings()
#s = find_suspect_ratings()
print s
