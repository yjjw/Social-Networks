import networkx as nx
import numpy as np
import scipy as sp
import time
n = 300


# build an undirected weighted graph from input file
# return the largest connected component in graph
def build_graph(file_path):
    t1 = time.time()
    graph = nx.Graph()
    file = open(file_path)
    lines = file.readlines()
    lines = [line.split() for line in lines]
    print('Start building graphs from the file')
    for line in lines:
        node1 = int(line[0][1:])
        node2 = int(line[1])
        weight = int(line[2])
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(node1, node2, weight=weight)

    print('Finish building graphs from the file')
    largest_component = max(nx.connected_components(graph), key=len)
    print('Start building largest component subgraph')
    # for node1 in largest_component:
    #     largest_subgraph.add_node(node1)
    #     for node2 in graph[node1].keys():
    #         largest_subgraph.add_node(node2)
    #         weight = graph[node1][node2]['weight']
    #         largest_subgraph.add_edge(node1, node2, weight=weight)
    largest_subgraph = graph.subgraph(largest_component)
    print('Finish building the largest component subgraph')
    print(f"The time taken to build the largest connected graph from the file was {time.time()-t1}")
    return largest_subgraph


# identify top n weighted nodes in the largest component of original graph
def find_top_n_nodes(graph):
    pr = nx.pagerank(graph, weight='weight')
    top_n_weighted_nodes = []
    # sort by weight value
    for node, weight in sorted(pr.items(), key=lambda kv: [kv[1], kv[0]]):
        top_n_weighted_nodes.append(node)
        if len(top_n_weighted_nodes) >= n:
            break

    return top_n_weighted_nodes


# return new graph after removing n top weighted nodes with edges
def remove_connection(graph, connections_to_be_removed):
    for node in connections_to_be_removed:
        if node in graph:
            del node
    return graph


def calculate_stats(graph):
    t2 = time.time()
    degree_separation = nx.average_shortest_path_length(graph, weight='weight')
    print(f'the degree of separation on average between any two authors is {degree_separation}')
    print(f"The time taken to calculate the statistics from the graph was {time.time()-t2}")


def main():
    file_path = "../dataset/AMiner-Coauthor.txt"
    graph = build_graph(file_path)
    print("Stats in original graph:")
    calculate_stats(graph)
    # connections_to_be_removed = find_top_n_nodes(graph)
    # new_graph = remove_connection(graph, connections_to_be_removed)


if __name__ == '__main__':
    main()
