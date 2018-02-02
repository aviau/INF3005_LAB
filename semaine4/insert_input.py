#!/usr/bin/python3

import os
import sqlite3


def get_connection():
    connection = sqlite3.connect('db.sqlite')
    return connection


def read_albums(filepath):
    albums = []

    with open(filepath, "r") as f:
        for line in f:
            artist, title, year = line.strip().split("|")

            albums.append(
                {
                    "artiste": artist,
                    "titre": title,
                    "annee": year,
                }
            )

    return albums


def get_artist_by_name(connection, artist_name):
    cursor = connection.cursor()

    cursor.execute(
        "select "
        "id, nom, est_solo, nombre_individus "
        "from artiste "
        "where nom = ?",
        (
            artist_name,
        ),
    )

    row = cursor.fetchone()

    artist = None

    if row:
        artist = {
            "id": row[0],
            "nom": row[1],
            "est_solo": row[2],
            "nombre_individus": row[3],
        }

    return artist


def create_artist(connection, nom, est_solo, nombre_individus):
    cursor = connection.cursor()

    cursor.execute(
        "insert into artiste "
        "(nom, est_solo, nombre_individus) "
        "VALUES "
        "(?, ?, ?);",
        (
            nom,
            str(est_solo).upper(),
            str(nombre_individus),
        ),
    )
    connection.commit()

    return get_artist_by_name(connection, nom)


def get_or_create_artist(connection, artist_name):
    existing_artist = get_artist_by_name(connection, artist_name)
    if existing_artist:
        return existing_artist

    created_artist = create_artist(
        connection,
        artist_name,
        True,
        1,
    )

    return created_artist


def create_album(connection, album):
    print(
        "Creating album {titre}...".format(
            titre=album["titre"],
        )
    )

    artist = get_or_create_artist(connection, album["artiste"])

    cursor = connection.cursor()

    cursor.execute(
        "insert into album "
        "(titre, annee, artiste_id, maison_disque_id) "
        "VALUES "
        "(?, ?, ?, ?);",
        (
            album["titre"],
            str(album["annee"]),
            str(artist["id"]),
            "1",
        ),
    )
    connection.commit()


def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    input_filepath = os.path.join(current_directory, "input.txt")

    albums = read_albums(input_filepath)

    connection = get_connection()

    for album in albums:
        create_album(connection, album)


if __name__ == "__main__":
    main()
