import geo_dataset as ds
import util

class GEO_Database(ds.GEO_Dataset):
	# These keys will be ignored.
	KEYS_TO_IGNORE = []
	
	def __init__(self, metadata, table_data, col_keys, col_labels):
		super().__init__(metadata, table_data, col_keys, col_labels)
		
	def make_cypher(self, metadata_path, table_path):
		data_copy = dict(self.metadata)
		
		s = f"""
				CREATE CONSTRAINT ON (ds:Database) ASSERT ds.search_key IS UNIQUE;
				
				LOAD CSV WITH HEADERS FROM 'file:///{metadata_path}' AS row
				MERGE (ds:Database {{search_key: row.search_key }})
				set ds.data_present = True
		"""
		
		s += self.cypher_generic_keys(data_copy)
			
		return s.replace("\t", "")
			