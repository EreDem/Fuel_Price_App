from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mlp import MLP

app = FastAPI()

nn = MLP(1, 1, 2, 4)
nn.load_weights("mlp_weights.npz")

origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://192.168.0.10:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # wer darf zugreifen
    allow_methods=["*"],       # welche HTTP-Methoden (GET, POST, ...)
    allow_headers=["*"],       # welche Header sind erlaubt
    allow_credentials=True,    # Cookies/Authentifizierung
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/predict")
def predict():
    pred = nn.feed_forward([[15]])
    print(pred)
    return {"prediction": pred.tolist()}