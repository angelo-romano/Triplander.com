from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D # `D` is a shortcut for `Distance`
from triplander.views import * 
from triplander.models import *
from triplander.remote import *
from triplander.cron import *
from triplander.geoinfo import *
from triplander.admin import admin_site

#admin.autodiscover()

# url_patterns
notfound_slug = '0-not-found'
urlpatterns = patterns('',
    # Example:
    url(r'^racina/', include(admin_site.urls), name='admin'),
    url(r'^/?$', callMain, name='site_home'),
    url(r'^site/about/?$', staticRender, {'js': False, 'path': 'site_about.html'}, name='site_about'),
    url(r'^site/contact/?$', staticRender, {'js': False, 'path': 'site_contact.html'}, name='site_contact'),
    url(r'^city/do/?', citySearchPost, name='city_searchpost'),
    url(r'^city/%s/?$' % notfound_slug, cityNotFound, name='city_notfound'),
    url(r'^city/(?P<city_id>\d+)(?:-(?P<city_slug>[a-z\-]+))?/?$', returnCitySummary, name='city_by_id'),
    url(r'^city/(?P<fullname>.+)/?$', httpRedirectCall, {'type': 'city'}, name='city_by_name'),
    url(r'^city:airports/(?P<city_id>\d+)(?:-(?P<city_slug>[a-z\-]+))?$', returnNearbyAirports_ForCity, name='city_airports'),
    url(r'^country/do/?', countrySearchPost, name='country_searchpost'),
    url(r'^country/%s/?$' % notfound_slug, countryNotFound, name='country_notfound'),
    url(r'^country/(?P<country_id>\d+)(?:-(?P<country_slug>[a-z\-]+))?/?$', returnCountrySummary, name='country_by_id'),
    url(r'^country/(?P<fullname>.+)/?$', httpRedirectCall, {'type': 'country'}, name='country_by_name'),
    url(r'^blue/city/delicious/(?P<param>\d+)$', httpSerialize, {'method': delicious_popular }, name='blue_delicious'),
    url(r'^blue/city/panoramio/(?P<param>\d+)$', httpSerialize, {'method': panoramio_set, 'json': True }, name='blue_panoramio'),
    url(r'^blue/city/weather/(?P<param>\d+)$', httpSerialize, {'method': weather_conditions, 'json': True, 'cache_timeout': 0 }, name='blue_weather'),
    url(r'^blue/city/wikipedia/(?P<param>\d+)$', httpSerialize, {'method': wikipedia_snippet, 'json': True, 'more': 'City' }, name='blue_wikipedia_city'),
    url(r'^blue/city/wikirank/(?P<param>\d+)$', httpSerialize, {'method': wikipedia_ranking, 'json': True, 'cache_timeout': 0 }, name='blue_wikipedia_rank'),
    url(r'^blue/city/panorank/(?P<param>\d+)$', httpSerialize, {'method': panoramio_ranking, 'json': True, 'cache_timeout': 0 }, name='blue_panoramio_rank'),
    url(r'^blue/city/ytrank/(?P<param>\d+)$', httpSerialize, {'method': yahootravel_ranking, 'json': True, 'cache_timeout': 0 }, name='blue_yahootravel_rank'),
    url(r'^blue/city/popularset/(?P<param>[\d,;\.\-+]+)$', httpSerialize, {'method': popular_city_selection, 'json': True, 'cache_timeout': 0 }, name='blue_popular_cities'),
    url(r'^blue/city/timezone/(?P<param>\d+)$', httpSerialize, {'method': city_timezone, 'json': True, 'debug': True, 'cache_timeout': 0  }, name='blue_city_timezone'),
    url(r'^blue/country/wikipedia/(?P<param>\d+)$', httpSerialize, {'method': wikipedia_snippet, 'json': True, 'more': 'Country' }, name='blue_wikipedia_country'),
    url(r'^blue/autocomplete/city/?$', jsonAutocompleteFilter,{'type': 'city'}, name='blue_autocomplete_city'),
    url(r'^blue/autocomplete/country/?$', jsonAutocompleteFilter,{'type': 'country'}, name='blue_autocomplete_country'),
    #url(r'^blue/country/commons/(?P<param>.+)$', httpSerialize, {'method': commons_image, 'json': True }),
    url(r'^blue/city/add/?$', cityAdd, name='blue_city_add'),
    url(r'^blue/city/edit/?$', cityEdit, name='blue_city_edit'),
    url(r'^blue/user/login/?$', userLogin, name='blue_user_login'),
    url(r'^blue/user/logout/?$', userLogout, name='blue_user_logout'),
    url(r'^blue/city/popularset/$', callMain, name='BASE_blue_popular_cities'),
    url(r'^js/(?P<path>.*\.js)$', staticRender, {'js': True}, name='js_script'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

