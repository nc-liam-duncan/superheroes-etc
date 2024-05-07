def make_get_superheroes_query(is_identity_secret: bool | None = None):
    query = "SELECT * FROM superheroes"
    if is_identity_secret is not None:
        query += " WHERE is_identity_secret = :is_identity_secret"
    return query
