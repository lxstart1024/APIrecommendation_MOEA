import pandas as pd
import numpy as np

from ge.classify import read_node_label, Classifier
from ge import Node2Vec
from sklearn.linear_model import LogisticRegression

import matplotlib.pyplot as plt
import networkx as nx
from sklearn.manifold import TSNE

if __name__ == "__main__":
    G=nx.read_edgelist('E:/paper2/data/callgraph/Photo/BeautyPlusEdges.txt',
                         create_using = nx.DiGraph(), nodetype = None, data = [('weight', int)])
    model = Node2Vec(G, walk_length=50, num_walks=80,
                     p=0.25, q=4, workers=1, use_rejection_sampling=0) #原参数 G, walk_length=10, num_walks=80,p=0.25, q=4, workers=1, use_rejection_sampling=0
    model.train(window_size = 10, iter = 3) #原参数 window_size = 5, iter = 3
    embeddings=model.get_embeddings()
    valuelist = []
    name = ["Node-embedding"]
    i = 0
    values = embeddings.values()
    for value in values:
        valuelist.append(value)
    # for j in range(len(valuelist)):
    #     print(valuelist[j])
    test = pd.DataFrame(data=valuelist)
    test.to_csv("E:/paper2/data/callgraph/Photo/BeautyPlusGraphEmbedding_re_re(node2vec).csv")