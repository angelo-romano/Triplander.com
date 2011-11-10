# -*- coding: utf-8 -*-
import re
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from math import log
from urllib import unquote

dab_set = {
     u"å": ["a", "aa"], u"ä": ["a", "ae"], u"ñ": ["n"],
     u"ă": ["a"], u"â": ["a"], u"î": ["a"], u"ș": ["s"],
     u"ț": ["ț"], u"æ": ["ae"], u"ø": ["o", "oe"],
     u"ö": ["o", "oe"], u"þ": ["th"], u"á": ["a"],
     u"é": ["e"], u"ð": ["th", "d"], u"í": ["i"], 
     u"ó": ["o"], u"ú": ["u"], u"ý": ["y"], u"ć": ["c"], 
     u"č": ["c"], u"đ": ["d"], u"š": ["s"], u"ž": ["z"],
     u"ř": ["r"], u"ą": ["a"], u"ę": ["e"], u"ł": ["l"],
     u"ń": ["n"], u"ś": ["s"], u"ź": ["z"], u"ż": ["z"],
     u"õ": ["o"], u"ü": ["u"], u"ő": ["o"], u"ű": ["u"],
     u"ā": ["a"], u"ē": ["e"], u"ī": ["i"], u"ū": ["u"], 
     u"ŗ": ["r"], u"ļ": ["l"], u"ķ": ["k"], u"ņ": ["n"], 
     u"ģ": ["g"], u"ė": ["e"], u"į": ["i"], u"ų": ["u"], 
     u"ċ": ["c"], u"ġ": ["g"], u"ħ": ["h"], u"ı": ["i"],
     u"ğ": ["g"], u"ç": ["c"], u"à": ["a"], u"è": ["e"],
     u"ì": ["i"], u"ò": ["o"], u"ù": ["u"], u"ṣ": ["s"],
     u"ї": ["i"], u"ё": ["e"], u"ў": ["y"], u"ť": ["t"],
     u"ů": ["u"], u"ê": ["e"], u"ô": ["o"], u"ň": ["n"],}

def dab_string(string,no_surprises=False):
    #string_uni = unicode(string,"utf-8")
    string_list = list(string)
    string_ret = [""]
    for c in string_list:
            
        c_lo = c.lower()
        if dab_set.has_key(c_lo):
            occs = dab_set[c_lo]
            if no_surprises:
                string_ret = [string_ret[0]+occs[0]]
            else:
                string_ret2 = []
                for s in string_ret:
                    for repl in occs:
                        if (c == c_lo):
                            string_ret2.append(s+repl)
                        else:
                            if(len(repl) == 1):
                                string_ret2.append(s+repl.upper())
                            else:
                                string_ret2.append(s+repl[0].upper()+repl[1:])
            
                string_ret = string_ret2
        else:
            string_ret = [s+c for s in string_ret]

    if no_surprises:
        return string_ret[0]
    
    if(len(string_ret) == 1 and string_ret[0] == string):
        string_ret = None
    
    return string_ret

def encodeVector(vec):
	ret_v = []
	sorted_vec = []
	cnt2 = 0
	
	head_elem = None
	for cnt in range(len(vec)):
		cur_e = vec[cnt]
		if (cur_e > 0):
			ret_tuple = (cur_e, cnt)
			ret_v.append(ret_tuple)
			sorted_vec.append((cur_e, cnt2))
			cnt2 = cnt2 + 1

	sorted_vec.sort(lambda x,y: y[0]-x[0])
	head_elem = sorted_vec[0][1]
	last_sorted = sorted_vec[len(sorted_vec)-1][0]
	sorted_vec = [(sorted_vec[i-1][0], sorted_vec[i][1]) for i in range(1,len(sorted_vec))] + [(last_sorted, -1)]

	for cnt in range(len(ret_v)):
		c = ret_v[cnt]
		pos = binsearch(sorted_vec,c[0])
		#print "%d %d %s %s" % (cnt, pos, c, sorted_vec)
		real_pos = sorted_vec[pos][1]
		sorted_vec = sorted_vec[:pos] + sorted_vec[pos+1:]
		
		ret_v[cnt] = (c[0], c[1], real_pos)

	
	return {"vector": ret_v, "head": head_elem, "size": len(vec)}

def decodeVector(vec):
	ret_vec = [0 for x in range(vec["size"])]
	for e in vec["vector"]:
		ret_vec[e[1]] = e[0]
	
	return ret_vec

def decodeVectorAsSorted(vec):
	ret_vec = [0 for x in range(vec["size"])]
	idx = vec["head"]
	for i in range(len(vec["vector"])):
		e = vec["vector"][idx];
		ret_vec[i] = e[0]
		idx = e[2]
	return ret_vec

def binsearch(seq, search):
   right = len(seq)
   left = 0
   previous_center = -1
   if search > seq[0][0]:
       return -1
   while 1:

       center = (left + right) / 2

       candidate = seq[center][0]
        
       if search == candidate:
           return center
       if center == previous_center:
           return - 2 - center
       elif search > candidate:
           right = center
       else:
           left = center
       previous_center = center
       
def getCityObject(id=None,slug=None,name=None):
    from triplander.models import City, CityRedirect
    city = None
    try:
        if(id is not None):
            city = City.objects.get(id=id)
        elif(slug is not None or name is not None):
            if(slug is not None):
                cities = City.objects.filter(slug__iexact = slug)
            elif(name is not None):
                cities = City.objects.filter(name__iexact = name)
            if (len(cities)==0):
                city = None
            elif (len(cities)==1):
                city = cities[0]
            else:
                city = cities
    except ObjectDoesNotExist:
        city = None
        
    if(city is None and name is not None):
        try: 
            city_red = CityRedirect.objects.get(name__iexact = dfrom)
        except ObjectDoesNotExist:
            city_red = None
        
        if city_red is not None: city = city_red.city

    return city

def dec_log(c, base=10):
	return Decimal(str(log(c)/log(base)))

def tl_response(name,vars,session=None):
    
    tl_additions = {'tl_logged_user': {
                                       'id' : None,
                                       'is_logged': False,
                                       'username': None,
                                       'can_add_cities'    : False,
                                       'can_edit_cities'   : False, 
                                       'can_edit_airports' : False, 
                                       'can_edit_countries': False, 
                                       }}
    if (session is not None):
        
        if(session.get('user_id') is not None): # logged user stored into session
            tl_additions['tl_logged_user']['id']                 = session['user_id']
            tl_additions['tl_logged_user']['is_logged']          = True
            tl_additions['tl_logged_user']['username']           = session['user_name']
            tl_additions['tl_logged_user']['can_add_cities']     = True
            tl_additions['tl_logged_user']['can_edit_cities']    = True
            tl_additions['tl_logged_user']['can_edit_airports']  = True
            tl_additions['tl_logged_user']['can_edit_countries'] = True
            
    return render_to_response(name,dict(vars,**tl_additions))

def tl_logged_user(session):
    from triplander.models import ApplicationUser
    # the user MUST be a valid one and currently logged
    if (session is None): return None 
    if (session.get('user_id') is None): return None

    try:
        user = ApplicationUser.objects.get(id=session['user_id'])
    except ObjectDoesNotExist:
        return None
    
    return user
    
def get_wikiname_by_url(wname_string):
    m = re.match('^(?:http://)?(?:en\.|www\.)wikipedia\.org/wiki/(.+)$', wname_string)
    if(m):
        base_string = m.group(1)
    else:
        base_string = wname_string
    
    if(wname_string is None): return None
    if(len(wname_string) < 2): return None
    return unquote(base_string).replace(' ','_')
