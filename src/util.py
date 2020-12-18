
import json
import re
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs


def parse_id(visitTime,urlcomp,urlquery):
    if(urlcomp.netloc != "adventofcode.com"): return None
    m = re.search(r'^/([0-9]+)/day/([0-9]+)',urlcomp.path)
    if not m: return None
    year = int(m.group(1))
    if year != 2020: return None
    day = int(m.group(2))
    if day != visitTime.day: return None
    return "{0}-{1}".format(year,day)

def is_end_candidate(visitTime,urlcomp,urlquery):
    if(urlcomp.netloc != "adventofcode.com"): return False
    if(urlcomp.path.endswith("/answer")): return True
    return False

def is_start_part2(visitTime,urlcomp,urlquery):
    if(urlcomp.netloc != "adventofcode.com"): return False
    if(urlcomp.fragment == "part2"): return True
    return False

def should_filter(visitTime,urlcomp,urlquery):
    if(urlcomp.netloc == "web.whatsapp.com"): return True
    if(urlcomp.netloc == "sso2.service.deutschebahn.com"): return True

    return False

def read_history(file,filter_file):

    with open(filter_file,encoding='utf-8') as json_filter:
        filter = json.load(json_filter)
    
    with open(file,encoding='utf-8') as json_file:
        historyList = json.load(json_file)

        statistic = {}
        id = None
        
        part = -1
        candidates = []
        for history in reversed(historyList):
            try:
                visitTime = datetime.fromtimestamp(float(history['visitTime'])/ 1000) 
                urlcomp   = urlparse(history['url'])
                urlquery = parse_qs(urlcomp.query)
                
                # filter private url
                if urlcomp.netloc in filter: continue

                # Start https://adventofcode.com/2020/day/17
                parseId = parse_id(visitTime,urlcomp,urlquery)

                
                if parseId:
                    if id != parseId:
                        #dump
                        #if id == "2020-2" or id == "2020-1":
                        #    print(id,json.dumps(statistic[id], indent = 2))

                        # Id changed, is_start
                        id = parseId
                        part = 0
                        candidates = []
                        start_time = visitTime
                        statistic[id] = { "start" : visitTime.strftime('%d. %B %H:%M') , "part": [] }
                        print("Start",visitTime.strftime('%d. %B %H:%M') ,history['url'])

                if id:
                    candidates.append((history,visitTime,urlcomp,urlquery))

                    if is_start_part2(visitTime,urlcomp,urlquery): 
                        print("Start2",visitTime.strftime('%d. %B %H:%M') ,history['url'])
                        part = 1

                    if part >= len(statistic[id]['part']):
                        statistic[id]['part'].append({ "stop": "", "attempts": 0, "seconds" : 0,  "search" : [] , "tutorial" : []})
                    # Ende https://adventofcode.com/2020/day/18/answer
                    if is_end_candidate(visitTime,urlcomp,urlquery):
                        for (h,v,o,a) in candidates:
                            if o.netloc == "adventofcode.com": continue #Ignore
                            if o.netloc == "www.google.com" and o.path == "/search":
                                statistic[id]['part'][part]["search"].append(a['q'])
                                continue
                            else:
                                statistic[id]['part'][part]["tutorial"].append((o.netloc,o.path))
                        
                        candidates = []
                        statistic[id]['part'][part]["stop"] = visitTime.strftime('%d. %B %H:%M')

                        statistic[id]['part'][part]["seconds"] = int((visitTime-start_time).total_seconds())

                        statistic[id]['part'][part]["attempts"] += 1

                        print("Ende (candidate) Part:",part,visitTime.strftime('%d. %B %H:%M'),history['url'])
              
            except Exception as e:
                print(e)
                print(history['visitTime'] ,history['url'])

        return statistic
