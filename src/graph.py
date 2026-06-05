
import networkx as nx
from pyvis.network import Network

def build_graph(relations):

    G = nx.DiGraph()

    for source, relation, target in relations:

        G.add_node(source)
        G.add_node(target)

        G.add_edge(
            source,
            target,
            title=relation
        )

    net = Network(
        height="750px",
        width="100%",
        directed=True
    )

    net.from_nx(G)

    net.save_graph("templates/graph.html")
