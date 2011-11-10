# coding: latin1
import decimal
import os
import re
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from triplander.geoinfo import gmaplocal_coordinates, city_timezone, _wikipedia_article, wikipedia_ranking, panoramio_ranking, yahootravel_ranking
from triplander.models import City, Country
from triplander.functions import get_wikiname_by_url
from triplander.cache import autocomplete, blue_delete_all

def add_new_city(name, country):
    # we need a name and a country at first!
    std_error_obj = {'error': 2, 'city': None}
    if(country is None): return std_error_obj
    
    # by name
    coords = gmaplocal_coordinates(name,country.name)
    if(coords is None): return std_error_obj
    # let's see if this city already exists
    new_city = None
    try:
        new_city = City.objects.get(name__iexact=coords['city'])
        if(new_city is None): new_city = City.objects.get(local_name__iexact=coords['city'])
    except ObjectDoesNotExist:
        new_city = None
    
    if new_city is not None: return {'id': new_city.id, 'slug': new_city.slug, 'error': 1}
    
    new_city = City()
    new_city.name = coords['city']
    new_city.coordinates = Point((float(coords['latitude']),float(coords['longitude'])))
    new_city.latitude = Decimal(coords['latitude'])
    new_city.longitude = Decimal(coords['longitude'])
    new_city.country = country
    
    new_city.save()
    
    # now it has an ID
    new_city_id = new_city.id
    # take timezone info
    timezone = city_timezone(new_city_id)
    new_city.timezone = timezone['offset']
    # wikipedia tentative article name & rankings
    wname = _wikipedia_article(new_city_id)
    if (wname is not None): 
        new_city.wikiname = wname['wikiname']
    
    new_city.save()
    # rank, and it's done
    rank_city(new_city)
    
    return {'id': new_city_id, 'slug': new_city.slug, 'error': 0}

def rank_city(city,save=True):
    # here we are, the rankings
    if(city.wikiname is not None):
        r1 = (wikipedia_ranking(city.wikiname))
        r1 = r1['content']
    else:
        r1 = 0.0
        
    r2 = (panoramio_ranking(city.id))
    r3 = (yahootravel_ranking(city.id))

    city.setRating(r1,r2,r3)
    if(save): city.save()

def update_city(id,name,country,latitude,longitude,wikiname,localname=None,population=None,rerank=False):
    city = City.objects.get(pk=id)
    if(city is None): return
    old_name = city.name
    
    city.name        = name
    city.country     = country
    city.coordinates = Point(float(latitude),float(longitude))
    city.latitude    = Decimal(latitude)
    city.longitude   = Decimal(longitude)
    city.wikiname    = get_wikiname_by_url(wikiname)
    city.local_name  = localname
    city.population  = population
    
    city.save()

    # empty cache
    blue_delete_all(id)
    
    autocomplete.CityAutocompleter.reset_cache(name[0].lower())
    if(old_name[0].lower != name[0].lower()):
        autocomplete.CityAutocompleter.reset_cache(old_name[0].lower())   
    
    # reranking
    if(rerank): rank_city(city,save=True)