from triplander.models import City, Country, CityRedirect
from triplander.geoinfo import wikipedia_ranking, panoramio_ranking, _wikipedia_article, yahootravel_ranking, city_timezone

import urllib
import math
import decimal

def generate_all_rankings(whatever=None,skip_if_set=True,range=(0,0)):
    cities = City.objects.all()[range[0]:range[1]]
    resp = ""
    for c in cities:
        wname = None
        if c.wikiname is None:
            name = _wikipedia_article(c.name)
            if (name is not None): wname = name['wikiname']
        else:
            if(skip_if_set is True):
                wname = None
            else:
                wname = c.wikiname

        if wname is not None:
            r1 = (wikipedia_ranking(wname))
            r2 = (panoramio_ranking(c.name))
            r3 = decimal.Decimal("0.0")            
                
            c.wikiname = wname
            c.setRating(r1['content'],r2,r3)
            c.save()
            
                
            resp += "%s (%s) [%d,%d]\n" % (c.name,wname,r1['content'],r2)
    
    resp += "Done\n"
    
    return resp

def generate_panoramio_rankings(whatever=None,skip_if_set=True,range=(0,0)):
    cities = City.objects.all()[range[0]:range[1]]
    resp = ""
    for c in cities:
        r2 = (panoramio_ranking(c.id))
            
        c.rating_factor_2 = r2
        c.save()
        resp += "%s (%s) [%d]\n" % (c.name,c.wikiname,r2)

    resp += "Done\n"
    
    return resp

def generate_requested_rankings(whatever=None,skip_if_set=True,range=(0,0)):
    cities = City.objects.filter(recompute=True)[range[0]:range[1]]
    resp = ""
    for c in cities:
                
        r1 = (wikipedia_ranking(c.wikiname))
        r2 = (panoramio_ranking(c.id))
        r3 = (yahootravel_ranking(c.id))            
                
        c.setRating(r1['content'],r2,r3)        
        #c.rating_factor_2 = r2   
        c.save()

        resp += "%s (%s) [%d,%d,%d]\n" % (c.name,c.wikiname,r1['content'],r2,r3)
    
    resp += "Done\n"
    
    return resp

def generate_yahootravel_rankings(whatever=None,skip_if_set=True,range=(0,0)):
    cities = City.objects.all()[range[0]:range[1]]
    resp = ""
    for c in cities:
        r3 = (yahootravel_ranking(c.id))
            
        c.rating_factor_3 = r3
        c.save()
        resp += "%s (%s) [%d]\n" % (c.name,c.wikiname,r3)

    resp += "Done\n"
    
    return resp

def find_suspect_ratings():
    all_cities = City.objects.all()
    rating_factors = (1+max([c.rating_factor_1 for c in all_cities]),
                      1+max([c.rating_factor_2 for c in all_cities]),
                      1+max([c.rating_factor_3 for c in all_cities]))
    cities = City.objects.all()
    resp = ""
    for c in cities:
        ratings = (c.rating_factor_1 / rating_factors[0],
                   c.rating_factor_2 / rating_factors[1], 
                   c.rating_factor_3 / rating_factors[2], 
                   )
        #01,02,10,12
        #combinations = [(0,1),(0,2),(1,0),(1,2)]
        avg  = (ratings[0]+ratings[1]+ratings[2])/decimal.Decimal("3")
        avg2 = (ratings[0]*ratings[0]+ratings[1]*ratings[1]+ratings[2]*ratings[2])/decimal.Decimal("3")
        stddev = decimal.Decimal(str(math.sqrt(avg2 - (avg*avg))))
        if (avg > decimal.Decimal("0")):
            stdvar = stddev/avg
    
            if stdvar > decimal.Decimal("1.41"):
                resp += "%d - %s [%f]\n" % (c.id,c.name,stdvar)
                
    return resp

def find_timezones(range=None):
    cities = City.objects.all()
    if (range is not None): cities=cities[range[0]:range[1]]
    resp = ""
    for c in cities:
        o = city_timezone(c.id)
        if(o is None):
            resp += "%d,127\n" % (c.id)
        else:
            c.timezone = int(o['offset'])
            c.save()
            resp += "%d,%s\n" % (c.id,o['offset'])

    return resp

def update_all_ratings(): 
    for c in City.objects.all(): c.refreshTotalRating()
                
    return "Okay"


def reslug_all_cities(range=None):
    resp = ""
    if range is not None:
        allcities = City.objects.all()[range[0]:range[1]]
    else:
        allcities = City.objects.all()
        
    for city in allcities:
        city.save()
        resp = resp + "%s (%s)\n" % (city.name, city.slug)
        
    return resp