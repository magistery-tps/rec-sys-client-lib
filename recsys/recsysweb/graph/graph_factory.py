import networkx as nx


class GraphFactory:
    @staticmethod
    def create_weihted_graph(df, graph_type = nx.Graph(), source='source', target='target', edge_attr='weight'):
        return nx.from_pandas_edgelist(
            df           = df,
            source       = source,
            target       = target,
            edge_attr    = edge_attr,
            create_using = graph_type
        )

    @staticmethod
    def create_undirected_weihted_graph(df):
        return GraphFactory.create_weihted_graph(df, graph_type = nx.Graph())

    @staticmethod
    def create_directed_weihted_graph(df):
        return GraphFactory.create_weihted_graph(df, graph_type = nx.DiGraph())