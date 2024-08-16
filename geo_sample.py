import geo_dataset as ds
import util

class GEO_Sample(ds.GEO_Dataset):
	# These keys will be ignored.
	KEYS_TO_IGNORE = ["sample_id", "series_id"]
	
	def __init__(self, metadata, table_data, col_keys, col_labels):
		# Some sample keys are postpended by '_ch1' to denote the first channel
		# As far as I can tell, no samples have more than one channel, and i have no idea what multiple channels would even entail
		# So we just delete the '_ch1's and move on with our day
		
		if(metadata["Sample_channel_count"][0] != "1"):
			raise Exception(f"Sample {metadata['Dataset_search_key']} has a channel count of {metadata['Sample_channel_count'][0]}, which is not equal to '1'. Fix the script to handle this.")
		
		new_metadata = {}
		for key in metadata:
			if("_ch1" in key):
				new_key = key[:key.find("_ch1")]
				new_metadata[new_key] = metadata[key]
			else:
				new_metadata[key] = metadata[key]
		
		super().__init__(new_metadata, table_data, col_keys, col_labels)
		
		#TODO handle characteristics

		
	def make_cypher(self, metadata_path, table_path):
		data_copy = dict(self.metadata)
		
		s = f"""
				CREATE CONSTRAINT ON (ds:Sample) ASSERT ds.search_key IS UNIQUE;
				
				LOAD CSV WITH HEADERS FROM 'file:///{metadata_path}' AS row
				MERGE (ds:Sample {{search_key: row.search_key }})
				set ds.data_present = True
		"""
		del data_copy["search_key"]
		
		s += f"""
				MERGE (db:Database {{search_key: "GeoMiame"}})
				ON CREATE SET db.data_present = False
				MERGE (ds)-[r:SOURCED_FROM]->(db)
		"""
				
		if("organism" in data_copy):
			s += f"""
					MERGE (s:Species {{name: row.organism}})
					ON CREATE SET s.data_present = False
					MERGE (ds)-[r1:TARGET_ORGANISM]->(s)
			"""
			del data_copy["organism"]
		
		s += self.cypher_generic_keys(data_copy)
		
		# Table data
		col_names_copy = list(self.col_names)
		s += f"""
				
				CREATE CONSTRAINT ON (ft:Platform_Feature) ASSERT ft.search_key IS UNIQUE;
			
				MERGE (ds:Sample {{search_key: '{self.get_search_key()}' }})
				with ds
				LOAD CSV WITH HEADERS FROM 'file:///{table_path}' AS row
				MERGE (ft:Platform_Feature {{search_key: row.id_ref }})
				ON CREATE
				set ft.data_present = False
				MERGE (ds)-[r2:MEASURES]->(ft)
		"""
		col_names_copy.remove("id_ref")
	
		for key in col_names_copy:
			s += f"\nset r2.{key} = " + util.decode_commas(f"row.{key}")		
		
		s += ";"
			
		return s.replace("\t", "")
			