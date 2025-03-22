import os
import numpy as np
import tensorflow as tf
import cv2
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

# ✅ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["FemWell"]
collection = db["userdetails"]

# ✅ Load Trained Model for Ultrasound Analysis
MODEL_PATH = "bestmodel.h5"
model = load_model(MODEL_PATH)

# ✅ Define Upload & Result Folders
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

# ✅ Allowed file types for Ultrasound
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# ✅ Function to check file type
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Function to preprocess image
def preprocess_image(image_path):
    img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# ✅ Function to add markings to the image
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

# ✅ Home/Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if user exists
        user = collection.find_one({"username": username})
        
        if user and check_password_hash(user["password"], password):
            flash("Login successful!", "success")
            return redirect(url_for("analysis"))  # Redirect to the Analysis page
        else:
            flash("Invalid username or password.", "error")
    
    return render_template("login.html")

# ✅ Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        if collection.find_one({"username": username}):
            flash("Username already exists. Choose another.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        collection.insert_one({
            "fullname": fullname,
            "email": email,
            "username": username,
            "password": hashed_password
        })

        flash("User registered successfully! You can now log in.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

# ✅ Analysis Dashboard
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

# ✅ Survey Page
@app.route("/survey")
def survey():
    return render_template("surveyform.html")

# ✅ Lab Results Page
@app.route("/lab_results")
def lab_results():
    return render_template("lab_results.html")

# ✅ Ultrasound Analysis Page
@app.route("/ultrasound", methods=["GET", "POST"])
def ultrasound():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded", "error")
            return redirect(url_for("ultrasound"))

        file = request.files["file"]
        if file.filename == "" or not allowed_file(file.filename):
            flash("Invalid file type", "error")
            return redirect(url_for("ultrasound"))

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
        marked_image_url = url_for("static", filename=f"results/{os.path.basename(marked_image_path)}")

        result = "Not Affected" if confidence > 0.5 else "Affected"

        return render_template("ultrasound.html", result=result, confidence=confidence, marked_image=marked_image_url)

    return render_template("ultrasound.html", result=None)

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
