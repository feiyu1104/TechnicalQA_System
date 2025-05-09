from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "gaoxiaoqiang0"))
print(graph.run("MATCH (n) RETURN n LIMIT 1").data())