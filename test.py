# SWAMI KARUPPASWAMI THUNNAI

import json
import time
import dateparser
import matplotlib.pyplot as plt



with open("E:\\aibeing\\solar-panel (2)\\slp\\solar_panel\\result.json", "r") as file:
    contents = json.load(file)

plot_data = dict()
for i in contents:
    for j in contents[i]["data"]:
        #print(j["TIME_STAMP"])
        plot_data[j["TIME_STAMP"]] = dict()
        for k in j:
            if "FIELD" in k:
                plot_data[j["TIME_STAMP"]][k] = j[k]
# print("plot_data",plot_data)

graphs = list()
for i in plot_data:
    for j in plot_data[i]:
        graphs.append(j)
# print('graphs',graphs)

graphs = list(set(graphs))

final_graph = dict()

for graph in graphs:
    final_graph[graph] = {"x": list(), "y": list(), "type": "scatter"}
    for i in plot_data:
        seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
        final_graph[graph]["x"].append(seconds)
        final_graph[graph]["y"].append(plot_data[i][graph])
print('final_graph',final_graph['FIELD12'])

out = []

for i in final_graph:
    out.append(final_graph[i])

with open("out.json", "w") as oup:
    oup.write(json.dumps(out))

#del final_graph["FIELD17"]["X"][3:]
#del final_graph["FIELD17"]["y"][3:]
#print(final_graph["FIELD17"])


