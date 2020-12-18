from src.util import *
import json


statistic = read_history("private/chrome-history.json","private/filter_url.json")

statistic_json = json.dumps(statistic, indent = 2)
text_file = open("public/data/data-gen.js", "w")
text_file.write("var generate = "+statistic_json+";\n")
text_file.close()
