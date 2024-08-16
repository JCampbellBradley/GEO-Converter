import sys, os
import geo_platform as plat
import geo_series as ser
import geo_sample as sam
import geo_database as dat
import util

class SoftParser:
	SUPPORTED_TYPES = {
		"PLATFORM": "Platform", 
		"SERIES": "Series",
		"SAMPLE": "Sample",
		"DATABASE": "Database",
	}
	
	def __init__(self, filename):
		self.filename = filename
		
		self.line_num = 0
		
		# The root of the filenames to output
		self.curr_id = ""
		
		# The data type in the current part of the file (e.g. platform)
		self.curr_data_type = None
		
		# Metadata of the current dataset
		self.metadata = {}
		
		# Tabular data, if present
		self.table_data = []
		self.col_keys = []
		self.col_labels = {}
		
		# Whether the parser is currently reading tabular data
		self.in_table = False
		self.in_table_header = False
		
	def parse_data(self):
		self.file_id = self.filename[:self.filename.find(".")]
		
		with open(f"cyphers/_{self.file_id}_combined.cql", "w", encoding="utf-8") as f:
			f.write("")
	
		with open(self.filename, "r", encoding="utf-8") as f:
			for line in f:
				self.line_num += 1
				
				s_line = line.strip()
				
				if(s_line[0] == '^'):
					self.parse_header(s_line)
				elif(s_line[0] == '!'):
					self.parse_metadata(s_line)
				elif(s_line[0] == '#'):
					self.parse_label(s_line)
				elif(self.in_table):
					self.parse_row(s_line)
				else:
					raise Exception(f"Could not parse line {self.line_num}: {line}")
					
			self.flush()
					
		
	def parse_header(self, line):
		self.flush()
		
		eq_index = line.find("=")
		
		data_type_raw = line[1:eq_index].strip()
		self.curr_id = line[eq_index + 1:].strip()
		self.metadata["Dataset_search_key"] = [self.curr_id]
					
		if(not data_type_raw in SoftParser.SUPPORTED_TYPES):
			raise Exception(f"Unrecognized data type {data_type}. Supported data types are {', '.join(SUPPORTED_TYPES)}.\nAt line {self.line_num}: {line}")
			
		self.curr_data_type = SoftParser.SUPPORTED_TYPES[data_type_raw]
	
	def parse_metadata(self, line):
		if(line == f"!{self.curr_data_type.lower()}_table_begin"):
			self.in_table = True
			self.in_table_header = True
		elif(line == f"!{self.curr_data_type.lower()}_table_end"):
			self.in_table = False
			self.in_table_header = False
			
		else:
			eq_index = line.find("=")
			full_key = line[1 : eq_index].strip()
			value = line[eq_index + 1 :].strip()
			
			if(full_key in self.metadata):
				self.metadata[full_key] += [util.encode_commas(value)]
			else:
				self.metadata[full_key] = [util.encode_commas(value)]
				
	def parse_label(self, line):
		eq_index = line.find("=")
		
		col_key = line[1:eq_index].strip()
		col_label = line[eq_index+1:].strip()
		
		self.col_labels[col_key] = util.encode_commas(col_label)
		
	def parse_row(self, line):
		if(self.in_table_header):
			self.col_keys = line.split("\t")
			self.in_table_header = False
		else:
			self.table_data += [line.split("\t")]
	
	def flush(self):
		if(self.curr_data_type == "Platform"):
			dataset = plat.GEO_Platform(self.metadata, self.table_data, self.col_keys, self.col_labels)
		elif(self.curr_data_type == "Series"):
			dataset = ser.GEO_Series(self.metadata, self.table_data, self.col_keys, self.col_labels)
		elif(self.curr_data_type == "Sample"):
			dataset = sam.GEO_Sample(self.metadata, self.table_data, self.col_keys, self.col_labels)
		elif(self.curr_data_type == "Database"):
			dataset = dat.GEO_Database(self.metadata, self.table_data, self.col_keys, self.col_labels)
		elif(self.curr_data_type == None):
			return
		
		with open(f"import/{self.curr_id}_metadata.csv", "w", encoding="utf-8") as f:	
			f.write(dataset.make_metadata_csv())
		
		if(dataset.has_table_data()):
			with open(f"import/{self.curr_id}.csv", "w", encoding="utf-8") as f:	
				f.write(dataset.make_table_csv())
		
		cypher = dataset.make_cypher(f"{self.curr_id}_metadata.csv", f"{self.curr_id}.csv")
		
		with open(f"cyphers/{self.curr_id}.cql", "w", encoding="utf-8") as f:	
			f.write(cypher)
			
		with open(f"cyphers/_{self.file_id}_combined.cql", "a", encoding="utf-8") as f:
			f.write(cypher)
			
		self.curr_id = ""
		
		self.curr_data_type = None
		
		self.metadata = {}
		
		self.table_data = []
		self.col_keys = []
		self.col_labels = {}
		
		self.in_table = False
		self.in_table_header = False

if(__name__ == "__main__"):
	if not os.path.exists("./cyphers"):
		os.makedirs("./cyphers")
		
	if not os.path.exists("./import"):
		os.makedirs("./import")
		
	if(len(sys.argv) != 2):
		raise Exception("Syntax: python3 softinterpreter.py [filename]")
	filename = sys.argv[1]
	
	parser = SoftParser(filename)
	parser.parse_data()