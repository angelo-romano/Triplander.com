from triplander.views import * # base class

# Search request - HTTP POST
@never_cache
def countrySearchPost(request):
    query = ''
    if ('query' in request.REQUEST): query=request.REQUEST['query']
    return httpRedirectCall(request,type='country',fullname=query)

# country not found - view
@cache_page(60*60*24*2) # 2 days caching (hardly changing)
@vary_on_cookie
def countryNotFound(request):
    return tl_response("www3/country_summary.html", {}, request.session)

# COUNTRY SUMMARY VIEW
@cache_page(60*60*24*5) # 5 days caching
@vary_on_cookie
def returnCountrySummary(request,country_id=None,country_slug=None):
    tl_message = []
    
    try:
        if(country_id is not None):
            cobj = Country.objects.get(id=country_id)
            if(country_slug is not None and cobj.slug != country_slug): cobj = None
        else:
            cobj = None
    except ObjectDoesNotExist:
        cobj = None

    if(cobj is None):
        return HttpResponseRedirect(reverse('country_notfound'))
    else:
        # no ambiguity from here
        if(cobj.local_name is not None and cobj.local_name != ''):
            tl_title = "%s (%s)" % (cobj.name, cobj.local_name)
        else:
            tl_title = cobj.name
        
        tl_googlemaps_active = False

        tl_country = {
                      'name'     : cobj.name.encode('utf-8'),
                      'localname': cobj.local_name.encode('utf-8'),
                      'id'       : cobj.id,
                      'icon'     : cobj.getFlagPath(),
                      'map'      : cobj.getMapPath(),
                      'currency' : cobj.currency,
                      'languages': ", ".join([l.name for l in cobj.languages.all()]),
                      'capital'  : { "id": cobj.capital_city.id,
                                     "name": cobj.capital_city.getFullName(),
                                     "slug": cobj.capital_city.slug }
                      }

        top_cities = City.objects.filter(country=cobj).order_by('-total_rating')[:5]
        tl_top_cities = []
        
        for c in top_cities:
            this_item = { 
                         "id": c.id, 
                         "fullname": c.getFullName(), 
                         "rating": c.getRating(), 
                         "rating_img": c.getRatingIcon(), 
                         "slug": c.slug 
                         }
            tl_top_cities.append(this_item)

    return tl_response("www3/country_summary.html", locals(), request.session)
