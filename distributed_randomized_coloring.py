# Centralized Simulation of a Distributed Randomized Coloring Algorithm
# Read the README for more information.

import networkx.generators.random_graphs as nx
import random

# debug flags
DEBUG = True  # set to False to disable all debug messages
GRAPH = True
INIT = False
SELECT_RANDOM_COLOR = True
NOTIFY_NEIGHBORS = False
NOTIFY_NEIGHBORS_DETAILED = False
COLOR = True
REMOVE_FROM_AVAILABLE_COLORS = False
DISCARD = True
UNCOLORED_NODES = True
VERIFY_COLORING = True


def debug(type=True, *args, **kwargs):
    if type and DEBUG:
        print(*args, **kwargs)


def verify_coloring(graph):
    for node in graph.nodes:
        for neighbor in graph.neighbors(node):
            assert graph.nodes[node]["color"] != graph.nodes[neighbor]["color"]
    debug(VERIFY_COLORING, "Coloring is valid")


def get_max_degree(graph):
    max_degree = 0
    for node in graph.nodes:
        if graph.degree(node) > max_degree:
            max_degree = graph.degree(node)
    return max_degree


def initialize(graph, node, colors):
    graph.nodes[node]["candidate"] = None
    graph.nodes[node]["neighbor_candidates"] = []
    graph.nodes[node]["available_colors"] = colors.copy()
    debug(INIT, f"Initalized node {node} with available colors {colors}")


def select_random_color(graph, node):
    # skip already colored nodes
    if "color" in graph.nodes[node]:
        return

    # select random candidate color from available colors
    assert graph.nodes[node]["available_colors"]
    graph.nodes[node]["candidate"] = random.choice(
        graph.nodes[node]["available_colors"]
    )
    debug(
        SELECT_RANDOM_COLOR,
        f"Node {node} selected candidate color {graph.nodes[node]['candidate']}",
    )


def notify_neighbors(graph, node):
    # skip already colored nodes
    if "color" in graph.nodes[node]:
        return

    # notify (uncolored) neighbors of selected candidate color
    for neighbor in graph.neighbors(node):
        if "color" not in graph.nodes[neighbor]:
            graph.nodes[neighbor]["neighbor_candidates"].append(
                graph.nodes[node]["candidate"]
            )
            debug(NOTIFY_NEIGHBORS_DETAILED, f"Node {node} notified node {neighbor}")
    debug(NOTIFY_NEIGHBORS, f"Node {node} notified neighbors")


def color_or_discard(graph, node):
    # skip already colored nodes
    if "color" in graph.nodes[node]:
        return

    if graph.nodes[node]["candidate"] not in graph.nodes[node]["neighbor_candidates"]:
        # permanently color node
        graph.nodes[node]["color"] = graph.nodes[node]["candidate"]
        debug(
            COLOR,
            f"Node {node} permanently colored with color {graph.nodes[node]['color']}",
        )

        # remove color from available colors of neighbors
        for neighbor in graph.neighbors(node):
            if graph.nodes[node]["color"] in graph.nodes[neighbor]["available_colors"]:
                graph.nodes[neighbor]["available_colors"].remove(
                    graph.nodes[node]["color"]
                )
                debug(
                    REMOVE_FROM_AVAILABLE_COLORS,
                    f"Node {neighbor} removed color {graph.nodes[node]['color']} from available colors",
                )
    else:  # discard candidate color
        debug(
            DISCARD,
            f"Node {node} discarded candidate color {graph.nodes[node]['candidate']}",
        )
        graph.nodes[node]["candidate"] = None
    graph.nodes[node]["neighbor_candidates"] = []


def uncolored_nodes(graph):
    debug(
        UNCOLORED_NODES,
        f"\nUncolored nodes: {[node for node in graph.nodes if 'color' not in graph.nodes[node]]}",
    )
    return [node for node in graph.nodes if "color" not in graph.nodes[node]]


def vertex_coloring(graph, max_degree):
    colors = [i for i in range(max_degree + 1)]
    for node in graph.nodes:
        initialize(graph, node, colors)

    while uncolored_nodes(graph):  # repeat until all nodes are colored
        for node in graph.nodes:  # 1 communication round
            select_random_color(graph, node)
            notify_neighbors(graph, node)

        for node in graph.nodes:  # 1 communication round
            color_or_discard(graph, node)


def basic_example(nodes=300, degree=120):
    # generate random graph
    G = nx.random_regular_graph(degree, nodes)
    debug(GRAPH, "Graph:")
    debug(GRAPH, G.nodes)
    debug(GRAPH, G.edges)

    vertex_coloring(G, degree)
    verify_coloring(G)


def test_cases(tests_per_type=6, disable_debug=True):
    if disable_debug:
        global DEBUG
        DEBUG = False

    graphs = []
    for i in range(tests_per_type):
        graphs.append(
            nx.random_regular_graph(
                random.randint(5, 99),
                random.randint(50, 500) * 2,  # n * d must be even
            )
        )
        graphs.append(
            nx.random_shell_graph(
                [
                    tuple(random.choices(range(1, 100), k=3))
                    for _ in range(random.randint(1, 5))
                ]
            )
        )
        graphs.append(
            nx.random_lobster(
                random.randint(100, 1000), random.uniform(0, 1), random.uniform(0, 1)
            )
        )
        graphs.append(
            nx.dual_barabasi_albert_graph(
                random.randint(100, 1000),
                random.randint(1, 30),
                random.randint(1, 10),
                random.uniform(0, 1),
            )
        )

    print("\nTesting...")
    for graph in graphs:
        vertex_coloring(graph, get_max_degree(graph))
        verify_coloring(graph)
    print("All tests passed")


if __name__ == "__main__":
    basic_example()
    test_cases()
