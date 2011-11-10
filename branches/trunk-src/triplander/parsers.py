import os
#import path
import re
import string
from os import path, environ

class wiki:
    """Object that turns Wiki markup into HTML.

    All formatting commands can be parsed one line at a time, though
    some state is carried over between lines."""
    
    _patterns = {
        'hr': re.compile(u'''^---*''', re.UNICODE | re.MULTILINE),
        'h6': re.compile(u'^======\s*(.*[^\s])\s*======\s*$', re.UNICODE | re.MULTILINE),
        'h5': re.compile(u'^=====\s*(.*[^\s])\s*=====\s*$', re.UNICODE | re.MULTILINE),
        'h4': re.compile(u'^====\s*(.*[^\s])\s*====\s*$', re.UNICODE | re.MULTILINE),
        'h3': re.compile(u'^===\s*(.*[^\s])\s*===\s*$', re.UNICODE | re.MULTILINE),
        'h2': re.compile(u'^==\s*(.*[^\s])\s*==\s*$', re.UNICODE | re.MULTILINE),
        'h1': re.compile(u'^=\s*(.*[^\s])\s*=\s*$', re.UNICODE | re.MULTILINE),
        'i': re.compile(u'\'\'(.+)\'\'', re.UNICODE | re.MULTILINE),
        'b': re.compile(u'\'\'\'(.+)\'\'\'', re.UNICODE | re.MULTILINE),
        'img': re.compile(u'\[\[Image:([^\]]+)\]\]\s*', re.UNICODE | re.MULTILINE),
        'cat': re.compile(u'\[\[Category:[^\]]+\]\]\s*', re.UNICODE | re.MULTILINE),
        'interwiki': re.compile(u'\[\[[a-z\-]+\:[^\]]+\]\]', re.UNICODE | re.MULTILINE),
        'a' : re.compile(u'\[\[([^\]]+)\]\]', re.UNICODE | re.MULTILINE),
        'tmpl': re.compile(u'{{(.+)}}', re.UNICODE | re.MULTILINE),
        'ref': re.compile(u'<ref>.*?</ref>', re.UNICODE | re.MULTILINE),
        'empty1': re.compile(u'\(\s*\)',re.UNICODE | re.MULTILINE),
        'comment': re.compile(u'<!--(.*?)-->',re.UNICODE | re.MULTILINE),
        'ol': re.compile(u'^\*\s*(.*[^\s])\s*$',re.UNICODE | re.MULTILINE),
        'ul': re.compile(u'^\:\s*(.*[^\s])\s*$',re.UNICODE | re.MULTILINE),
    }
    _pattern_order = [ 'ref', 'tmpl', 'comment',
                       'b', 'i', 
                       'ol',
                       'h6', 'h5', 'h4', 'h3', 'h2', 'h1', 'hr',
                       'img', 'cat', 'interwiki', 'a',
                       'empty1' ] 
                      
    _replacements = {
        'hr': ur'<hr />',
        'h1': ur'<h1>\1</h1>',
        'h2': ur'<h2>\1</h2>',
        'h3': ur'<h3>\1</h3>',
        'h4': ur'<h4>\1</h4>',
        'h5': ur'<h5>\1</h5>',
        'h6': ur'<h6>\1</h6>',
        'img': ur'<img src="\1" alt="\1" />',
        'a' : ur'<a>\1</a>',
        'b' : ur'<strong>\1</strong>',
        'i' : ur'<i>\1</i>',
        'ol': ur'<ol>\1</ol>',
        'cat': '',
        'tmpl': '',
        'ref': '',
        'interwiki': '',
        'comment': '',
        'empty1': '',
    }

    def __init__(self, raw):
        self.raw = raw
        
    def parse(self, raw=None):
        if (raw is None):
            new_raw = self.raw
        else:
            new_raw = raw
            
        for k in self._pattern_order:
            new_raw = self._patterns[k].sub(self._replacements[k],new_raw)
            
        return new_raw