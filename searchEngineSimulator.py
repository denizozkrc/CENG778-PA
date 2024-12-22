class SearchEngineSimulator:

    def __init__(self, indexFile, k_values):
        self.indexFile = indexFile
        self.k_values = k_values

    def run(self, query_list, type):
        if type == "term":  # Term Based Partitioning:
            term_based_costs = [0]*len(self.k_values)
            node_costs_term = [0]*len(self.k_values)
            for k, K in enumerate(self.k_values):
                total_costs = [0]*len(query_list)  # total cost for each query
                total_cost_each_node = [0]*(K+1)  # total cost for each node
                for i, val in enumerate(self.indexFile.values()):
                    val[1] = (i % K)+1  # node number. 0 is the broker, so not used here
                for q, query in enumerate(query_list):
                    query_len = len(query)
                    nodes = [[0, 0, 0] for _ in range(K + 1)]  # +1 for the broker. first is number of terms, second is total posting length, third is for min posting length
                    costs = [0]*(K+1)  # index 0 is for the broker
                    for term in query:
                        if term not in self.indexFile:
                            query_len -= 1
                            continue
                        node_num = self.indexFile[term][1]  # which node is it on
                        nodes[node_num][0] += 1  # number of terms
                        nodes[node_num][1] += self.indexFile[term][0]  # total posting length
                        if self.indexFile[term][0] < nodes[node_num][2] or nodes[node_num][2] == 0:
                            nodes[node_num][2] = self.indexFile[term][0]

                    for i, node in enumerate(nodes):
                        if i == 0:
                            continue

                        if node[0] == 0:  # no term here
                            continue
                        elif node[0] == query_len:  # all terms here
                            costs[i] = node[1]  # all done in node, nothing in broker
                        elif node[0] == 1:  # multiterm query, one term here
                            costs[0] += node[2]  # nothing done in node, add cost on broker
                        else:  # mulitple terms in this node, but not all
                            costs[i] = node[1]  # total posting list cost in node
                            costs[0] += node[2]  # min posting list cost in the broker
                    total_costs[q] = costs[0] + max((cost for cost in costs[1:] if cost != 0), default=0)
                    total_cost_each_node = [total + cost for total, cost in zip(total_cost_each_node, costs)]
                term_based_costs[k] = total_costs
                node_costs_term[k] = total_cost_each_node
            return term_based_costs, node_costs_term

        elif type == "doc":  # Document Based Partitioning:
            doc_based_costs = [0]*len(self.k_values)
            total_cost_per_node = [0]*len(self.k_values)
            for k, K in enumerate(self.k_values):
                total_costs = [0]*len(query_list)
                for q, query in enumerate(query_list):
                    query_len = len(query)
                    cost = 0
                    for term in query:
                        if term not in self.indexFile:
                            query_len -= 1
                            continue
                        cost += (self.indexFile[term][0]/K)+1  # +1 for ceiling. same cost for each node
                    total_cost_per_node[k] += cost  # same for each node so calculate only for one node
                    total_costs[q] = cost  # total cost of a query = cost of a query at a single node
                doc_based_costs[k] = total_costs
            return doc_based_costs, total_cost_per_node

        else:
            raise ValueError("Invalid partition type. Use 'term' or 'doc'.")
