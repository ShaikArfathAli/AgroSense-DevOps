import os
from ai_edge_litert.interpreter import Interpreter
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = os.path.join(
    BASE_DIR,
    "models",
    "plant_disease_prediction_model.tflite"
)

interpreter = Interpreter(model_path=model)
interpreter.allocate_tensors()

inp = interpreter.get_input_details()[0]
out = interpreter.get_output_details()[0]

# Create a dummy 224x224 RGB image
x = np.random.rand(1, 224, 224, 3).astype(np.float32)

interpreter.set_tensor(inp["index"], x)
interpreter.invoke()

result = interpreter.get_tensor(out["index"])

print("Prediction shape:", result.shape)
print("Predicted class:", np.argmax(result, axis=1)[0])