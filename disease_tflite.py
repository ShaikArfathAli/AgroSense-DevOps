import os
import numpy as np
from PIL import Image
from ai_edge_litert.interpreter import Interpreter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "plant_disease_prediction_model.tflite"
)

interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def predict(image_path):
    img = Image.open(image_path).convert("RGB").resize((224, 224))

    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    interpreter.set_tensor(
        input_details[0]["index"],
        img_array
    )

    interpreter.invoke()

    return interpreter.get_tensor(
        output_details[0]["index"]
    )
