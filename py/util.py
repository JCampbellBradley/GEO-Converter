import re

def encode_commas(s):
	return s.replace(",", "[COMMA]").replace(";", "[SEMICOLON]")

def decode_commas(s):
	return f"replace(replace(replace({s}, ';', '\t'), '[COMMA]', ','), '[SEMICOLON]', ';')"

def reformat_key(s):
	s = s.strip().lower().replace("/", "_slash_")
	s = re.sub("[ .,'\"]", "", s)
	return s