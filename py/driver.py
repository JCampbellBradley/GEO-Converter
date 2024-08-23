from neo4j import GraphDatabase


uri = "bolt://localhost:7474"
with GraphDatabase.driver(uri, auth=("neo4j", "password")) as driver:
	with driver.session() as session:
		result = session.run("MATCH (n) return n;")
		print(result)