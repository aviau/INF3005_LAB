#!/usr/bin/python3

import sqlite3


def get_connection():
    connection = sqlite3.connect('db.sqlite')
    return connection


def get_artists(connection):
    cursor = connection.cursor()
    cursor.execute("select id, nom from artiste")

    artists = []
    for row in cursor:
        artists.append(
            {
                "id": row[0],
                "nom": row[1],
            }
        )

    return artists


def print_artists(artists):
    print("Voici la liste des artistes:")
    for artist in artists:
        print(
            "{id}. {nom}".format(
                id=artist["id"],
                nom=artist["nom"],
            )
        )

def get_int_input(message, minval, maxval):
    while True:
        print(message)
        try:
            number = int(input())
            if number >= minval and number <= maxval:
                return number
        except ValueError:
            pass


def get_artist_albums(connection, artist_id):
    cursor = connection.cursor()

    cursor.execute(
        "select "
        "id, titre, annee, artiste_id, maison_disque_id "
        "from album "
        "where artiste_id = ?",
        (
            str(artist_id),
        ),
    )

    albums = []

    for row in cursor:
        albums.append(
            {
                "id": row[0],
                "titre": row[1],
                "annee": row[2],
                "artiste_id": row[3],
                "maison_disque_id": row[4],
            }
        )

    return albums


def print_albums(albums):
    print("Voici la liste des albums:")
    for album in albums:
        print(
            "- {titre} ({annee})".format(
                titre=album["titre"],
                annee=album["annee"],
            )
        )


def main():
    connection = get_connection()

    while True:
        try:
            artists = get_artists(connection)
            print_artists(artists)

            choice = get_int_input(
                "Veuillez choisir un artiste:",
                1,
                len(artists),
            )

            albums = get_artist_albums(connection, choice)
            print_albums(albums)

            print("Entrée pour recommencer. Ctrl-c pour quitter.")
            input()

        except KeyboardInterrupt:
            print("\nfin du programme.")
            break


if __name__ == "__main__":
    main()
