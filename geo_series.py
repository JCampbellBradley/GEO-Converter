import geo_dataset as ds
import util

class GEO_Series(ds.GEO_Dataset):
	# These keys will be ignored.
	KEYS_TO_IGNORE = []
	
	def __init__(self, metadata, table_data, col_keys, col_labels):
		super().__init__(metadata, table_data, col_keys, col_labels)
		
	def make_cypher(self, metadata_path, table_path):
		data_copy = dict(self.metadata)
		
		s = f"""
				CREATE CONSTRAINT ON (ds:Series) ASSERT ds.search_key IS UNIQUE;
				
				LOAD CSV WITH HEADERS FROM 'file:///{metadata_path}' AS row
				MERGE (ds:Series {{search_key: row.search_key }})
				set ds.data_present = True
		"""
		del data_copy["search_key"]
		
		s += f"""
				MERGE (db:Database {{search_key: "GeoMiame"}})
				ON CREATE SET db.data_present = False
				MERGE (ds)-[r:SOURCED_FROM]->(db)
		"""
		
		if("sample_id" in data_copy):
			
			
			s += f"""
					WITH ds, row
					UNWIND split(row.sample_id, ';') AS sm_id
					MERGE (sm:Sample {{search_key: {util.decode_commas('sm_id')} }})
					ON CREATE SET sm.data_present = False
					MERGE (ds)-[r1:CONTAINS_SAMPLE]->(sm)
			"""
			del data_copy["sample_id"]
		
		s += self.cypher_generic_keys(data_copy)
		
		return s.replace("\t", "")
			