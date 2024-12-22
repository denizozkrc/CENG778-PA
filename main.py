from searchEngineSimulator import SearchEngineSimulator
import matplotlib.pyplot as plt

k_values = [8, 32]

dataset = (open(file="./datasets/wordlist.txt", mode="r")).read()
index_dict = {}
for line in dataset.split("\n"):
    if len(line) == 0:
        continue
    parts = line.split(" ")
    key = parts[0]
    value = [int(parts[1]), 0]  # 0 will be replaced while term partitioning
    index_dict[key] = value  # We can discard the second number. {"eddie" : [7, 0]} PLL=7, node_num =0 (to be updated)

querylist = (open(file="./datasets/10000.topics", mode="r")).read()
query_list = []
for line in querylist.split("\n"):
    if len(line) == 0:
        continue
    parts = line.split(":", 1)
    query = parts[1].split(" ")
    query_list.append(query)  # ['after', 'school', 'program', 'evaluation']

simulator = SearchEngineSimulator(index_dict, k_values)

term_based_costs, node_costs_term = simulator.run(query_list, type="term")
doc_based_costs, total_cost_per_node = simulator.run(query_list, type="doc")

average_QP_term = [0] * len(k_values)
average_QP_doc = [0] * len(k_values)
average_load_per_node = [0] * len(k_values)
for k in range(len(k_values)):
    average_QP_term[k] = sum(term_based_costs[k])/len(term_based_costs[k])
    average_QP_doc[k] = sum(doc_based_costs[k])/len(doc_based_costs[k])
    average_load_per_node[k] = sum(node_costs_term[k])/len(node_costs_term[k])

print("Average QP cost with term-based partitioning: ", average_QP_term)
print("Average QP cost with document-based partitioning: ", average_QP_doc)
print("QP cost per node with document-based partitioning: ", total_cost_per_node)
print("average QP cost per node with term-based partitioning: ", average_load_per_node)

"""
term_based_costs = [for each k][for each query]
node_costs_term = [for each k][for each node]

doc_based_costs = [for each k][for each query]
total_cost_per_node = [for each k]
"""

for k_index, costs in enumerate(node_costs_term):
    node_numbers = list(range(len(costs)))

    # Create a new figure for each k
    plt.figure()
    plt.plot(node_numbers, costs, marker='o', label=f'k={len(node_numbers)-1}')
    plt.title(f'Plot for K={len(node_numbers)-1}')
    plt.xlabel('Node Numbers')
    plt.ylabel('Values')
    plt.grid(True)
    plt.legend()
    plt.show()
