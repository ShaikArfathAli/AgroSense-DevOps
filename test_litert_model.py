from ai_edge_litert.interpreter import Interpreter
import numpy as np
from PIL import Image

model = "/work/models/plant_disease_prediction_model.tflite"
image = "/work/datasets/color/Apple___Apple_scab/00075aa8-d81a-4184-8541-b692b78d398a___FREC_Scab 3335.JPG"

interpreter = Interpreter(model_path=model)
interpreter.allocate_tensors()

inp = interpreter.get_input_details()[0]
out = interpreter.get_output_details()[0]

img = Image.open(image).convert("RGB").resize((224,224))
x = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, 0)

interpreter.set_tensor(inp["index"], x)
interpreter.invoke()

result = interpreter.get_tensor(out["index"])

print("Prediction shape:", result.shape)
print("Predicted class:", np.argmax(result, axis=1)[0])
