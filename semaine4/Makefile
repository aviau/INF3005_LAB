
db.sqlite:
	sqlite3 -line db.sqlite '.read musique.sql'


.PHONY: browse-artists
browse-artists: db.sqlite
	./browse_artists.py

.PHONY: clean
clean:
	rm -f db.sqlite
