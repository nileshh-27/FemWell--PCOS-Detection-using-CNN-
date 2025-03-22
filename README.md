# 🚀 FemWell - AI-Powered Women's Health Analysis

## 📌 Project Overview
FemWell is an AI-powered web application that assists in analyzing ultrasound images, survey responses, and lab results for women's health diagnostics. It features user authentication, a dashboard for different analysis tools, and a deep learning model for ultrasound image classification.

---

## 🛠️ Features
✅ **User Authentication** - Secure login & registration using MongoDB.  
✅ **Analysis Dashboard** - Access different diagnostic tools.  
✅ **Ultrasound Image Analysis** - AI-powered image classification using TensorFlow.  
✅ **Survey Analysis** - Collect and process personalized survey data.  
✅ **Lab Results Comparison** - Compare hormone levels for accurate diagnosis.  
✅ **Flask Web App** - Seamless web interface with HTML, CSS, and JavaScript.

---

## 🎯 Tech Stack
- **Backend:** Flask, MongoDB
- **Frontend:** HTML, CSS, JavaScript
- **AI Model:** TensorFlow, Keras, OpenCV
- **Database:** MongoDB

---

## 📂 Project Structure
```
FemWell/
│-- static/
│   │-- uploads/         # Uploaded images
│   │-- results/         # Processed images with AI analysis
│   │-- styles/          # CSS styles
│-- templates/
│   │-- login.html       # User login page
│   │-- register.html    # Registration page
│   │-- analysis.html    # Dashboard
│   │-- ultrasound.html  # Ultrasound AI analysis page
│-- app.py               # Main Flask application
│-- bestmodel.h5         # Pre-trained AI model
│-- requirements.txt     # Python dependencies
│-- README.md            # Project documentation
```

---

## 🚀 Installation & Setup
### 🔹 Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/FemWell.git
cd FemWell
```

### 🔹 Step 2: Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 🔹 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 Step 4: Setup MongoDB
1. Install MongoDB and start the server.
2. Create a database called `FemWell`.

### 🔹 Step 5: Run the Application
```bash
python app.py
```
Application will run at: **http://127.0.0.1:5000/**

---

## 📸 Screenshots
### 🔹 **Login & Register**
![Login Page](static/screenshots/login.png)

### 🔹 **Analysis Dashboard**
![Dashboard](static/screenshots/dashboard.png)

### 🔹 **Ultrasound Analysis**
![Ultrasound AI](static/screenshots/ultrasound.png)

---

## 🛠️ API Routes
| Route          | Method | Description |
|---------------|--------|-------------|
| `/`           | GET, POST | User login |
| `/register`   | GET, POST | User registration |
| `/analysis`   | GET | Main dashboard |
| `/survey`     | GET | Survey analysis page |
| `/ultrasound` | GET, POST | Upload & analyze ultrasound images |
| `/lab_results`| GET | View lab results |

---

## 🤖 AI Model Details
- Pre-trained **Deep Learning Model (bestmodel.h5)** using TensorFlow & Keras.
- Accepts ultrasound images (JPG, PNG, JPEG) and classifies them as **Affected / Not Affected**.
- Uses **OpenCV** to mark predictions on the image.

---

## 🌟 Contributing
1. **Fork** the repository.
2. Create a **new branch** (`feature-branch`).
3. **Commit** changes.
4. Push to your **forked repo**.
5. Create a **Pull Request (PR)**.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 📞 Contact
For questions or collaboration, contact:  
📧 **your-email@example.com**  
🔗 [GitHub](https://github.com/your-username)

