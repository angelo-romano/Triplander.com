# coding: utf8
import json
from wikimarkup import parse
fh = open("ciccio.txt", "r");
content = fh.read()
fh.close()
obj = json.read(content)
obj = obj['query']['pages']['25458']['revisions'][0]['*']
obj = obj[0:12000]
#print(obj)
print parse(obj)
