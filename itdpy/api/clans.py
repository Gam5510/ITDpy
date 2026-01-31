def get_top_clans(client):
    r = client.get("/api/users/stats/top-clans")
    return r.json()