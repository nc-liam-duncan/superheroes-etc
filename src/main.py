from fastapi import FastAPI, HTTPException, status
from pg8000.native import DatabaseError
from src.db.connection import connect_to_db, close_db_connection
from src.utils.format_response import format_response
from src.utils.query_makers import make_get_superheroes_query
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class NewSuperhero(BaseModel):
    alias: str
    real_name: str
    is_identity_secret: bool
    image_url: str
    team_id: int


@app.get("/healthcheck")
def get_server_health():
    return {"msg": "server up and running!"}


@app.get("/api/superheroes")
def get_superheroes(is_identity_secret: bool | None = None):
    db = None
    try:
        db = connect_to_db()
        superhero_query = make_get_superheroes_query(is_identity_secret)
        if is_identity_secret is not None:
            superheroes = db.run(
                superhero_query, is_identity_secret=is_identity_secret)
        else:
            superheroes = db.run(superhero_query)
        col_headings = [col["name"] for col in db.columns]
        formatted_superheroes = format_response(superheroes, col_headings)
        return {"superheroes": formatted_superheroes}
    except DatabaseError as de:
        err_code = de.args[0]["C"]
        if err_code == "22P02":
            raise HTTPException(
                status_code=400,
                detail="invalid type for is_identity_secret query"
            )
    finally:
        if db:
            close_db_connection(db)


@app.post("/api/superheroes", status_code=status.HTTP_201_CREATED)
def post_superhero(superhero: NewSuperhero):
    db = None
    try:
        insert_query = "INSERT INTO superheroes \
            (alias, real_name, is_identity_secret, image_url, team_id) \
        VALUES \
            (:alias, :real_name, :is_identity_secret, :image_url, :team_id)\
        RETURNING *"
        db = connect_to_db()
        inserted = db.run(
            insert_query,
            alias=superhero.alias,
            real_name=superhero.real_name,
            is_identity_secret=superhero.is_identity_secret,
            image_url=superhero.image_url,
            team_id=superhero.team_id
        )
        new_superhero = {}
        columns = [col['name'] for col in db.columns]
        # Need to populate new_superhero dict
        for i in range(len(insert_query[0])):
            new_superhero[columns[i]] = inserted[0][i]
        return {"new_superhero": new_superhero}
    finally:
        if db:
            close_db_connection(db)


if __name__ == "__main__":
    uvicorn.run(app="__main__:app", host="localhost", reload=True)
