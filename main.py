from searchEngineSimulator import SearchEngineSimulator

dataset = (open(file="./datasets/wordlist.txt", mode="r")).read()

index_dict = {}
for line in dataset.split("\n"):
    if len(line) == 0:
        continue
    parts = line.split(" ")
    key = parts[0]
    value = parts[1]
    index_dict[key] = value  # We can discard the second number

querylist = (open(file="./datasets/10000.topics", mode="r")).read()

query_list = []
for line in querylist.split("\n"):
    if len(line) == 0:
        continue
    parts = line.split(":", 1)
    query = parts[1].split(" ")
    query_list.append(query)

simulator = SearchEngineSimulator(index_dict)
simulator.run(query_list)
