import urllib.request as ur
from sys import argv
import subprocess
import os.path


def get(accessions):
	for accession in accessions:
		if(accession[:3] != "GSE"):
			raise Exception("Only series (prefixed by 'GSE') are currently supported")
		
		
		if(not os.path.isfile(f"soft/{accession}.soft")):
			accession_thousands = f"{accession[:-3]}nnn"
			local_arch = f"soft/{accession}.soft.gz"
			
			url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{accession_thousands}/{accession}/soft/{accession}_family.soft.gz"
			ur.urlretrieve(url, local_arch)
			
			subprocess.run(["gzip", "-d", local_arch])
	
	
if(__name__ == "__main__"):
	if not os.path.exists("./soft"):
		os.makedirs("./soft")
		
	if(len(argv) < 2):
		raise Exception("Please provide at least one argument (the accession code(s) of the desired SOFT file(s)).")
		
	accessions = argv[1:]
	
	get(accessions)