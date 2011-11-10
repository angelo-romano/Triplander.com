from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.utils import simplejson
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D # `D` is a shortcut for `Distance`
from django.core.cache import cache
from xml.dom import minidom
from triplander.models import *
from triplander.functions import getCityObject

import urllib
import urllib2
import types
import random
import time
import math

def callAssociateFunction(what,params):
    resp = None
    if(what == 'getDestinations'):
        resp = _getDestinations(params['dfrom'])
    elif(what == 'getCityFromAirport'):
        resp = _getCityFromAirport(params['dfrom'])
    elif(what == 'getCityFromName'):
        resp = _getCityFromName(params['dfrom'])
    elif(what == 'getClosestAirports'):
        resp = _getClosestAirports(params['dfrom'])
    elif(what == 'getClosestCities'):
        if(params.has_key('more')):
            resp = _getClosestCities(params['dfrom'],params['more'])
        else:
            resp = _getClosestCities(params['dfrom'])
    elif(what == 'getAirportCoordinates'):
        resp = _getAirportCoordinates(params['dfrom'])
    elif(what == 'getRandomCities'):
        resp = _getRandomCities(params['dfrom'])
    else:
        resp = None
        
    if (params.has_key('http') and params['http'] is True):
        if resp is None: return HttpResponseNotFound('Object Not Found')
        jsonResp = simplejson.dumps(resp)
        return HttpResponse(jsonResp)
    elif (params.has_key('json') and params['json'] is True):
        if resp is None: return "{}";
        jsonResp = simplejson.dumps(resp)
        #jsonResp = response.replace("{", "\n{")
        return jsonResp
    else:
        return resp

def _getDestinations(dfrom):   
    source = Station.objects.get(code_alt = dfrom)
    cities = City.objects.filter(coordinates__distance_gt=(source.coordinates,D(km=500)),
                                 coordinates__distance_lt=(source.coordinates,D(km=1000)))
    
    dests = Station.objects.filter(city__in=cities)
    
    for d in dests:
        d.short_name = unicode(urllib.quote(d.short_name.encode('utf8')," ,-"))
        #d.short_name = d.short_name.encode('utf8')
    
    #json_ser = serializers.get_serializer('json')()
    #json_ser.serialize(dests,fields=('code_alt','short_name'),ensure_ascii=False)
    
    return dests

def _getCityFromAirport(dfrom):
    source = Station.objects.get(code_alt = dfrom)
    popularity = City.objects.filter(coordinates__distance_lt=(source.coordinates,D(km=180))).count()
    
    jsonObject = {
                  'city': unicode(urllib.quote(source.city.name.encode('utf8')," ,-")),
                  'latitude': float(source.city.latitude),
                  'longitude': float(source.city.longitude),
                  'popularity': popularity
                 }
                        
    #json_ser = serializers.get_serializer('json')()
    #json_ser.serialize(city,ensure_ascii=False)
    
    #return (json.write(jsonObject).encode("utf8"))
    return jsonObject

def _getCityFromName(dfrom):
    city = getCityObject(name=dfrom)
    response = None
    
    if city is None: 
        return None
    else:     
        jsonObject = {
                      'city': unicode(urllib.quote(city.name.encode('utf8')," ,-")),
                      'latitude': float(city.latitude),
                      'longitude': float(city.longitude),
                     }
                            
        #json_ser = serializers.get_serializer('json')()
        #json_ser.serialize(city,ensure_ascii=False)
        
        #return (json.write(jsonObject).encode("utf8"))
        return jsonObject

def getCityObjectFromName(dfrom):
    return getCityObject(name=dfrom)

def _getAirportCoordinates(dfrom):
    airport = Station.objects.get(code_alt = dfrom)
    if airport is None: return None
    return airport.coordinates

def _getCityCoordinates(dfrom):
    city = getCityObject(name=dfrom)
    if city is None: return None
    return city.coordinates

def _getClosestAirports(dfrom):
    city = getCityObject(id=dfrom)
    if city is None: return None
    #return HttpResponseNotFound('City Not Found')

    # up to 20 airprots, with a distance <= 300 km
    closest_airports = Station.objects.filter(
                                              coordinates__distance_lt=
                                              (city.coordinates,D(km=300))).transform().distance(city.coordinates)[:20]

    # city representation
    jsonCity = {"name": city.name, 
                "x"   : city.coordinates.x, 
                "y"   : city.coordinates.y, 
                "id"  : city.id,
                "slug": city.slug}
    
    jsonSet = {"city"    : jsonCity,
               "airports": None}

    jsonObj = []
    
    minimumSelection = False
    minimumSelectionNum = 10
    
    if (len(closest_airports) < minimumSelectionNum):
        closest_airports = Station.objects.filter(coordinates__distance_lt=(city.coordinates,D(km=500))).distance(city.coordinates)
        #closest_airports.sort(lambda x,y: x.distance - y.distance)
        minimum_selection = True
        
    for c in closest_airports:
        
        jsonElem = {'code'    : c.code_alt, 
                    'name'    : unicode(urllib.quote(c.short_name.encode('utf8')," ,-")),
                    'distance': c.distance.km, 
                    'x'       : c.coordinates.x, 
                    'y'       : c.coordinates.y }
        jsonObj.append(jsonElem)

    jsonObj.sort(lambda x,y: int(math.floor(x['distance']-y['distance'])))
      
    if (minimumSelection): jsonObj = jsonObj[:minimumSelectionNum]
    jsonSet['airports'] = jsonObj

    #response = simplejson.dumps(jsonSet)
    
    #response = response.replace("{", "\n{")
    return jsonSet
    #return HttpResponse(response)

def _getRandomCities(dfrom=None,more=None):
    if(dfrom is not None): 
        howmany = dfrom
    else:
        howmany = 50
        
    cities = City.objects.all()
    city_selection = random.sample(xrange(len(cities)),howmany)
    
    return [cities[i] for i in city_selection]

def _getClosestCities(dfrom,more=None):
    #city = __getCityObjectFromName(dfrom)
    city = getCityObject(id=dfrom)
    if city is None: return None
       
    c_distance  = 300
    c_limit     = 250
    c_randomize = False
    c_cycle     = True
    c_usecache  = False
    
    if(more is None):
        pass
    else:
        if(more.has_key('distance') and more['distance'] is not None): c_distance=more['distance']
        if(more.has_key('limit') and more['limit'] is not None): c_limit=more['limit']
        if(more.has_key('randomize') and more['randomize'] is not None): c_randomize=more['randomize']
        if(more.has_key('usecache') and more['usecache'] is True): c_usecache = True
        
    jsonObj = None
    if(c_usecache):
        # whole set of nearby cities can be cached - 
        # they are stored purely, with no randomization or selection
    
        c_cache_key = "remote.getClosestCities[%d]" % (dfrom)
        c_cache_timeout = 60*60*24*5 # 5 days
        jsonObj = cache.get(c_cache_key)
    
    if(jsonObj is None): # nothing cached yet
        
        # the big deal - retrieving all nearby cities
        c_distance_base = c_distance * 0.667
    
        while(c_cycle):       
            closest_cities = City.objects.filter(coordinates__distance_lt=(city.coordinates,D(km=c_distance))).transform().distance(city.coordinates)
            if(len(closest_cities)<(c_limit+1)):
                c_distance = c_distance + c_distance_base
            else:
                c_cycle = False
                
        jsonObj  = []
        
        # selecting and converting to a proper format to be returned as json
        for c in closest_cities:
            if (c != city):       
                jsonElem = {"name": c.name, "country": c.country.name,
                            "x": c.coordinates.x, "y": c.coordinates.y,
                            "distance": c.distance.km, "slug": c.slug,
                            "id": c.pk }
                if (c.local_name is not None and c.local_name != ''):
                    jsonElem["local_name"] = c.local_name
                jsonObj.append(jsonElem)
                
    jsonCity = {"name": city.name, "x": city.coordinates.x, "y": city.coordinates.y}
    jsonSet  = {"city": jsonCity, "nearby_cities": None}

    if (c_usecache): cache.set(c_cache_key,jsonObj,c_cache_timeout) # store into cache
    if (c_randomize): random.shuffle(jsonObj)
    if (c_limit is not None and c_limit > 0): jsonObj = jsonObj[:c_limit]
    
    jsonObj.sort(lambda x,y: int(math.floor(x['distance']-y['distance'])))
    
    jsonSet['nearby_cities'] = jsonObj
    return jsonSet

def get_http_scheduler(delta=None):
    try:
        if(delta is not None):
            scheduler = HTTPRequestScheduler()
        else:
            scheduler = HTTPRequestScheduler(delta=delta)
    except Singleton, s:
        scheduler = s
        
    return scheduler

class Singleton: # singleton -> used for httprequestscheduler -> MANDATORY
    __single = None
    def __init__( self ):
        if Singleton.__single:
            raise Singleton.__single
        Singleton.__single = self
        
class HTTPRequestScheduler(Singleton): # http request scheduler
    """TODO: CACHING SUPPORT (urgent!)"""
    _services = {
                 "wikipedia"  : 0,
                 "panoramio"  : 0,
                 "commons"    : 0,
                 "yahootravel": 0,
                 "earthtools" : 0,
                 }
    
    _delta = 0
    _default_delta = 0
    def __init__(self,delta=0): # initialization
        Singleton.__init__( self )
        self._delta = delta
    
    def urlopen(self,service,url,alt_delta=None,json=False,xml=False,usecache=False):
        # open a service url
        # delta is the minimum amount between two consecutive calls 
        if(self._delta is None): self._delta = self._default_delta
        this_delta = self._delta
        if (alt_delta is not None): this_delta = alt_delta 
        if(not self._services.has_key(service)): return None
        if(self._services[service] is None): self._services[service] = 0
        if(time.time() <= (self._services[service] + this_delta)):
            if(this_delta > 0): time.sleep(this_delta)
        
        http_completed  = False
        http_tentatives = 0

        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        
        # send call
        while(not http_completed):
            try:
                httpresp = opener.open(url)
                httpwhat = httpresp.read()
                http_completed = True
            except urllib2.HTTPError:
                time.sleep(3)
                http_tentatives = http_tentatives + 1
                if (http_tentatives == 3):
                    http_completed = True
                    raise urllib2.HTTPError("Not working: %s" % url)
                else:
                    http_tentatives = 0
                    http_completed = False
        
        # store time
        self._services[service] = time.time()
        
        # json/xml conversion
        if(json is True): httpwhat = simplejson.loads(httpwhat)
        if(xml is True):
            #the usual unicode mess
            httpwhat = httpwhat.replace('<?xml version="1.0"?>','<?xml version="1.0" encoding="ISO-8859-15"?>').decode('latin1').encode('latin1')
            httpwhat = minidom.parseString(httpwhat)
        
        return httpwhat
    
    def _cacheGet(self,url):
        return None
    
    def _cacheStore(self,url,content):
        pass