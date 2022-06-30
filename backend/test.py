# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import csv


class Stuebi:
    def __init__(self, arg_name, arg_friends):
        self.name = arg_name
        self.friends = arg_friends


def parseStuebi():

    loc_stuebiNames = []
    with open(r"..\test_graph.csv", newline="") as csvfile:

        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        for i, row in enumerate(spamreader):

            if i >= 1:

                loc_name = row[1].strip() + " " + row[0].strip()
                loc_stuebiNames.append(loc_name)
    loc_stuebis = []
    with open(r"..\test_graph.csv", newline="") as csvfile:

        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        for i, row in enumerate(spamreader):

            if i >= 1:

                loc_name = row[1].strip() + " " + row[0].strip()

                loc_friends = []
                for f in [row[4], row[5]]:
                    splitted = f.split(",")
                    for s in splitted:
                        s = s.strip()
                        if s != "":
                            if s in loc_stuebiNames:
                                loc_friends.append(s)
                            else:
                                print("cannot find: ", s, " (", loc_name, ")")

                loc_stuebis.append(Stuebi(loc_name, loc_friends))
    return loc_stuebis


def drawWithMatplots(arg_fromArray, arg_toArray):
    # Build a dataframe with your connections
    df = pd.DataFrame({"from": arg_fromArray, "to": arg_toArray})
    # Build your graph
    G = nx.from_pandas_edgelist(df, "from", "to", create_using=nx.DiGraph())

    # Chart with Custom edges:
    nx.draw(
        G,
        with_labels=True,
        width=1,
        edge_color="skyblue",
        # style="solid",
        arrows=True,
        # font_size=12,
        # node_size=2500,
        node_shape=".",
        # linewidths=2,
        # margins=0.6,
    )
    # nx.draw_networkx_nodes(G, pos=nx.spring_layout(G))
    plt.show()


def drawWithPyvis(arg_stuebis):
    from pyvis.network import Network
    import pandas as pd

    zl_net = Network(
        height="100%",
        width="100%",
    )

    # set the physics layout of the network
    zl_net.force_atlas_2based()

    # zl_net.set_edge_smooth()

    for stuebi in arg_stuebis:
        zl_net.add_node(
            stuebi.name,
            stuebi.name,
            title=stuebi.name,
        )

    for stuebi in arg_stuebis:

        for f in stuebi.friends:
            zl_net.add_edge(stuebi.name, f, value=1)

    # zl_net.show_buttons(filter_=["nodes", "edges", "physics"])
    zl_net.show_buttons(
        filter_=[
            "layout",
            "interaction",
            "manipulation",
            "physics",
            "selection",
            "rendere",
        ]
    )
    # zl_net.set_options()

    options = {
        "interaction": {"navigationButtons": True},
    }

    # zl_net.set_options(options)
    zl_net.options["interaction"]["navigationButtons"] = True
    zl_net.show("zl.html")


stuebis = parseStuebi()

fromArray = []
toArray = []

for s in stuebis:
    if len(s.friends) == 0:
        fromArray.append(s.name)
        toArray.append(s.name)
        # print(s.name)
    for i, friend in enumerate(s.friends):
        fromArray.append(s.name)
        toArray.append(s.friends[i])


drawWithPyvis(stuebis)
# drawWithMatplots(fromArray, toArray)
