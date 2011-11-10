from triplander.views import * # base class

# Search request - HTTP POST
@never_cache
def citySearchPost(request):
    query = ''
    if ('query' in request.REQUEST): query=request.REQUEST['query']
    return httpRedirectCall(request,type='city',fullname=query)

# city disambiguation view
@cache_page(60*30) # 30 min caching (hardly changing)
@vary_on_cookie
def returnCityDisambig(request,cities):
    #cities = getCityObject(slug=city_slug)
    #if(type(cities).__name__ != 'City'): 
    
    #multiple cities - ambiguity!
    
    tl_title = cities[0].name.capitalize()
    tl_possible_cities = []
    for c in cities:
        if(c.local_name is not None and c.local_name != ''):
            city_fullname = "%s (%s)" % (c.name, c.local_name)
        else:
            city_fullname = c.name
            
        newobj = {
                  "country"    : c.country.name,
                  "countryflag": c.country.getFlagPath(),
                  "fullname"   : city_fullname,
                  "id"         : c.id,
                  "slug"       : c.slug,
                  }
        
        tl_possible_cities.append(newobj)
    
    return tl_response("www3/city_ambiguity.html", locals(), request.session)

# city not found - view
@cache_page(60*60*24*2) # 2 days caching (hardly changing)
@vary_on_cookie
def cityNotFound(request):
    return tl_response("www3/city_summary.html", {}, request.session)

# CITY SUMMARY VIEW
# city not found - view
@vary_on_cookie
def returnCitySummary(request,city_id=None,city_slug=None):
    city_name_verified = None
    tl_message = []
    
    # retrieve city
    if(city_id is not None):
        cobj = getCityObject(id=city_id)
        if(cobj is not None and 
           city_slug is not None and 
           city_slug != cobj.slug): cobj = None
    else:
        cobj = None
    
    if(cobj is None): # not found
        return HttpResponseRedirect(reverse('city_notfound'))
    else:
        tl_city_localname = None
        
        if(cobj.local_name is not None and cobj.local_name != ''): # local name found
            tl_city_localname = cobj.local_name
            tl_title = "%s (%s)" % (cobj.name, cobj.local_name)
        else:
            tl_title = cobj.name
               
        # google map generation
        tl_googlemaps_active = True
        tl_googlemaps_set    = [
                                           GoogleMap(
                                                     center=(cobj.coordinates.y, cobj.coordinates.x),
                                                     zoom=7,
                                                     markers=[GMarker(
                                                                      geom =(cobj.coordinates.y,cobj.coordinates.x),
                                                                      title=tl_title
                                                                      )
                                                     ])
                                ]
        if(tl_logged_user(request.session) is not None):
            tl_googlemaps_set.append(
                                               GoogleMap(
                                                         center=(cobj.coordinates.y, cobj.coordinates.x),
                                                         zoom=12,
                                                         markers=[GMarker(
                                                                          geom =(cobj.coordinates.y,cobj.coordinates.x),
                                                                          title='Current coordinates',
                                                                          )
                                                         ]
                                                        )
                                    )
            
        tl_googlemaps = GoogleMapSet(tl_googlemaps_set)

        tl_city = {
                   'name'        : cobj.name,
                   'id'          : cobj.id,
                   'slug'        : cobj.slug,
                   'icon'        : cobj.country.getFlagPath(),
                   'timezone'    : cobj.getFormattedTimeZone(),
                   'localname'   : cobj.local_name or '',
                   'population'  : cobj.population,
                   'wikiname'    : cobj.wikiname,
                   'coordinates' : {'x': cobj.coordinates.x, 'y': cobj.coordinates.y},
                   }
        
        tl_cityname_encoded = urllib.quote(cobj.name.encode('utf8'))
        tl_city_timezone = ''
        tl_city_country = {'name': cobj.country.name, 'id': cobj.country.id, 'slug': cobj.country.slug }
        
        tl_rating_val     = cobj.getRating()
        tl_rating_imgfile = cobj.getRatingIcon()
        
        # retrieve them directly
        nearby_cities = callAssociateFunction('getClosestCities', {'dfrom': cobj.id, 'more': { 'distance': 60, 'limit': 5, 'randomize': True, 'usecache': True}})
        tl_nearbycities = []
        
        if (nearby_cities is not None and nearby_cities['nearby_cities'] is not None):            
            for n in nearby_cities['nearby_cities']:
                this_entry = {"name": n['name'], "fullname": n['name'], "id": n['id'], "slug": n['slug']}
                if (n.has_key('local_name')): 
                    this_entry['fullname'] = "%s (%s)" % (n['name'], n['local_name'])
                this_entry['fullname'] = this_entry['fullname'] + " [%d km]" % (math.floor(n['distance'])) 
                tl_nearbycities.append(this_entry)

    return tl_response("www3/city_summary.html", locals(), request.session)


def returnNearbyAirports_ForCity(request,city_id=None,city_slug=None): 
    city_name_verified = None
    tl_airports = None
    tl_city     = None
    
    if(city_id is not None):
        cobj = getCityObject(id=city_id)
        if(cobj is not None and 
           city_slug is not None and 
           city_slug != cobj.slug): cobj = None

    elif(city_slug is not None):
        cobj = getCityObject(slug__iexact=city_slug)
    else:
        cobj = None
        
    if cobj is None: 
        json_resp = None 
    else:
        json_resp = callAssociateFunction('getClosestAirports', {'dfrom': cobj.id})
        
    if(json_resp is None): 
        pass
    else:
        #tl_title = "Airports nearby %s" % (json_resp['city']['name'])
        tl_city     = json_resp ['city']
        tl_airports = []
        map_center  = (tl_city['y'],tl_city['x'])
        
        markers = []
        tl_googlemaps_active = True
        for r in json_resp['airports']:
            airport = Station.objects.get(code_alt=r['code'])
            entry = {
                "name"     : airport.name,
                "code"     : airport.code_alt, 
                "city"     : airport.city.name,
                "country"  : airport.city.country.name,
                "distance" : math.floor(r['distance']*(1000))/1000,
                "x"        : airport.coordinates.x,
                "y"        : airport.coordinates.y,
                "img"      : airport.city.country.getFlagPath(),
            }
            
            tl_airports.append(entry)
            airplane_icon = GIcon('airplane_icon',
                                  image='/static/images/marker_aeroplane.png',
                                  iconsize=(32,32))
            markers.append(GMarker(geom=(airport.coordinates.y,airport.coordinates.x),title=entry["name"],
                                   icon=airplane_icon))

        markers.append(GMarker(geom=map_center,title=string.upper(tl_city['name'])))
        
        tl_googlemaps = GoogleMapSet(GoogleMap(center=map_center,zoom=10,markers=markers))
        
    return tl_response("www3/city_airports.html", locals(), request.session)

# Add new city
@never_cache
def cityAdd(request):
    # possible errors
    error = {
             'NO_PARAMS': 2,
             'COUNTRY_NOT_FOUND': 2,
             'CITY_EXISTS': 0,
             'UNEXPECTED_ERROR': 2,
             'OPERATION_NOT_PERMITTED': 1,
             }

    # logged user info
    user = tl_logged_user(request.session)
    if(user is None):
        return blueProcess({'error': error['OPERATION_NOT_PERMITTED']},json=True)    

    # mandatory fields
    if ('name' not in request.REQUEST or 'country' not in request.REQUEST):
        return blueProcess({'error': error['NO_PARAMS']},json=True)
    
    # request fields
    city_name    = request.REQUEST['name']
    country_name = request.REQUEST['country']
    city    = None
    country = None
    
    try:
        country = Country.objects.get(name__iexact=country_name) # search for country
        if(country is None): country = Country.objects.get(local_name__iexact=country_name)
    except ObjectDoesNotExist:
        country = None
        
    if(country is None): return blueProcess({'error': error['COUNTRY_NOT_FOUND']},json=True,debug=True)

    # let's see if the city already exists
    try:
        city = City.objects.get(name__iexact=city_name)
        if(city is None): city = City.objects.get(local_name__iexact=city_name)
    except ObjectDoesNotExist:
        city = None
        
    # city already existing
    if(city is not None): return blueProcess({'error': error['CITY_EXISTS'], 
                                              'id'   : city.id,
                                              'url'  : reverse('city_by_id',args=[city.id,city.slug])},
                                              json=True)

    # add new city
    resp = add_new_city(city_name, country)
    
    # does city already exist?
    if(resp['error']==1): return blueProcess({'error': error['CITY_EXISTS'], 
                                              'id'   : resp['id'],
                                              'url'  : reverse('city_by_id',args=[resp['id'],resp['slug']])},
                                              json=True)
    # unexpected error?
    if(resp['error']==2): return blueProcess({'error': error['UNEXPECTED_ERROR']},json=True)

    # add entry into ApplicationUserHistory
    city = City.objects.get(id=resp['id'])

    user_history           = ApplicationUserHistory()
    user_history.user      = user
    user_history.operation = ApplicationUserHistory.USER_OP_ADDCITY
    user_history.setChangelog({
                                'query_city_name'   : city_name,
                                'query_country_name': country_name,
                                'country_name'      : country.name,
                                'city_id'           : resp['id'],
                                'city_name'         : city.name,
                                'city_wikiname'     : city.wikiname,
    })
    user_history.save()

    return blueProcess({'error': 0, 
                        'id'   : resp['id'],
                        'url'  : reverse('city_by_id',args=[resp['id'],resp['slug']])},
                        json=True)

# Edit existing city
@never_cache
def cityEdit(request):
    error = {
             'NO_PARAMS': 2,
             'COUNTRY_NOT_FOUND': 3,
             'UNEXPECTED_ERROR': 4,
             'INVALID_FIELD_VALUES': 5,
             'OPERATION_NOT_PERMITTED': 1,
             }
    
    user = tl_logged_user(request.session)
    if(user is None):
        return blueProcess({'error': error['OPERATION_NOT_PERMITTED']},json=True)    

    # mandatory fields
    if ('id' not in request.REQUEST or 
        'name' not in request.REQUEST or
        'country' not in request.REQUEST or
        'x' not in request.REQUEST or
        'y' not in request.REQUEST):
        return blueProcess({'error': error['NO_PARAMS']},json=True)
    
    city_vals = {
               'name'      : request.REQUEST['name'],
               'country'   : request.REQUEST['country'],
               'id'        : request.REQUEST['id'],
               'x'         : request.REQUEST['x'],
               'y'         : request.REQUEST['y'],
               'localname' : request.REQUEST['localname'] or '',
               'population': request.REQUEST['population'] or 0,
               'wikiname'  : get_wikiname_by_url(request.REQUEST['wikiname']),
               'rerank'    : (request.REQUEST['rerank'] == '1')
               }
        
    country = None
    
    if(city_vals['wikiname'] is None): return blueProcess({'error': error['INVALID_FIELD_VALUES']},json=True)

    try:
        country = Country.objects.get(name__iexact=city_vals['country'])
        if(country is None): country = Country.objects.get(local_name__iexact=country_name)
    except ObjectDoesNotExist:
        country = None
        
    if(country is None): return blueProcess({'error': error['COUNTRY_NOT_FOUND']},json=True)

    # let's take the city entry - and update it
    update_city(city_vals['id'],name=city_vals['name'],country=country,
                latitude=city_vals['x'],
                longitude=city_vals['y'],
                wikiname=city_vals['wikiname'],
                localname=city_vals['localname'],
                population=city_vals['population'],
                rerank=city_vals['rerank']
                )

    # add entry into ApplicationUserHistory
    user_history           = ApplicationUserHistory()
    user_history.user      = user
    user_history.operation = ApplicationUserHistory.USER_OP_ADDCITY
    user_history.setChangelog({
                                'city_id'           : city_vals['id'],
                                'city_name'         : city_vals['name'],
                                'city_latitude'     : city_vals['x'],
                                'city_longitude'    : city_vals['y'],
                                'city_wikiname'     : city_vals['wikiname'],
                                'city_localname'    : city_vals['localname'],
                                'city_population'   : city_vals['population'],
    })
    user_history.save()

    return blueProcess({'error': 0, 
                        'id': city_vals['id'], 
                        'url': reverse('city_by_id',args=[city_vals['id'],slugify(city_vals['name'])])
                        },json=True)
