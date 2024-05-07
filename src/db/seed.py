import pg8000.native
from pprint import pprint
import json
from src.db.connection import connect_to_db, close_db_connection
from src.db.config import database, TESTING
from src.utils.create_ref import create_ref


def seed(teams_data, superheroes_data):
    db = connect_to_db()
    # drop tables
    db.run("DROP TABLE IF EXISTS superheroes;")
    db.run("DROP TABLE IF EXISTS teams;")
    # create tables
    db.run("""
    CREATE TABLE teams (
        team_id SERIAL PRIMARY KEY,
        team_name VARCHAR(100),
        formation_year INT
    );
    """)
    db.run("""
    CREATE TABLE superheroes (
        superhero_id SERIAL PRIMARY KEY,
        alias VARCHAR(100),
        real_name VARCHAR(100),
        is_identity_secret BOOLEAN,
        image_url VARCHAR(500),
        team_id INT REFERENCES teams(team_id)
    );
    """)

    for team in teams_data:
        db.run("""
                INSERT INTO teams
                    (team_name, formation_year)
                VALUES
                    (:team_name, :formation_year);
                    """,
               team_name=team["team_name"],
               formation_year=team["formation_year"]
               )

    # create reference object to format team names -> team IDs
    inserted_teams = db.run("SELECT * FROM teams;")
    id_index = 0
    name_index = 1
    team_name_id_ref = create_ref(inserted_teams, name_index, id_index)

    for hero in superheroes_data:
        db.run("""
                INSERT INTO superheroes
                    (alias, real_name, is_identity_secret, image_url, team_id)
                VALUES
                    (:alias, :real_name, :is_identity_secret, :image_url, :team_id);
                    """,
               alias=hero["alias"],
               real_name=hero["real_name"],
               is_identity_secret=hero["is_identity_secret"],
               image_url=hero["image_url"],
               team_id=team_name_id_ref[hero["team"]],
               )

    pprint(f"Seeding complete for database: {database}")

    close_db_connection(db)


if __name__ == "__main__":
    # set correct test/development data file path
    if TESTING:
        data_dir = "src/data/test"
    else:
        data_dir = "src/data/dev"
    try:
        # get teams_data
        with open(f"{data_dir}/teams.json", "r", encoding="utf-8") as file:
            teams_data = json.load(file)

        # get superheroes data
        with open(f"{data_dir}/superheroes.json", "r", encoding="utf-8") as file:
            superheroes_data = json.load(file)
        # RUN SEED
        seed(teams_data, superheroes_data)
    except BaseException as e:
        print("SOMETHING BAD -->", e)
