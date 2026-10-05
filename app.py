# from flask import Flask, request, render_template, url_for
# import pickle
# import numpy as np
# import os
# from werkzeug.utils import secure_filename
# from PIL import Image
# import tensorflow as tf

# app = Flask(__name__, template_folder='templates', static_folder='static')

# # Load Models
# crop_recommendation_model = pickle.load(open('models/model.pkl', 'rb'))
# disease_model = tf.keras.models.load_model('models/plant_disease_prediction_model.h5')
# scaler = pickle.load(open('models/minmaxscaler.pkl', 'rb'))

# # Fertilizer suggestion function
# from fertilizer.fertilizer_sugg import suggest_fertilizer

# # Allowed image extensions
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # ----------- HOME PAGE -----------
# @app.route('/')
# def home():
#     return render_template('home.html')

# # ----------- ABOUT PAGE -----------
# @app.route('/about')        
# def about():
#     return render_template('about.html')

# # ----------- FEATURES PAGE -----------
# @app.route('/features')
# def features():
#     return render_template('features.html')

# # ----------- CROP RECOMMENDATION -----------  
# @app.route('/crop', methods=['GET', 'POST'])
# def crop():
#     if request.method == 'POST':
#         try:
#             N = float(request.form['nitrogen'])
#             P = float(request.form['phosphorous'])
#             K = float(request.form['potassium'])
#             temp = float(request.form['temperature'])
#             humidity = float(request.form['humidity'])
#             ph = float(request.form['ph'])
#             rainfall = float(request.form['rainfall'])

#             # Prepare and scale input
#             input_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
#             scaled_input = scaler.transform(input_data)

#             # Make prediction
#             prediction = crop_recommendation_model.predict(scaled_input)[0]

#             # Optional: reverse map integer label to crop name
#             crop_dict = {
#                 1: 'rice', 2: 'maize', 3: 'chickpea', 4: 'kidneybeans', 5: 'pigeonpeas',
#                 6: 'mothbeans', 7: 'mungbean', 8: 'blackgram', 9: 'lentil', 10: 'pomegranate',
#                 11: 'banana', 12: 'mango', 13: 'grapes', 14: 'watermelon', 15: 'muskmelon',
#                 16: 'apple', 17: 'orange', 18: 'papaya', 19: 'coconut', 20: 'cotton',
#                 21: 'jute', 22: 'coffee'
#             }
#             predicted_crop = crop_dict.get(prediction, "Unknown")

#             return render_template('crop_rec_page.html', prediction=predicted_crop,
#                                    N=N, P=P, K=K, temp=temp, humidity=humidity, ph=ph, rainfall=rainfall)

#         except Exception as e:
#             return render_template('crop_rec_page.html', error=str(e),
#                                    N=request.form.get('nitrogen'), P=request.form.get('phosphorous'), K=request.form.get('potassium'),
#                                    temp=request.form.get('temperature'), humidity=request.form.get('humidity'),
#                                    ph=request.form.get('ph'), rainfall=request.form.get('rainfall'))

#     return render_template('crop_rec_page.html')

# # ----------- FERTILIZER SUGGESTION -----------
# @app.route('/fertilizer', methods=['GET', 'POST'])
# def fertilizer():
#     if request.method == 'POST':
#         try:
#             # Get the form inputs
#             crop_name = request.form['cropname'].strip()
#             N = request.form['nitrogen']
#             P = request.form['phosphorous']
#             K = request.form['potassium']
            
#             # Validate form data
#             if not crop_name:
#                 raise ValueError("Crop name is required.")
#             if not N.isdigit() or not P.isdigit() or not K.isdigit():
#                 raise ValueError("Please enter valid numeric values for nitrogen, phosphorous, and potassium.")
            
#             # Convert values to integers
#             N = int(N)
#             P = int(P)
#             K = int(K)

#             # Call the fertilizer suggestion function
#             result = suggest_fertilizer(crop_name, N, P, K)
            
#             # Return the result and passed form data back to the template
#             return render_template('fertilizer_sugg_page.html', result=result, cropname=crop_name, nitrogen=N, phosphorous=P, potassium=K)

#         except ValueError as e:
#             # Catch and display value errors (e.g., missing fields, invalid data)
#             return render_template('fertilizer_sugg_page.html', error=str(e), cropname=crop_name, nitrogen=N, phosphorous=P, potassium=K)

#         except Exception as e:
#             # Catch any other exceptions and show a generic error message
#             return render_template('fertilizer_sugg_page.html', error="An error occurred. Please try again later.", cropname=crop_name, nitrogen=N, phosphorous=P, potassium=K)

#     return render_template('fertilizer_sugg_page.html')


# # ----------- PLANT DISEASE DETECTION -----------
# @app.route('/disease', methods=['GET', 'POST'])
# def disease():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             return "No file part"
        
#         file = request.files['image']
#         if file and allowed_file(file.filename):
#             try:
#                 # Secure the filename
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join('static', 'uploads', filename)  # Save to 'static/uploads'

#                 # Ensure 'static/uploads' exists
#                 if not os.path.exists(os.path.dirname(filepath)):
#                     os.makedirs(os.path.dirname(filepath))
                
#                 file.save(filepath)

#                 # Preprocess image
#                 img = Image.open(filepath).resize((224, 224))  # Adjust the size as per your model input
#                 img_array = tf.keras.utils.img_to_array(img)
#                 img_array = tf.expand_dims(img_array, 0) / 255.0  # Normalize the image

#                 # Make prediction
#                 prediction = disease_model.predict(img_array)
#                 predicted_class = np.argmax(prediction, axis=1)[0]

#                 # Your class names (ensure this list is correct)
#                 class_names = [
#                     'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
#                     'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
#                     'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
#                     'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
#                     'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)',
#                     'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
#                     'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy',
#                     'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
#                     'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
#                     'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
#                     'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
#                 ]
#                 result = class_names[predicted_class]

#                 # Return the image path along with prediction result
#                 return render_template('plant_disease_page.html', result=result, image_url=f'uploads/{filename}')
#             except Exception as e:
#                 return f"Error: {str(e)}"
#         else:
#             return "Invalid file format"
#     return render_template('plant_disease_page.html')

# # ----------- RUN APP -----------
# if __name__ == '__main__':
#     if not os.path.exists('uploads'):
#         os.makedirs('uploads')
#     app.run(host="0.0.0.0", port=5000, debug=False)


from flask import Flask, request, render_template, url_for
import pickle
import numpy as np
import os
from werkzeug.utils import secure_filename
from PIL import Image
from disease_tflite import predict as predict_disease

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load Models
crop_recommendation_model = pickle.load(open('models/model.pkl', 'rb'))
scaler = pickle.load(open('models/minmaxscaler.pkl', 'rb'))

# Fertilizer suggestion function
from fertilizer.fertilizer_sugg import suggest_fertilizer

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ----------- HOME PAGE -----------
@app.route('/')
def home():
    return render_template('home.html')


# ----------- ABOUT PAGE -----------
@app.route('/about')
def about():
    return render_template('about.html')


# ----------- FEATURES PAGE -----------
@app.route('/features')
def features():
    return render_template('features.html')


# ----------- CROP RECOMMENDATION -----------
@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        try:
            N = float(request.form['nitrogen'])
            P = float(request.form['phosphorous'])
            K = float(request.form['potassium'])
            temp = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])

            # Prepare and scale input
            input_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
            scaled_input = scaler.transform(input_data)

            # Make prediction
            prediction = crop_recommendation_model.predict(scaled_input)[0]

            # Optional: reverse map integer label to crop name
            crop_dict = {
                1: 'rice',
                2: 'maize',
                3: 'chickpea',
                4: 'kidneybeans',
                5: 'pigeonpeas',
                6: 'mothbeans',
                7: 'mungbean',
                8: 'blackgram',
                9: 'lentil',
                10: 'pomegranate',
                11: 'banana',
                12: 'mango',
                13: 'grapes',
                14: 'watermelon',
                15: 'muskmelon',
                16: 'apple',
                17: 'orange',
                18: 'papaya',
                19: 'coconut',
                20: 'cotton',
                21: 'jute',
                22: 'coffee'
            }

            predicted_crop = crop_dict.get(prediction, "Unknown")

            return render_template(
                'crop_rec_page.html',
                prediction=predicted_crop,
                N=N,
                P=P,
                K=K,
                temp=temp,
                humidity=humidity,
                ph=ph,
                rainfall=rainfall
            )

        except Exception as e:
            return render_template(
                'crop_rec_page.html',
                error=str(e),
                N=request.form.get('nitrogen'),
                P=request.form.get('phosphorous'),
                K=request.form.get('potassium'),
                temp=request.form.get('temperature'),
                humidity=request.form.get('humidity'),
                ph=request.form.get('ph'),
                rainfall=request.form.get('rainfall')
            )

    return render_template('crop_rec_page.html')


# ----------- FERTILIZER SUGGESTION -----------
@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    if request.method == 'POST':
        try:
            # Get the form inputs
            crop_name = request.form['cropname'].strip()
            N = request.form['nitrogen']
            P = request.form['phosphorous']
            K = request.form['potassium']

            # Validate form data
            if not crop_name:
                raise ValueError("Crop name is required.")

            if not N.isdigit() or not P.isdigit() or not K.isdigit():
                raise ValueError(
                    "Please enter valid numeric values for nitrogen, phosphorous, and potassium."
                )

            # Convert values to integers
            N = int(N)
            P = int(P)
            K = int(K)

            # Call the fertilizer suggestion function
            result = suggest_fertilizer(crop_name, N, P, K)

            # Return the result and passed form data back to the template
            return render_template(
                'fertilizer_sugg_page.html',
                result=result,
                cropname=crop_name,
                nitrogen=N,
                phosphorous=P,
                potassium=K
            )

        except ValueError as e:
            return render_template(
                'fertilizer_sugg_page.html',
                error=str(e),
                cropname=crop_name,
                nitrogen=N,
                phosphorous=P,
                potassium=K
            )

        except Exception as e:
            return render_template(
                'fertilizer_sugg_page.html',
                error="An error occurred. Please try again later.",
                cropname=crop_name,
                nitrogen=N,
                phosphorous=P,
                potassium=K
            )

    return render_template('fertilizer_sugg_page.html')


# ----------- PLANT DISEASE DETECTION -----------
@app.route('/disease', methods=['GET', 'POST'])
def disease():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part"

        file = request.files['image']

        if file and allowed_file(file.filename):
            try:
                # Secure the filename
                filename = secure_filename(file.filename)

                filepath = os.path.join(
                    'static',
                    'uploads',
                    filename
                )

                # Ensure 'static/uploads' exists
                if not os.path.exists(os.path.dirname(filepath)):
                    os.makedirs(os.path.dirname(filepath))

                file.save(filepath)

                # Make prediction using TFLite + LiteRT
                prediction = predict_disease(filepath)

                predicted_class = np.argmax(
                    prediction,
                    axis=1
                )[0]

                # Class names
                class_names = [
                    'Apple___Apple_scab',
                    'Apple___Black_rot',
                    'Apple___Cedar_apple_rust',
                    'Apple___healthy',
                    'Blueberry___healthy',
                    'Cherry_(including_sour)___Powdery_mildew',
                    'Cherry_(including_sour)___healthy',
                    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                    'Corn_(maize)___Common_rust_',
                    'Corn_(maize)___Northern_Leaf_Blight',
                    'Corn_(maize)___healthy',
                    'Grape___Black_rot',
                    'Grape___Esca_(Black_Measles)',
                    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                    'Grape___healthy',
                    'Orange___Haunglongbing_(Citrus_greening)',
                    'Peach___Bacterial_spot',
                    'Peach___healthy',
                    'Pepper,_bell___Bacterial_spot',
                    'Pepper,_bell___healthy',
                    'Potato___Early_blight',
                    'Potato___Late_blight',
                    'Potato___healthy',
                    'Raspberry___healthy',
                    'Soybean___healthy',
                    'Squash___Powdery_mildew',
                    'Strawberry___Leaf_scorch',
                    'Strawberry___healthy',
                    'Tomato___Bacterial_spot',
                    'Tomato___Early_blight',
                    'Tomato___Late_blight',
                    'Tomato___Leaf_Mold',
                    'Tomato___Septoria_leaf_spot',
                    'Tomato___Spider_mites Two-spotted_spider_mite',
                    'Tomato___Target_Spot',
                    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                    'Tomato___Tomato_mosaic_virus',
                    'Tomato___healthy'
                ]

                result = class_names[predicted_class]

                # Return the image path along with prediction result
                return render_template(
                    'plant_disease_page.html',
                    result=result,
                    image_url=f'uploads/{filename}'
                )

            except Exception as e:
                return f"Error: {str(e)}"

        else:
            return "Invalid file format"

    return render_template('plant_disease_page.html')


# ----------- RUN APP -----------
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )