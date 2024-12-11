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

simulator = SearchEngineSimulator(index_dict)
simulator.run()
