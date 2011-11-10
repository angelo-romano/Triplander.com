# -*- coding: utf-8 -*-
import re
#import json
import math
import marshal
import urllib
import urllib2
import codecs
import string
import os.path
#import simplejson
#iport MySQLdb
#from rhyvee.RhyveeReader import *
from datetime import datetime
from django.db import connection
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.utils.encoding import smart_unicode, force_unicode
from django.utils import simplejson
from django.contrib.gis.maps.google import *
from django.template import TemplateDoesNotExist
from django.core.urlresolvers import reverse # URL reversal
from django.template.defaultfilters import slugify # slugify function

# caching modules/functions
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache

#from geolocal import LocalGeoRepr
from triplander.models import *
from triplander.functions import *
from triplander.remote import *
from triplander.functions import dab_string, tl_response, get_wikiname_by_url
from triplander.settings import GOOGLEMAPS_APIKEY
from triplander.update import add_new_city, update_city

# basic imports
from triplander.views.base    import *
from triplander.views.city    import *
from triplander.views.country import *