import networkx as nx
import numpy as np
import scipy as sp
import time
n = 10
m = 20000

# build an undirected weighted graph from input file
# return the largest connected component in graph
def build_graph(file_path):
    t1 = time.time()
    graph = nx.Graph()
    file = open(file_path)
    lines = file.readlines()
    lines = [line.split() for line in lines]
    print('Start building graphs from the file')
    for i in range(m):
        node1 = int(lines[i][0][1:])
        node2 = int(lines[i][1])
        weight = int(lines[i][2])
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(node1, node2, weight=weight)

    print('Finish building graphs from the file')
    largest_subgraph = find_largest_connected_graph(graph)
    return largest_subgraph


def find_largest_connected_graph(graph):
    largest_component = max(nx.connected_components(graph), key=len)
    largest_subgraph = graph.subgraph(largest_component)
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


# return new connected graph after removing n top weighted nodes with edges
def remove_connection(graph, connections_to_be_removed):
    new_graph = graph.copy()
    for node in connections_to_be_removed:
        if node in new_graph:
            new_graph.remove_node(node)

    largest_connected_subgraph = find_largest_connected_graph(new_graph)
    return largest_connected_subgraph


def calculate_stats(graph):
    t2 = time.time()
    degree_separation = nx.average_shortest_path_length(graph, weight='weight')
    print(f'the degree of separation on average between any two authors is {degree_separation}')
    print(f"The time taken to calculate the statistics from the graph was {time.time()-t2}")


def main():
    file_path = "../dataset/AMiner-Coauthor.txt"
    graph = build_graph(file_path)
    connections_to_be_removed = find_top_n_nodes(graph)
    new_graph = remove_connection(graph, connections_to_be_removed)
    print("Stats in original graph:")
    calculate_stats(graph)
    print("Stats in graph after removing important connections:")
    calculate_stats(new_graph)


if __name__ == '__main__':
    main()
