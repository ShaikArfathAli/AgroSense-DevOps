import sys

sys.path.insert(0, "/work")

from disease_tflite import predict

image_path = "/work/datasets/color/Apple___Apple_scab/00075aa8-d81a-4184-8541-b692b78d398a___FREC_Scab 3335.JPG"

result = predict(image_path)

print("Prediction shape:", result.shape)
print("Predicted class:", result.argmax(axis=1)[0])
