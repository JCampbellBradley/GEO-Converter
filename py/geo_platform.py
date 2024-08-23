import geo_dataset as ds
import util

class GEO_Platform(ds.GEO_Dataset):
	# These keys will be ignored.
	KEYS_TO_IGNORE = ["sample_id", "series_id"]
	
	def __init__(self, metadata, table_data, col_keys, col_labels):
		super().__init__(metadata, table_data, col_keys, col_labels)
		
	def make_cypher(self, metadata_path, table_path):
		data_copy = dict(self.metadata)
		
		s = f"""
				CREATE CONSTRAINT ON (ds:Platform) ASSERT ds.search_key IS UNIQUE;
				
				LOAD CSV WITH HEADERS FROM 'file:///{metadata_path}' AS row
				MERGE (ds:Platform {{search_key: row.search_key }})
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
		
		if("relation_alternative_to" in data_copy):
			
			
			s += f"""
					WITH ds, row
					UNWIND split(row.relation_alternative_to, ';') AS acc
					MERGE (alt:Platform {{search_key: acc}})
					ON CREATE SET alt.data_present = False
					MERGE (alt)-[r2:ALTERNATIVE]->(ds)
			"""
			del data_copy["relation_alternative_to"]
		
		s += self.cypher_generic_keys(data_copy)
		
		# Table data
		col_names_copy = list(self.col_names)
		s += f"""
				CREATE CONSTRAINT ON (ft:Platform_Feature) ASSERT ft.search_key IS UNIQUE;
				CREATE CONSTRAINT ON (g:Gene) ASSERT g.search_key IS UNIQUE;
			
				LOAD CSV WITH HEADERS FROM 'file:///{table_path}' AS row
				MERGE (ft:Platform_Feature {{search_key: row.id }})
				ON CREATE
				SET ft.spot_id = {util.decode_commas('row.spot_id')}
				SET ft.id = {util.decode_commas('row.id')}
				MERGE (ds:Platform {{search_key: '{self.get_search_key()}' }})
				MERGE (ds)-[r3:HAS_FEATURE]->(ft)
				set ft.data_present = True
				;
		"""
		col_names_copy.remove("id")
		if("id" in col_names_copy):
			col_names_copy.remove("spot_id")
		
		if("gene_symbol" in self.col_names):
			s += f"""
					LOAD CSV WITH HEADERS FROM 'file:///{table_path}' AS row
					WITH row WHERE row.gene_symbol IS NOT NULL
					MERGE (ft:Platform_Feature {{search_key: row.id }})
					MERGE (g:Gene {{search_key: row.gene_symbol }})
					ON CREATE
			"""
			
			for key in col_names_copy:
				s += f"\nset g.{key} = " + util.decode_commas(f"row.{key}")
					
			
			s += f"""
					MERGE (ft)-[r2:CORRESPONDS_TO]->(g)
					set g.data_present = True
			"""
		
			s += ";"
			
		return s.replace("\t", "")
			