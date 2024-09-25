import pandas as pd
import uvicorn
from aiohttp.web_exceptions import HTTPRedirection
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition d'un modèle pour les données d'entrée
db = pd.read_csv('../data/appartements.csv')

# Initialisation du modèle de régression linéaire
model = LinearRegression()

# Variable pour vérifier si le modèle est entraîné
is_model_trained = False

# Endpoint pour entraîner le modèle

global model_note
global model_year
global model_garage

@app.get('/train')
def train_models():
    global is_model_trained
    # j'ai enlevé les villes car ça me faisait une erreur de colonnes
    X_note = pd.get_dummies(db[['surface', 'price']])
    y_note = db['note']
    X_train_note, X_test_note, y_train_note, y_test_note = train_test_split(X_note, y_note, test_size=0.2)

    global model_note
    model_note = LinearRegression()
    model_note.fit(X_train_note, y_train_note)

    # X_year = pd.get_dummies(db[['city']])
    # y_year = db['annee']
    # X_train_year, X_test_year, y_train_year, y_test_year = train_test_split(X_year, y_year, test_size=0.2)
    # global model_year
    # model_year = LinearRegression()
    # model_year.fit(X_train_year, y_train_year)


    X_garage = pd.get_dummies(db[['price']])
    y_garage = db['garage']
    X_train_garage, X_test_garage, y_train_garage, y_test_garage = train_test_split(X_garage, y_garage, test_size=0.2)
    global model_garage
    model_garage = LogisticRegression()
    model_garage.fit(X_train_garage, y_train_garage)

    is_model_trained = True

    return {"message": "Modèles entraînés avec succès."}


class PredictionNoteData(BaseModel):
    surface: float
    # ville: str
    prix: float

@app.post("/predict/note")
async def predict(data: PredictionNoteData):
    global is_model_trained

    # Vérifier si le modèle a été entraîné
    if not is_model_trained:
        raise HTTPException(
            status_code=400, detail="Le modèle n'est pas encore entraîné. Veuillez entraîner le modèle d'abord.")

    global model_note
    predicted_note = model_note.predict([[data.surface, data.prix]])

    return {"note": predicted_note[0]}

# class PredictionYearData(BaseModel):
#     ville: str
#
# @app.post("/predict/annee")
# async def predict(data: PredictionYearData):
#     global is_model_trained
#
#     # Vérifier si le modèle a été entraîné
#     if not is_model_trained:
#         raise HTTPException(
#             status_code=400, detail="Le modèle n'est pas encore entraîné. Veuillez entraîner le modèle d'abord.")
#
#     predicted_year = model_year.predict([[data.ville]])
#
#     return {"annee": predicted_year}

class PredictionGarageData(BaseModel):
    prix: float
    # ville: str -> j'ai jamais pu faire fonctionner un enum de string, ça décalait toute mes colonnes avec le pd.get_dummies

@app.post("/predict/garage")
async def predict(data: PredictionGarageData):
    global is_model_trained
    global model_garage

    # Vérifier si le modèle a été entraîné
    if not is_model_trained:
        raise HTTPException(
            status_code=400, detail="Le modèle n'est pas encore entraîné. Veuillez entraîner le modèle d'abord.")

    predicted_garage = model_garage.predict([[data.prix]])
    # j'ai pas trouvé comment faire pour que le résultat soit un booléen
    has_garage = True if predicted_garage[0] == 1 else False

    return {"garage": has_garage}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)