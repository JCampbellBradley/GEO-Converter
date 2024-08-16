def encode_commas(s):
	return s.replace(",", "[COMMA]").replace(";", "[SEMICOLON]")

def decode_commas(s):
	return f"replace(replace(replace({s}, ';', '\t'), '[COMMA]', ','), '[SEMICOLON]', ';')"
