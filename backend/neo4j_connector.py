from py2neo import Graph
class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.graph = Graph(uri, auth=(user, password))
    def run_query(self, query):
        try:
            results = self.graph.run(query).data()
            return results
        except Exception as e:
            print(f"查询出错：{e}")
            return []