import aocutils
import copy
import heapq
import itertools
from typing import List, Dict, Set, FrozenSet

test_array = [
    "jqt: rhn xhk nvd",
    "rsh: frs pzl lsr",
    "xhk: hfx",
    "cmg: qnr nvd lhk bvb",
    "rhn: xhk bvb hfx",
    "bvb: xhk hfx",
    "pzl: lsr hfx nvd",
    "qnr: nvd",
    "ntq: jqt hfx bvb xhk",
    "nvd: lhk",
    "lsr: lhk",
    "rzs: qnr cmg lsr rsh",
    "frs: qnr lhk lsr",
]

EDGE_WEIGHT_FACTOR = 100.0

def parse_data(input: List[str]):

    nodes = {}
    edges = {}

    for line in input:
        node, connections_str = line.split(":")
        connections = connections_str.split()
        if node not in nodes:
            nodes[node] = set()
        for conn in connections:
            nodes[node].add(conn)
            if conn not in nodes:
                nodes[conn] = set()
            nodes[conn].add(node)
            edges[frozenset({node, conn})] = 0.0
    
    return nodes, edges

def find_path(node_start: str, node_end: str, nodes: Dict[str, Set[str]], edges: Dict[FrozenSet[str], float], max_weight: float = 1.0):

    heap = []
    visited_nodes = set()
    dist_node = {}
    prev_node = {}
    tag_node = {}
    tag_count = 0

    heapq.heappush(heap, (0, node_start, tag_count))
    dist_node[node_start] = 0
    prev_node[node_start] = None
    tag_node[node_start] = tag_count
    tag_count += 1

    while len(heap) > 0:
        _, node, node_tag = heapq.heappop(heap)
        if tag_node[node] != node_tag:
            continue # Was invalidated by a better path
        if node == node_end:
            break

        visited_nodes.add(node)
        
        for next_node in nodes[node]:
            if next_node in visited_nodes:
                continue
            if edges[frozenset({node, next_node})] >= max_weight:
                continue # Max weight already reached

            next_weight = dist_node[node] + 1 + (edges[frozenset({node, next_node})] * EDGE_WEIGHT_FACTOR)
            if next_node in dist_node and next_weight >= dist_node[next_node]:
                continue

            heapq.heappush(heap, (next_weight, next_node, tag_count))
            dist_node[next_node] = next_weight
            prev_node[next_node] = node
            tag_node[next_node] = tag_count
            tag_count += 1
    else:
        # Did not find a path
        return None
    
    shortest_path = []
    node = node_end
    while node:
        shortest_path.append(node)
        node = prev_node[node]
    shortest_path.reverse()
    return shortest_path

def fill_path(path: List[str], edges: Dict[FrozenSet[str], float], path_weight: float):
    for i, node in enumerate(path[:-1]):
        edges[frozenset({path[i], path[i+1]})] += path_weight

def find_bridges(nodes_ref: Dict[str, Set[str]], edges_ref: Dict[FrozenSet[str], float], bridge_count: int):

    for node_start, node_end in itertools.combinations(nodes_ref.keys(), 2):
        nodes = copy.deepcopy(nodes_ref)
        edges = copy.deepcopy(edges_ref)

        for _ in range(bridge_count * 4):
            path = find_path(node_start, node_end, nodes, edges, 1.0)
            if not path:
                break
            fill_path(path, edges, 0.25)
        else:
            # Test that no more paths are possible...
            path = find_path(node_start, node_end, nodes, edges, 1.0)
            if path:
                continue
            full_edge_count = 0
            bridges = set()
            for edge, value in edges.items():
                if value >= 1.0:
                    bridges.add(edge)
                    full_edge_count += 1
            if full_edge_count == bridge_count:
                return bridges

def get_groups(nodes_ref: Dict[str, Set[str]], edges_ref: Dict[FrozenSet[str], float], bridge_count: int):

    nodes = copy.deepcopy(nodes_ref)
    edges = copy.deepcopy(edges_ref)
    bridges = find_bridges(nodes_ref, edges_ref, bridge_count)

    for bridge in bridges:
        del edges[bridge]

    groups = []
    while len(nodes):
        new_group = set()
        groups.append(new_group)
        stack = []
        stack.append(nodes.popitem())
        while len(stack):
            node, connections = stack.pop()
            new_group.add(node)
            for conn in connections:
                if conn in nodes and frozenset({node, conn}) in edges:
                    stack.append((conn, nodes[conn]))
                    del nodes[conn]
    return groups

if __name__ == "__main__":

    input_data = aocutils.getDataInput(25)
    #input_data = test_array

    nodes_ref, edges_ref = parse_data(input_data)

    #### Part 1 ####

    groups = get_groups(nodes_ref, edges_ref, 3)
    result_1 = 1
    for g in groups:
        result_1 *= len(g)
    aocutils.printResult(1, result_1)