from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import pandas as pd

# 1. Definieer de API
app = FastAPI(
    title="Nova Stad Traffic Voorspeller",
    description="API voor het voorspellen van verkeersdrukte o.b.v. weerdata."
)

# 2. Definieer hoe de input data eruit moet zien
class TrafficRequest(BaseModel):
    temp: float
    rain_1h: float
    snow_1h: float
    clouds_all: int
    month: int
    hour: int
    dayofweek: int

# We starten Spark en laden het model zodra de API opstart
spark = SparkSession.builder.master("local[1]").appName("TrafficAPI").getOrCreate()

# LET OP: In de praktijk laad je hier je opgeslagen model in:
# model = PipelineModel.load("../../models/cloud_hybrid/random_forest_model")

@app.get("/")
def home():
    return {"message": "De Nova Stad Traffic API is online! Ga naar /docs voor de interface."}

@app.post("/predict")
def predict_traffic(data: TrafficRequest):
    # Converteer de inkomende JSON request naar een Pandas DataFrame en dan naar Spark
    pdf = pd.DataFrame([data.dict()])
    sdf = spark.createDataFrame(pdf)
    
    # In productie doe je hier: prediction = model.transform(sdf).collect()[0]["prediction"]
    # Voor nu simuleren we een antwoord:
    gesimuleerde_voorspelling = 3500 
    
    return {
        "status": "success",
        "verwachte_verkeersvolume": gesimuleerde_voorspelling,
        "gebruikte_features": data.dict()
    }