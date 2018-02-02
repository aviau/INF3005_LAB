db.sqlite:
	sqlite3 -line db.sqlite '.read musique.sql'

.PHONY: browse-artists
browse-artists: db.sqlite
	./browse_artists.py

.PHONY: insert-input
insert-input: db.sqlite
	./insert_input.py

.PHONY: clean
clean:
	rm -f db.sqlite
