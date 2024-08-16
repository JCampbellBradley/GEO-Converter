import util

class GEO_Dataset:
	NAME_KEYS = ["contributor", "contact_name"]
	DATE_KEYS = ["submission_date", "last_update_date"]
	
	def __init__(self, metadata, table_data, col_keys, col_labels):
		self.metadata = {}
		self.parse_metadata(metadata)
		
		self.table_data = table_data
		#self.col_names = [encode_commas(col_labels[key].strip().lower().replace(" ", "_"))
		#				for key in col_keys if key in col_labels 
		#				else key.lower()]
		self.col_names = [key.lower() for key in col_keys]
	
	def parse_metadata(self, data_dict):
		for key in data_dict:
			short_key = key[key.find('_') + 1:]
			short_key = short_key.replace('/', '_slash_')
			value = data_dict[key]
			
			if(short_key == "relation"):
				for item in value:
					colon_pos = item.find(":")
					
					relation_type = item[:colon_pos].strip().lower().replace(" ", "_")
					new_key = f"{short_key}_{relation_type}"
					item = item[colon_pos+1:].strip()
					
					if(new_key in self.metadata):
						self.metadata[new_key] += [item]
					else:
						self.metadata[new_key] = [item]
						
			elif(short_key in GEO_Dataset.NAME_KEYS):
				#remove the weird formatting of names in the SOFT format
				value = [" ".join([name for name in item.split("[COMMA]") if len(name) > 0]) for item in value]
				self.metadata[short_key] = value
				
			else:
				self.metadata[short_key] = value
			
	def make_metadata_csv(self):
		s = ",".join(self.metadata.keys()) + "\n"
		
		for key in self.metadata:
			s += ";".join(self.metadata[key]) + ","
			
		s = s[:-1]
		
		return s
		
	def make_table_csv(self):
		s = ",".join(self.col_names)
		
		for row in self.table_data:
			s += "\n" + ",".join(row)
			
		return s
		
	def cypher_generic_keys(self, generic_keys):
		s = ""
		for key in generic_keys:
			if(not key in self.KEYS_TO_IGNORE):
				if(key in self.DATE_KEYS):
					#toDate is not implemented in ONGDB

					#s += f"\nset ds.{key} = toDate(row.{key})"
					s += f"\nset ds.{key} = " + util.decode_commas(f"row.{key}")
				else:
					s += f"\nset ds.{key} = " + util.decode_commas(f"row.{key}")
		
		s += ";"
		return s
		
	def has_table_data(self):
		return self.table_data != []
		
	def get_search_key(self):
		return self.metadata['search_key'][0]