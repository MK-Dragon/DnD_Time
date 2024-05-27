from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Player(BaseModel):
    id: int
    name:str
    hp:int
    initiative:int


players = {
    0: Player(name='Marco', id=0, hp=15, initiative=7),
    1: Player(name='Tatiana', id=1, hp=19, initiative=15),
    2: Player(name='Daniel', id=2, hp=10, initiative=3),
    3: Player(name='Daniela', id=3, hp=17, initiative=16),
}

@app.get("/")
def index():
    return {'players': players}

@app.get("/player/{num}")
def get_player(num):
    print(f'{num = }')
    return players[int(num)]


# Needed for running locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)