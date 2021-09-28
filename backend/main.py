from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
import motor.motor_asyncio

# db credentials et url
mongo = {}
mongo['usr'] = "root"
mongo['pwd'] = "secret"
mongo['url'] = "mongo"
MONGODB_URI=f"mongodb://{mongo['usr']}:{mongo['pwd']}@{mongo['url']}/demodb?authSource=admin"

# db  connexion 
print(MONGODB_URI)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client.demodb



app = FastAPI()

@app.get('/')
def index():
    return HTMLResponse('Hello, World')

compteur = 0
@app.get('/testdb')
async def insert_one():
    global compteur
    new_record = {"key1": compteur}
    compteur = compteur + 1
    new_record = await db['simpletable'].insert_one(jsonable_encoder(new_record))
    new_record = await db["simpletable"].find_one({"_id": new_record.inserted_id})
    return  HTMLResponse(content=str(new_record))
