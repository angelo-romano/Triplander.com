from triplander.models import *
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.conf.urls.defaults import *
from django.contrib.admin.sites import AdminSite

class MyAdminSite(AdminSite):
	def get_urls(self):
		urls = super(MyAdminSite, self).get_urls()
		my_urls = patterns('',
			(r'^what/$', self.admin_view(self.this_view))
		)
		return my_urls+urls

	def this_view(self, request):
		from triplander.cache import autocomplete, blue_delete_all
    		autocomplete.CityAutocompleter.reset_cache()
		autocomplete.CountryAutocompleter.reset_cache()
		return HttpResponse('Done.')
		

admin_site = MyAdminSite()

admin_site.register(City)
admin_site.register(CityRedirect)
admin_site.register(Country)
admin_site.register(Region)
admin_site.register(ApplicationUser)
admin_site.register(UserActivity)

