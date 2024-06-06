# OCR - Adrian Spycher

## Requirements

-   Python 3.6 or higher
-   TensorFlow
-   Keras
-   OpenCV (headless version)
-   Matplotlib
-   Scikit-learn
-   FastAPI
-   Uvicorn

These packages can be installed using the provided `requirements.txt` file.

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Prepare the Dataset

```bash
mkdir assets/numbers && tar -xf assets/numbers_20.tar.xz -C assets/numbers
```

### 4. Train the Neural Network

```bash
python3 neural_network.py
```

### 5. Start the API Server

```bash
uvicorn api:app --reload
```

### 6. Access the API

```
open http://127.0.0.1:8000
```

## Cleanup Instructions

1. Deactivate the virtual environment if it's currently active

```bash
deactivate
```

2. Remove any temporary files or directories generated during the project

```bash
rm -rf .venv __pycache__ assets/numbers
```
