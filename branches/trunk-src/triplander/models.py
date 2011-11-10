# -*- coding: utf-8 -*-
#from django.db import models
import re
import decimal
import hashlib

from math import log
from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.template.defaultfilters import slugify

from triplander.functions import dec_log

class PasswordField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(models.CharField, self).__init__(*args, **kwargs)

    def pre_save(self,model_instance,add):
        value = super(models.CharField, self).pre_save(model_instance,add)
        myre  = re.compile("^md5\[(.+)\]$")
        if(add):
            return self.getEncodedPassword(value)
        else:
            if (myre.match(value)):
                return value
            else:
                return self.getEncodedPassword(value)
            pass
            
    # set password - use this!
    def getEncodedPassword(self,pwd):
        md5 = hashlib.md5()
        md5.update(pwd)
        return "md5[%s]" % md5.hexdigest()

# Language
class Language(models.Model):
    name = models.CharField(max_length=64,unique=True)
    local_name = models.CharField(max_length=64,null=True,blank=True)
    def __unicode__(self):
        if(self.local_name == ""):
            return self.name
        else:
            return self.name+" ("+self.local_name+")"
    class Meta:
        ordering = ["name"]
    class Admin:
        pass

# Country
class Country(models.Model):
    name = models.CharField(max_length=64,unique=True)
    local_name = models.CharField(max_length=64,null=True,blank=True)
    slug = models.SlugField()
    languages = models.ManyToManyField(Language)
    currency = models.CharField(max_length=32,null=True,blank=True)
    code = models.CharField(max_length=3,null=True,blank=True)
    wikiname = models.CharField(max_length=64,null=True,blank=True)
    #map = models.CharField(max_length=64,null=True,blank=True)
    capital_city = models.ForeignKey('triplander.City',related_name='city')

    # map path associated to country
    def getMapPath(self):
        return "/static/images/country_maps/%s_map.png" % (self.code.lower())
    
    # flag path associated to country
    def getFlagPath(self):
        return "/static/images/flags/mini/country_%s.png" % (self.code.lower())
    
    # SEO field values must be generated automatically
    def save(self):
        self.slug = slugify(self.name)
        super(Country,self).save()
    
    # unicode val
    def __unicode__(self):
        if(self.local_name == ""):            
            return self.name
        else:
            return self.name+" ("+self.local_name+")"
    class Meta:
        ordering = ["name"]
    class Admin:
        pass

# Region
class Region(models.Model):
    name = models.CharField(max_length=64)
    local_name = models.CharField(max_length=64,null=True,blank=True)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name+", "+self.country.name
    class Meta:
        ordering = ["name"]
    class Admin:
        pass

# City
class City(models.Model):
    name = models.CharField(max_length=64)
    local_name = models.CharField(max_length=64,null=True,blank=True)
    slug = models.SlugField()
    country = models.ForeignKey(Country)
    region = models.ForeignKey(Region,null=True,blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5,default=0)
    longitude = models.DecimalField(max_digits=8, decimal_places=5,default=0)
    population = models.DecimalField(max_digits=8, decimal_places=0,default=0)
    rating_factor_1 = models.DecimalField(max_digits=14, decimal_places=8,default=0)
    rating_factor_2 = models.DecimalField(max_digits=14, decimal_places=8,default=0)
    rating_factor_3 = models.DecimalField(max_digits=14, decimal_places=8,default=0)
    total_rating = models.DecimalField(max_digits=14, decimal_places=8,default=0)
    wikiname = models.CharField(max_length=64,null=True,blank=True)
    coordinates = models.PointField()
    timezone = models.IntegerField(default=0)
    recompute = models.BooleanField(default=False)
    
    objects = models.GeoManager()
    
    # unicode val
    def __unicode__(self):
        return self.name+", "+self.country.name

    # get full name - whatever it means
    def getFullName(self):
        if (self.local_name is not None and self.local_name != ''): 
            return "%s (%s)" % (self.name, self.local_name)

        return self.name

    # refresh current rating value
    def refreshTotalRating(self):
        self.total_rating = self.getRating(round=False)
        self.save()

    # sets rating
    def setRating(self,factor1,factor2,factor3):
        self.rating_factor_1 = decimal.Decimal(factor1)
        self.rating_factor_2 = decimal.Decimal(factor2)
        self.rating_factor_3 = decimal.Decimal(factor3)
        self.total_rating = self.getRating(round=False)

    # get total rating
    def getRating(self,round=True,divide=10):
        #0.5+4.5*LOG(1+0.75*rating_factor_1/470+0.25*rating_factor_2/22000)/0.28
        a1 = decimal.Decimal("0.30")/dec_log(decimal.Decimal("470"))
        a2 = decimal.Decimal("0.20")/dec_log(decimal.Decimal("22050"))
        a3 = decimal.Decimal("0.50")/dec_log(decimal.Decimal("13070"))
        #decimal.Decimal("2.1").
        #0.5 + 4.5*(LOG(1+0.22*rating_factor_1/470+0.13*rating_factor_2/22050+0.65*rating_factor_2/13070)/LOG(10))/0.29
        #(LOG(1+0.35*LOG(1+rating_factor_1)/LOG(470)+0.15*LOG(1+rating_factor_2)/LOG(22050)+0.50*LOG(rating_factor_3+1)/LOG(13070))/LOG(10))
        rank = log(decimal.Decimal(1+a1*dec_log(1+self.rating_factor_1)
                                   +a2*dec_log(1+self.rating_factor_2)
                                   +a3*dec_log(1+self.rating_factor_3)),10)
        
        rank = decimal.Decimal("0.5") + decimal.Decimal("4.5")*decimal.Decimal(str(rank))/decimal.Decimal("0.30")
        #rank = 0.5+4.5*math/4.23

    	if(round):
    
    		rsets = [(50, decimal.Decimal("4.75")),
    		         (45, decimal.Decimal("4.25")),
    		         (40, decimal.Decimal("3.75")),
    		         (35, decimal.Decimal("3.25")),
    		         (30, decimal.Decimal("2.75")),
    		         (25, decimal.Decimal("2.25")),
    		         (20, decimal.Decimal("1.75")),
    		         (15, decimal.Decimal("1.25")),
    		         (10, decimal.Decimal("0.75")),
    		         (5, decimal.Decimal("-0.1")),
    		         ]
    		
    		for (r_ret,r_limit) in rsets:
    		    if (rank > r_limit): return r_ret / divide
    
    		return 0
    	else:
    		return rank

    # return corresponding rating icon
    def getRatingIcon(self):
        rating_corresps = {
                            "50": "50_2.png",
                            "45": "45_2.png",
                            "40": "40_2.png",
                            "35": "35_2.png",
                            "30": "30_2.png",
                            "25": "25_2.png",
                            "20": "20_2.png",
                            "15": "15_2.png",
                            "10": "10_2.png",
                             "5": "05_2.png",
                            }
        this_rating_val = self.getRating(divide=1)
        return rating_corresps[str(this_rating_val)]

    # return timezone in a properly formatted value
    def getFormattedTimeZone(self):
        if(self.timezone < 0):
            return "UTC%d" % (self.timezone)
        elif(self.timezone == 0):
            return "UTC+0 (GMT)"
        else:
            return "UTC+%d" % (self.timezone)
    
    # SEO field values must be generated automatically
    def save(self):
        self.slug = slugify(self.name)
        super(City,self).save()
        
    class Meta:
        ordering = ["name"]
    class Admin:
        search_fields = ('name',)

# City redirect (e.g. alternative names)
class CityRedirect(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(City)
    def __unicode__(self):
        return self.name+"-> "+self.city.name
    class Meta:
        ordering = ["name"]
    class Admin:
        pass

# Bag of Words
class BagOfWords(models.Model):
    TERM_TYPE = (
         (0, 'Base'),
         (1, 'Occasional'),
         (2, 'Very Frequent'),
         (3, 'Other')
    )
    
    tag = models.CharField(max_length=20)
    type = models.IntegerField(choices=TERM_TYPE,default=0)
    rank = models.DecimalField(max_digits=10, decimal_places=6,default=0)
    frequency = models.IntegerField(null=True,blank=True,default=0)

# User
class ApplicationUser(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username = models.CharField(max_length=20,unique=True)
    password = PasswordField(max_length=64)
    first_name = models.CharField(max_length=32,null=True,blank=True) 
    last_name = models.CharField(max_length=32,null=True,blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES) 
    country = models.ForeignKey(Country,null=True,blank=True)
    city = models.ForeignKey(City,null=True,blank=True)
    registration_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True,blank=True)

    def matchPassword(self,pwd,md5encoded=True):
        real_pwd = pwd
        if(not md5encoded):
            md5 = hashlib.md5()
            md5.update(pwd)
            real_pwd = md5.hexdigest()
        
        real_pwd = "md5[%s]" % real_pwd
        
        return (self.password == real_pwd)
    
    def __unicode__(self):
        return "%s" % (self.username)
    
    class Meta:
        ordering = ["username"]
    class Admin:
        pass

# User history
class ApplicationUserHistory(models.Model):
    USER_OP_TYPE = (
        (1, 'add_city'),
        (2, 'edit_city'),
    )
    USER_OP_ADDCITY  = 1
    USER_OP_EDITCITY = 2
    user = models.ForeignKey(ApplicationUser)
    operation = models.IntegerField(choices=USER_OP_TYPE)
    changelog = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def setChangelog(self,params):
        # params is a dictionary {k: v, ...}
        s = ""
        for key, val in params.iteritems():
            if(s == ""):
                s = u"[%s=%s]" % (key, unicode(val))
            else:
                s = s + u";[%s=%s]" % (key, unicode(val))
        
        self.changelog = s
    
    def getChangelog(self):
        params = {}
        fields  = "".split(";")
        this_re = re.compile("^\[([^=]+)=(.+)\]$")
        for f in fields:
            re_result = this_re.match(f)
            if (re_result): params[re_result.group(1)] = re_result.group(2)
        
        return params
    
#Ranking changes
class RankingVariation(models.Model):
    city = models.ForeignKey(City)
    old_ranking = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    new_ranking = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    week_id = models.IntegerField()
    
# Station
class Station(models.Model):
    CONN_TYPE = (
        (1, 'Commercial'),
        (2, 'Commercial/Minor-LowCost'),
        (3, 'Military'),
        (4, 'Inactive'),
        (127, 'Other')
                 )
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=32)
    city = models.ForeignKey(City)
    latitude = models.DecimalField(max_digits=8, decimal_places=5,null=True,blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5,null=True,blank=True)
    code = models.CharField(max_length=7,null=True,blank=True)
    code_alt = models.CharField(max_length=7,null=True,blank=True)
    type = models.IntegerField(choices=CONN_TYPE)
    website = models.URLField(null=True,blank=True)
    coordinates = models.PointField()
    rank = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    wikiname = models.CharField(max_length=64,null=True,blank=True)
    
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name+" ("+self.short_name+";"+self.code_alt+")"
    class Meta:
        ordering = ["short_name"]
    class Admin:
        pass
# Connection provider (e.g., flight companies)
class ConnectionProvider(models.Model):
    CONN_TYPE = (
        (1, 'Train'),
        (2, 'Generic Airline'),
        (3, 'Bus'),
        (4, 'Boat/Ship'),
        (5, 'Low-cost Airline'),
        (6, 'Charter Airline'),
        (127, 'Other'),
                 )
    name = models.CharField(max_length=32)
    name_short = models.CharField(max_length=16,null=True,blank=True)
    name_full = models.CharField(max_length=64,null=True,blank=True)
    country = models.ForeignKey(Country,null=True,blank=True)
    website = models.URLField(null=True,blank=True)
    type = models.IntegerField(choices=CONN_TYPE)
    code = models.CharField(max_length=5)
    code_alt = models.CharField(max_length=5,null=True,blank=True)

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.code)
    
    class Meta:
        ordering = ["name"]
    class Admin:
        pass

# Connection website (recognition)
class ConnectionWebsite(models.Model):
    METHOD_TYPE = ( (1, 'GET'), (2, 'POST') )
    provider = models.ForeignKey(ConnectionProvider)
    url = models.URLField()
    method = models.IntegerField(choices=METHOD_TYPE,default=2)
    payload = models.CharField(max_length=2048)
    regexp = models.CharField(max_length=2048)
    class Admin:
        pass
    
# Connection between two stations
class Connection(models.Model):
    departure = models.ForeignKey(Station,related_name="departureStation")
    arrival = models.ForeignKey(Station,related_name="arrivalStation")
    provider = models.ForeignKey(ConnectionProvider)
    #type = models.IntegerField(choices=CONN_TYPE,null=True,blank=True)
    est_time = models.IntegerField() # in minutes
    est_fare = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    
class UserActivity(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,db_index=True)
    session = models.ForeignKey(Session,db_index=True,null=True,blank=True)
    date = models.DateTimeField(help_text="Date Request started processing",auto_now_add=True,db_index=True)
    request_time = models.IntegerField(help_text="Time the request took to process (in microseconds)",null=True, blank=True)
    request_url = models.CharField(max_length=800,db_index=True)
    referer_url = models.URLField(verify_exists=False,db_index=True,blank=True,null=True)
    client_address = models.IPAddressField(blank=True,null=True)
    client_host = models.CharField(max_length=256,blank=True,null=True)
    browser_info = models.TextField(null=True,blank=True)
    error = models.TextField(null=True,blank=True)
    
    def set_request_time(self):
        from datetime import datetime
        if self is not None and self.date is not None:
            self.request_time = (datetime.now()-self.date).microseconds
            if (self.request_time is not None): self.save()
        
    def __unicode__(self):
        return '%s: %s - %s - %s' % (self.client_address,self.date,self.request_url,self.request_time)
    
    class Admin:
        pass
