from triplander.views import * # base class

# Create your views here.
@cache_page(60*60*24*2) # 2 days caching (hardly changing)
@vary_on_cookie
def callMain(request):
    tl_googlemaps_active = True
    map_center = (-1.933594,55.849006) # Angelo's choice
    markers    = []
    cities     = callAssociateFunction('getRandomCities', {'dfrom': 50})
        
    tl_googlemaps = GoogleMapSet(GoogleMap(center=map_center,zoom=3,markers=markers))

    tl_info = {
               'num_cities'   : City.objects.count(),
               'num_countries': Country.objects.count(),
               }

    return tl_response("www3/index2.html", locals(), request.session)

def callRemoteFunction_Adapter(request,dfrom,type):
    params = {
              "dfrom": dfrom,
              "http" : True
              }
    return callAssociateFunction(type,params)
    #return None

@cache_page(60*60*24*2) # 2 days of caching (static data) 
def staticRender(request,path,js=False):
    if(js): local_path = "www3/js/%s" % path
    else  : local_path = "www3/%s" % path
    resp = None
    
    try:
        resp = tl_response(local_path, locals(), request.session)
    except TemplateDoesNotExist:
        resp = HttpResponseNotFound("Static module/template '%s' not found" % path)
    
    return resp

# blue processing -> JSON / web service calls
def blueProcess(o,json=False, debug=False):
    mimetype = 'text/plain'
    if (json and not debug): mimetype = 'application/json'
    
    if (o is None): return HttpResponseNotFound("None")
    if (json): o = simplejson.dumps(o)
    return HttpResponse(o,mimetype=mimetype)

def httpRedirectCall(request, type, slug=None, fullname=None):
    type_set = {'city'   : ('city_by_id',    'city_notfound',    City),
                'country': ('country_by_id', 'country_notfound', Country), 
                }
    # only valid content
    if not type_set.has_key(type): return HttpResponseNotFound("Invalid redirect call")
    # retrieve redirect URL
    type_urlname_found    = type_set[type][0]
    type_urlname_notfound = type_set[type][1]
    type_class            = type_set[type][2]
    type_id               = 0
    type_slug             = 'not-found'
    entries               = None
    if(slug is not None):
        entries           = type_class.objects.filter(slug=slug)
    elif(fullname is not None):
        entries           = type_class.objects.filter(slug=slugify(fullname))

    if(entries is not None and len(entries) > 0):
        # more than one entry with same slug - disambiguate!
        if(type == 'city' and len(entries) > 1): return returnCityDisambig(request,entries)
        
        # just one entry from here
        entries   = entries[0] 
        type_id   = entries.id
        type_slug = entries.slug
    
        new_url = reverse(type_urlname_found,args=[type_id,type_slug])
        # these redirects are PERMANENT
        return HttpResponsePermanentRedirect(new_url)
    else:
        new_url = reverse(type_urlname_notfound)
        # these redirect are NOT PERMANENT (what if I create a city with that slug?!?)
        return HttpResponseRedirect(new_url)

# serializer for "blue" calls - it also uses caching (default 5 mins)
def httpSerialize(request, param, method, 
                  json=False, xml=False, debug=False, 
                  more=None, cache_timeout=(60*5)):
    
    from triplander.cache import blue_get, blue_set
    if ('_debug' in request.REQUEST and request.REQUEST['_debug'] == '1'):
        cache_timeout = 0
        debug = True
    
    resp = None
    
    if(cache_timeout > 0): # caching enabled
        resp = blue_get(request.path)
        #resp['cached'] = 1
        
    if resp is None:
        if more is not None:
            resp = method(param,more=more)
        else:
            resp = method(param)

    blue_set(request.path,resp,cache_timeout)
    return blueProcess(resp,debug=debug,json=json)

# autocompleter view - returns JSON formatted content
def jsonAutocompleteFilter(request, type):
    from triplander.cache import autocomplete
    if ('q' in request.REQUEST):
        word = request.REQUEST['q'].lower()
        
        # autocomplete results are cached using a suffix tree structure!
        ac_manager = None
        if (type == 'city'):
            ac_manager = autocomplete.CityAutocompleter.get_tree_part(word[0])        
            resp = ac_manager.get_cities(word)
        elif (type == 'country'):
            ac_manager = autocomplete.CountryAutocompleter.get_tree_part(word[0])        
            resp = ac_manager.get_countries(word)

        # getting json-formatted information
        json_data = simplejson.dumps(resp)
                
    else:
        json_data = simplejson.dumps([])
    
    if('_debug' in request.REQUEST and request.REQUEST['_debug'] == '1'):
        mime_type = 'text/plain' #only for debug purposes
    else:
        mime_type = 'application/json'
    
    return HttpResponse(content=json_data, mimetype=mime_type, status=200)

def createRedirects(request):
    cities = City.objects.all()
    
    for c in cities:
        dabs = dab_string(c.name)
        if(c.local_name is not None):
            if dabs is None:
                dabs = dab_string(c.local_name)
            else:
                dabs2 = dab_string(c.local_name)
                if dabs2 is not None:
                    dabs = dabs + dabs2
                    dabs2 = []
            
        if dabs is not None:
            for d in dabs:
                cityDab = CityRedirect(name=d,city=c)
                cityDab.save()
    
    tl_message = []
    
    return tl_response("www3/info.html", locals(), request.session)

# user login & logout functions
@never_cache
def userLogin(request):
    error = {
             'MISSING_FIELDS': 2,
             'INVALID_USERNAME': 3,
             'INVALID_PASSWORD': 3,
             'COOKIES_DISABLED': 4,
             }

    if('username' not in request.REQUEST or 
       'password' not in request.REQUEST):
        return blueProcess({'error': error['MISSING_FIELDS']},json=True)

    try:
        user = ApplicationUser.objects.get(username=request.REQUEST['username'])
    except ObjectDoesNotExist:
        return blueProcess({'error': error['INVALID_USERNAME']},json=True)
    
    if(not user.matchPassword(request.REQUEST['password'])):
        return blueProcess({'error': error['INVALID_PASSWORD']},json=True)
 
    request.session['user_id']   = user.id
    request.session['user_name'] = user.username
    
    # login information updated
    user.last_login = datetime.now()
    user.save()
    
    return blueProcess({'error': 0},json=True)

@never_cache
def userLogout(request):
    #logout - end session
    if (request.session.get('user_id') is not None)  : del request.session['user_id']
    if (request.session.get('user_name') is not None): del request.session['user_name']
    
    return blueProcess({'error': 0},json=True)