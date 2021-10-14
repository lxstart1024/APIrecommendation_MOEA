import pandas as pd
from ge import Node2Vec
import networkx as nx

if __name__ == "__main__":
    G=nx.read_edgelist('E:/APK1Edges.txt', create_using = nx.DiGraph(), nodetype = None, data = [('weight', int)])
    model = Node2Vec(G, walk_length=10, num_walks=80, p=0.25, q=4, workers=1, use_rejection_sampling=0)
    model.train(window_size = 5, iter = 3)
    embeddings=model.get_embeddings()
    valuelist = []
    name = ["Node-embedding"]

    i = 0
    values = embeddings.values()
    for value in values:
        valuelist.append(value)

    test = pd.DataFrame(data=valuelist)
    test.to_csv("E:/APK1GraphEmbedding.csv")