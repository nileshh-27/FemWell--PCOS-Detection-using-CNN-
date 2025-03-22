import os
import numpy as np
import tensorflow as tf
import cv2
from flask import Flask, request, jsonify, render_template, url_for
from keras.models import load_model
from werkzeug.utils import secure_filename

# Initialize Flask App
app = Flask(__name__)

# Load the trained model
MODEL_PATH = "bestmodel.h5"
model = load_model(MODEL_PATH)

# Define Upload & Result Folders
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

# Allowed file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Function to check file type
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to preprocess image
def preprocess_image(image_path):
    img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# Function to add markings to image
def mark_image(image_path, prediction):
    image = cv2.imread(image_path)
    
    # Define the label based on prediction confidence
    label = "Not Affected" if prediction > 0.5 else "Affected"
    color = (0, 255, 0) if prediction > 0.5 else (0, 0, 255)
    
    # Add text to the image
    cv2.putText(image, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Save marked image
    marked_filename = f"marked_{os.path.basename(image_path)}"
    marked_path = os.path.join(RESULT_FOLDER, marked_filename)
    cv2.imwrite(marked_path, image)

    return marked_path  # Return local path

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Image Prediction Route
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Secure filename and save
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Process image
    input_arr = preprocess_image(file_path)
    pred = model.predict(input_arr)[0][0]
    confidence = float(pred)

    # Mark the ultrasound image
    marked_image_path = mark_image(file_path, pred)

    # Convert local path to a URL path
    marked_image_url = url_for("static", filename=f"results/{os.path.basename(marked_image_path)}", _external=True)

    # Result
    result = "Not Affected" if confidence > 0.5 else "Affected"

    return jsonify({
        "result": result,
        "confidence": confidence,
        "marked_image": marked_image_url
    })

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
