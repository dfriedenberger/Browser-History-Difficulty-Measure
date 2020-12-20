from src.util import *
import json


statistic = read_history("private/chrome-history.json","private/filter_url.json")



#fix day 13 "seconds": 9650, //27650-18000
#statistic["2020-13"]["part"][1]["seconds"] -= 18000
#statistic["2020-20"]["part"][0]["seconds"] -= 7200
#statistic["2020-20"]["part"][1]["seconds"] -= 10800

statistic_json = json.dumps(statistic, indent = 2)
text_file = open("public/data/data-gen.js", "w")
text_file.write("var generate = "+statistic_json+";\n")
text_file.close()
