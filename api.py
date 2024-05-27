import keras
import numpy as np
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse


# --- MOUNT STATIC FILE ---

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

model = keras.models.load_model('models/model.h5')

def shift_to_top_left(img_bin):
    """
    Shift the non-zero pixels of a binary image to the top-left corner.
    :param img_bin: Binary image (numpy array) with shape (20, 20).
    :return: Binary image with the number shifted to the top-left corner.
    """
    # Find the bounding box of the non-zero regions
    rows = np.any(img_bin, axis=1)
    cols = np.any(img_bin, axis=0)
    
    # Get the start and end coordinates of the bounding box
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # Extract the bounding box from the binary image
    cropped = img_bin[rmin:rmax+1, cmin:cmax+1]
    
    # Create a new binary image with the same shape
    shifted_img = np.zeros_like(img_bin)
    
    # Place the cropped region in the top-left corner of the new image
    shifted_img[0:cropped.shape[0], 0:cropped.shape[1]] = cropped
    
    return shifted_img


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
    img_bin = np.where(grayscale_array < 220, 1, 0)
    shifted_img_bin = shift_to_top_left(img_bin)
    
    # - make prediction -    
    
    try:
        input_data = np.expand_dims(shifted_img_bin, axis=0)
        prediction = model.predict(input_data).tolist()
    
        return JSONResponse(content={"message": "Pixel data received", "prediction": prediction, "number": np.argmax(prediction).tolist()})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)