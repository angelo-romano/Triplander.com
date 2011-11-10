from django.core.urlresolvers import reverse # URL reversal
from django.core.cache import cache

def blue_get(path):
    url_s = "httpSerialize[%s]" % path

    resp = cache.get(url_s)
    return resp

def blue_set(path,resp,cache_timeout=300):
    if(cache_timeout > 0):
        url_s = "httpSerialize[%s]" % path
        cache.set(url_s,resp,cache_timeout)
        
def blue_delete_all(id):
    cacheable_blue_urlnames = ['blue_panoramio','blue_wikipedia_city']
    cacheable_blue_urls = [reverse(url,args=[id]) for url in cacheable_blue_urlnames]
    
    for url in cacheable_blue_urls:
        keyname = "httpSerialize[%s]" % url
        cache.delete(keyname)

    

