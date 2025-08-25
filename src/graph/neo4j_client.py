from typing import List, Dict
from neo4j import GraphDatabase
from src.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Neo4jClient:
    def __init__(self, uri: str = NEO4J_URI, user: str = NEO4J_USER, password: str = NEO4J_PASSWORD):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def init_schema(self):
        cyphers = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Contract) REQUIRE c.id IS UNIQUE",
            "CREATE INDEX IF NOT EXISTS FOR (cl:Clause) ON (cl.label)"
        ]
        with self.driver.session() as s:
            for q in cyphers:
                s.run(q)

    def create_contract_with_clauses(self, contract_id: str, labeled_clauses: List[Dict]):
        with self.driver.session() as s:
            s.run("MERGE (c:Contract {id:$cid})", cid=contract_id)
            for idx, item in enumerate(labeled_clauses):
                s.run(
                    """
                    MATCH (c:Contract {id:$cid})
                    CREATE (cl:Clause {idx:$idx, text:$text, label:$label, score:$score})
                    CREATE (c)-[:HAS_CLAUSE]->(cl)
                    MERGE (cat:Category {name:$label})
                    CREATE (cl)-[:BELONGS_TO]->(cat)
                    """,
                    cid=contract_id, idx=idx, text=item["clause"], label=item["label"], score=item.get("score", 0.0)
                )