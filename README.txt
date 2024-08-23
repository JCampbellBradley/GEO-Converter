OVERVIEW:

Fetches files from the GEO database and 

POSSIBLE FUTURE WORK:
-perhaps most importantly, importing samples is very slow. There is most likely a way to tweak this to be more efficient (see: https://neo4j.com/docs/getting-started/data-import/csv-import/#optimizing-load-csv).
-cyphers must currently be manually copy pasted into the browser or the geequel interpreter. Being able to load cyphers automatically would be very nice.
-there may or may not be critical formatting issues left (in the form of SOFT keys or characteristics containing illegal characters, like periods or slashes). If encountered, this is usually fixed by a simple modification to util.reformat_key.
-there are some non-critical formatting issues to be solved. The contributors to a series, for example, have their names smashed together with no spaces in between.
-contributors and orther entities are represented as strings, rather than as their own nodes. This may or may not be something we want to fix.
-the interpreter can't pull multiple characteristics from the same line (see the samples from GSE2748)
-Dr. Kirby will likely want this system to be expanded to interpret data from other sources. A good start would be taking the cypher snippets hardcoded into the geo_* files, and finding a way to generate them dynamically.
