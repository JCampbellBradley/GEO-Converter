USAGE:

Fetches files from the GEO database and massages them into a format usable by ONgDB. Both CSV and cypher files are produced, under import/ and cypher/ respectively. The import folder should be copied to the ongdb directory.

python3 py/geo_downloader.py [accession number]: Gets a series family file from the GEO database. This contains related samples and platform info.
python3 py/soft_interpreter.py [soft file]: Converts a soft file into CSV and cypher files, ready to be loaded into ONgDB.

OVERVIEW:

util.py contains some utility functions.
geo_downloader.py is a script to download files from the GEO database.
soft_interpreter.py parses soft files, and loads the data into the objects described below.
geo_*.py store data for each respective dataset (series, sample, platform, as well as some metadata about the GEO database itself), and the superclass geo_dataset.py contains shared code.

POSSIBLE FUTURE WORK:

-perhaps most importantly, importing samples is very slow. There is most likely a way to tweak this to be more efficient (see: https://neo4j.com/docs/getting-started/data-import/csv-import/#optimizing-load-csv).
-cyphers must currently be manually copy pasted into the browser or the geequel interpreter. Being able to load cyphers automatically would be very nice.
-there may or may not be critical formatting issues left (in the form of SOFT keys or characteristics containing illegal characters, like periods or slashes). If encountered, this is usually fixed by a simple modification to util.reformat_key.
-there are some non-critical formatting issues to be solved. The contributors to a series, for example, have their names smashed together with no spaces in between.
-contributors and orther entities are represented as strings, rather than as their own nodes. This may or may not be something we want to fix.
-the interpreter can't pull multiple characteristics from the same line (see the samples from GSE2748)
-Dr. Kirby will likely want this system to be expanded to interpret data from other sources. A good start would be taking the cypher snippets hardcoded into the geo_* files, and finding a way to generate them dynamically.
