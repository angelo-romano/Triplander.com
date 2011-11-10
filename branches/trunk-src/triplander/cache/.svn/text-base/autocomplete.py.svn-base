from django.core.cache import cache
from triplander.models import City, Country

AC_CACHE_SUBTREE_KEY = "acSuffixTree[%s,%s]"
AC_CACHE_KEYLIST_KEY = "acSuffixTreeKeys[%s]"
AC_CACHE_TIMEOUT = 60*60*72 # 3 days

# suffix tree - generic class
class SuffixTree:
    # tree[0]: suffix, tree[1]: value; tree[2]: subtree
    tree = [None,None,{}] # empty tree
    ENDING_CHAR = "$" # ending character
    _term_shifting = False
    
    # initializes a new class instance
    def __init__(self,term_shifting=False):
        # term shifting: if you add "ciao", you want to be able to find every possible
        # substring into it (not just prefixes), so you are going to store all
        # possible shifts of the term (ciao$, iao$c, ao$ci, o$cia, $ciao)
        self._term_shifting = term_shifting 
    
    # add a term into the tree
    def add(self,term,val=True):
        my_term = "%s%s" % (term.lower(),self.ENDING_CHAR)
        term_list = [my_term]
        if(self._term_shifting): # also add shifted version (ciao$, iao$c, ao$ci, o$cia)
            for i in xrange(1,len(my_term)):
                new_term = my_term[i:]+my_term[:i]
                term_list.append(new_term)
        
        #tree_iter = self.tree.iteritems()
        
        prefix_set = False
        
        # tree walk in order to add the new term into it
        for this_term in term_list:
            cur_node = self.tree
            for i in xrange(0,len(this_term)):
                if(not cur_node[2].has_key(this_term[i])):
                    
                    if(i==(len(this_term)-1)): # last loop cycle
                        this_suffix = None
                    else:
                        this_suffix = this_term[i+1:]
                    
                    cur_node[2][this_term[i]] = [this_suffix,val,{}]
                    
                    cur_node = cur_node[2][this_term[i]]
                else:
                    cur_node = cur_node[2][this_term[i]]
                    if(cur_node[0] is not None):
                        cur_node[0] = None
                        cur_node[1] = None
                
    # find term(s) with a given prefix/substring
    def find(self,prefix):
        # tree walk
        my_prefix = prefix.lower()
        cur_node  = self.tree
        for i in xrange(0,len(my_prefix)):
            # no more available paths -> not found
            if (not cur_node[2].has_key(my_prefix[i])): return {}
            
            cur_node = cur_node[2][my_prefix[i]]
            
            # directly found only a single instance -> returns it 
            if(cur_node[1] is not None): 
                return {
                        self._term_process(my_prefix[:i+1]+cur_node[0]): cur_node[1]
                        }

        # in-depth search
        results = {}
        self._depth_visit(cur_node,prefix,results)
        return results
    
    # term processing f("ao$ci") = f("ciao$") = "ciao"
    def _term_process(self,s):
        pos = s.find(self.ENDING_CHAR)
        if (pos == -1): return None # not found!!!
        
        return s[pos+1:]+s[:pos]
    
#    def _term_not_present(self,term,results):
#        if(results.has_key(term)): return False
#        return True
    
    # adapted depth-first search
    def _depth_visit(self,tree,prefix,results):
        if tree is None or len(tree) != 3: return False

        for (key, val) in tree[2].iteritems():
            # found - optimized path, return it
            if val[1] is not None and val[0] is not None: # suffix & values set
                results[self._term_process(prefix+key+val[0])] = val[1]

            # recursion
            for k in val[2].keys():
                self._depth_visit(val,prefix+key,results)
            
            # found - non-optimized path, return it
            if val[1] is not None and val[0] is None:
                results[self._term_process(prefix+key)] = val[1]
            
        return False
    
    # use an existing tree
    def setTree(self,tree):
        self.tree = [None, None, tree]
        
    # returns the tree
    def getTree(self): 
        return self.tree[2]

    # add a tree part (autocompletion optimization)
    def addTreePart(self,tree_part,key):
        self.tree[2][key] = tree_part

##########################
##
## Procedures used by autocompletion stuff 
##
##########################
AUTOCOMPLETE_TYPES = {'city': City, 'country': Country}

# BASE AUTOCOMPLETER - Used by City and Country autocompleters by inheritance
class BaseAutocompleter:
    # suffix tree
    suffix_tree = None
    
    # constructor - does nothing
    def __init__(self):
        pass
    
    # get cache key names
    @classmethod
    def _get_cachekey_subtree(cls,k):
        return AC_CACHE_SUBTREE_KEY % (cls._get_type(),k)
    @classmethod
    def _get_cachekey_keylist(cls):
        return AC_CACHE_KEYLIST_KEY % cls._get_type()
    # get/check type
    @staticmethod
    def _get_type():
        return ''
    
    @classmethod
    def _check_type(cls):
        if(AUTOCOMPLETE_TYPES.has_key(cls._get_type())): return True
        return False
    
    # adds an element to our suffix tree
    def add_element(self,elem):
        pass

    # initialize the WHOLE suffix tree
    @classmethod
    def initialize_suffix_tree(cls):
        # check type
        if(not cls._check_type()): return None
        type = cls._get_type() 

        new_ac = cls() # initialize new instance
        new_ac.suffix_tree = SuffixTree() # initialize a new suffixtree
        
        contents = AUTOCOMPLETE_TYPES[type].objects.all()
        for c in contents:
            new_ac.add_element(c)
	
	del contents       
 
        # save into cache
        keylist = []
        for (k, subtree) in new_ac.suffix_tree.getTree().iteritems():
            keylist.append(k)
            this_cache_key = cls._get_cachekey_subtree(k)
            cache.set(this_cache_key,subtree,AC_CACHE_TIMEOUT)
        
        # keylist cached as well
        cache.set(cls._get_cachekey_keylist(), keylist, AC_CACHE_TIMEOUT)
        
        # returns a new autocompleter instance
        return new_ac
    
    # get the whole tree
    @classmethod
    def get_whole_tree(cls,type):
        # check type
        if(not cls._check_type()): return None 
        type = cls._get_type()

        keylist = cache.get(cls._get_cachekey_keylist())
        if keylist is None:
            new_ac = cls.initialize_suffix_tree()
            return new_ac
        else:
            new_ac = cls()
            new_ac.suffix_tree = SuffixTree()
            for k in keylist:
                this_subtree = cache.get(cls._get_cachekey_subtree(k))
                if(this_subtree is not None): # valid subtree - adding it 
                    new_ac.suffix_tree.addTreePart(this_subtree,k)
                    
            return new_ac
    
    # get a tree part
    @classmethod
    def get_tree_part(cls,k):
        # check type
        if(not cls._check_type()): return None 
        type = cls._get_type()
        
        this_subtree = cache.get(cls._get_cachekey_subtree(k))
        
        if(this_subtree is not None):
            new_ac = cls()
            new_ac.suffix_tree = SuffixTree() 
            new_ac.suffix_tree.addTreePart(this_subtree,k)
        else: # not found, initialize the structure
            new_ac = cls.initialize_suffix_tree()
            # another optimization - empty all the suffix tree
            new_ac.suffix_tree.tree[2] = {}
            return cls.get_tree_part(k)
            
        return new_ac
    
    # reset cached info
    @classmethod
    def reset_cache(cls,k=None):
        keylist = cache.get(cls._get_cachekey_keylist())
        if(keylist is not None):
            if(k is None):
                for this_k in keylist: 
                    cache.delete(cls._get_cachekey_subtree(this_k))
                
                cache.delete(cls._get_cachekey_keylist())
            else:
                cache.delete(cls._get_cachekey_subtree(k))
                

# CITY AUTOCOMPLETER     
class CityAutocompleter(BaseAutocompleter):
    @staticmethod
    def _get_type(): return 'city'

    def add_element(self,elem):
        vals = [elem.name, 
                elem.id, 
                elem.slug, 
                elem.country.name, 
                elem.country.getFlagPath(),
                elem.total_rating]
        self.suffix_tree.add(elem.name, val=vals)
        
    # get cities
    def get_cities(self,prefix,offset=10):
        resp = self.suffix_tree.find(prefix).values()
        def sort_compare(x,y):
            if(x[5] > y[5]): return -1
            else: return 1
            
        resp.sort(sort_compare)
        resp = [r[:5] for r in resp]
        return resp[:offset]

# COUNTRY AUTOCOMPLETER         
class CountryAutocompleter(BaseAutocompleter):
    @staticmethod
    def _get_type(): return 'country'

    def add_element(self,elem):
        vals = [elem.name, elem.id, elem.slug, elem.name, elem.getFlagPath()]
        self.suffix_tree.add(elem.name, val=vals)
        
    # get cities
    def get_countries(self,prefix,offset=10):
        resp = self.suffix_tree.find(prefix).values()
        def sort_compare(x,y):
            if(x[0] > y[0]): return 1
            else: return -1
            
        resp.sort(sort_compare)
        
        return resp[:offset]
