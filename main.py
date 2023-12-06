from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, types
from databases import Database
from sqlalchemy.sql import select
from datetime import date


app = FastAPI() #instancia de la aplicación

USERNAME = 'jumafe2'
PASSWORD = 'isis2503'
NAME_MEW = '10.128.0.4'
NAME_DB = 'citas_db'
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{NAME_MEW}:5432/{NAME_DB}"


metadata=MetaData()
database = Database(DATABASE_URL)


async def startup_db():
    try:
        await database.connect()
        return database
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def shutdown():
    return database.disconnect()

app.add_event_handler("startup", startup_db)
app.add_event_handler("shutdown", shutdown)


citas_table = Table(
    "citas",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('paciente', String(50)),
    Column('medico', String(50)),
    Column('fecha', types.DateTime),
    Column("nota", String(100)),
    
)


@app.get('/')
def message():
    return "Hola mundo!"


@app.get('/citas')
async def getCitas():
    query = select(citas_table)
    citas = await database.fetch_all(query)
    return citas

@app.get('/citas/{}')
def getcitaby(algo):
    pass

#citas/?cualquierCosa como cedula o fecha o doctor que atiende

@app.get('/citas/{}')
def getCitasbysomeshit(someshit):
    #return list(filter(lambda item['someshit'] == stock, products))
    pass