import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, Driver
import pandas as pd
from json import loads, dumps
from tqdm import tqdm

load_dotenv()

URI = "neo4j+s://2fb37773.databases.neo4j.io"
AUTH = (os.getenv("USERNAME"), os.getenv("INSTANCE_PASSWORD"))

index_df = pd.read_csv("BIOGRID-PROJECT-ups_project-GENES-4.4.232.projectindex.txt", sep="\t",)
index_df = index_df.rename(columns={"#BIOGRID ID": "BIOGRID ID"})



def add_gene_to_db(json_string: str, driver: Driver):
    driver.execute_query("CREATE (:Gene $props)", props=loads(json_string))

def add_interaction_to_db(json_string: str, driver: Driver):
    json_object = loads(json_string)
    driver.execute_query(""" MATCH (a:Gene {`BIOGRID ID`: $id_a}), (b:Gene {`BIOGRID ID`: $id_b})
    CREATE (a)-[:INTERACTION $props]->(b), (b)-[:INTERACTION $props]->(a)
    """, props=json_object, id_a=json_object["BioGRID ID Interactor A"], id_b=json_object["BioGRID ID Interactor B"])
    


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    gene_strings: list[str] = index_df.to_json(orient='records', lines=True).splitlines() # returns a list of json strings where each string is a gene entry
    [add_gene_to_db(attributes, driver) for attributes in tqdm(gene_strings, desc="Processesing Genes")]
    for start_row in tqdm(range(403765//3000 + 1), desc="Processing Interactions"):
        interaction_df = pd.read_csv("BIOGRID-PROJECT-ups_project-INTERACTIONS-4.4.232.tab3.txt", sep="\t", skiprows=start_row*3000, nrows=3000)
        interaction_df = interaction_df.rename(columns={"#BioGRID Interaction ID": "BioGRID Interaction ID"})
        interaction_strings: list[str] = interaction_df.to_json(orient='records', lines=True).splitlines() # same as above, but for interactions
        [add_interaction_to_db(attributes, driver) for attributes in tqdm(interaction_strings, desc=f"Interaction group no {start_row} out of {403765//3000 + 1}", leave=False)]
    driver.verify_connectivity()