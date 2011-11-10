import re
from datetime import datetime
from django.conf import settings

from triplander.models import UserActivity

class Activity(object):
	def process_request(self,request):
		if self.is_blue(request):
			self.activity = None
			return
		
		if request.META.has_key('HTTP_REFERER'):
			referer = request.META['HTTP_REFERER']
		else:
			referer = ''

		self.activity = UserActivity(
			#user = request.user,
			#session = request.session,
			date = datetime.now(),
			request_url = request.META['PATH_INFO'],
			referer_url = referer,
			client_address = request.META['REMOTE_ADDR'],
			client_host = request.META['REMOTE_HOST'],	
			browser_info = request.META['HTTP_USER_AGENT']
		)
				
	def process_exception(self,request,exception):
		#if self.is_blue(request): return
		if(self.activity is not None):
			self.activity.error = exception
			self.activity.save()

	def process_response(self,request,response):
		#if self.is_blue(request): return
		
		if self.activity is not None and response.status_code == 200:
			self.activity.set_request_time()
		
		return response

	def is_blue(self,request):
		ignore_pattern = '^\/(?:blue|admin|racina|js|static)'
		
		if re.match(ignore_pattern,request.META['PATH_INFO']): return True
		return False
