from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mlp import MLP

app = FastAPI()

# load the pre-trained model
nn = MLP(1, 1, 2, 4)
nn.load_weights("mlp_weights.npz")

# allowed origins for CORS
origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://192.168.0.10:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_methods=["*"],
    allow_headers=["*"],       
    allow_credentials=True,    
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# request for fuel price prediction
@app.get("/predict")
def predict(fuel_station: str, fuel_type: str, time_frame: str):
    return {"fuel_station": fuel_station, "fuel_type": fuel_type, "time_frame": time_frame}