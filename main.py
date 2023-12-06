from fastapi import FastAPI


app = FastAPI() #instancia de la aplicación

@app.get('/')
def message():
    return "Hola mundo!"


@app.get('/citas')
def getCitas():
    pass

@app.get('/citas/{}')
def getcitaby(algo):
    pass