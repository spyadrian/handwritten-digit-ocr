import keras
import numpy as np
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse


# --- MOUNT STATIC FILE ---

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

model = keras.models.load_model('models/model.h5')


# --- ROUTE ---

# - get -

@app.get("/", response_class=HTMLResponse)
def read_index():
    with open("frontend/index.html") as f:
        return f.read()

# - post -

@app.post("/post-canvas")
async def process_canvas(request: Request):
    # - receive data -
    
    data = await request.json()
    pixels = data.get("pixels", [])
    width = data.get("width", 0)
    height = data.get("height", 0)
    
    if not pixels or not width or not height:
        return JSONResponse(content={"message": "Invalid data received"}, status_code=400)
    
    grayscale_array = np.array(pixels, dtype=np.uint8).reshape((height, width))
    
    # - make prediction -    
    
    try:
        input_data = np.expand_dims(grayscale_array, axis=0)
        prediction = model.predict(input_data).tolist()
    
        return JSONResponse(content={"message": "Pixel data received", "prediction": prediction})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)