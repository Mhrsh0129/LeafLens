# 🍃 LeafLens 

**A Trademark of @Maharsh Doshi**

[![React Native](https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactnative.dev/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

---

## 📖 Overview

**LeafLens** is a state-of-the-art, end-to-end Machine Learning solution designed to classify plant and leaf diseases automatically. Equipped with a high-accuracy deep learning model, a modern **FastAPI** backend, an elegant **React** web application, and a **React Native** mobile app, LeafLens empowers farmers, gardeners, and plant enthusiasts to instantly diagnose plant health from a single photo.

Proudly created by **@Maharsh Doshi**.

---

## ✨ Key Features

- **🧠 Accurate ML Model**: Diagnoses leaf health (e.g., Early Blight, Late Blight, or Healthy) with high precision using Convolutional Neural Networks.
- **⚡ Fast Backend**: Developed with FastAPI and integrated with TensorFlow Serving for scalable inference.
- **🌐 Beautiful Web App**: A user-friendly React web interface for seamless drag-and-drop diagnostic testing.
- **📱 Mobile Ready**: A React Native application for iOS and Android—snap a photo and get results instantly!
- **☁️ Cloud Deployment**: Ready-to-deploy configurations for Google Cloud Platform (GCP) using TF Lite or full models.

---

## 🛠️ Setup Instructions

### 1. Python API Setup

Prerequisites: Python 3.x, TensorFlow Serving.

```bash
# 1. Install dependencies
pip install -r training/requirements.txt
pip install -r api/requirements.txt

# 2. Run the FastAPI server locally
cd api
uvicorn main:app --reload --host 0.0.0.0
```

### 2. Web App (React) Setup

Prerequisites: Node.js, NPM.

```bash
# 1. Go to the frontend directory
cd frontend

# 2. Install packages
npm install --from-lock-json

# 3. Setup Environment Variables
cp .env.example .env
# Update the API URL in .env if needed

# 4. Start the application
npm start
```

### 3. Mobile App (React Native) Setup

Prerequisites: React Native CLI environment.

```bash
# 1. Navigate to the mobile app directory
cd mobile-app

# 2. Install packages
yarn install

# 3. (macOS only) Install iOS pods
cd ios && pod install && cd ..

# 4. Setup Environment Variables
cp .env.example .env
# Update the API URL in .env if needed

# 5. Run the app!
npm run android   # For Android
npm run ios       # For iOS
```

---

## 🧠 Model Training

The model was trained on thousands of plant leaf images to effectively separate healthy leaves from diseased ones.

1. Open `training/potato-disease-training.ipynb` in a Jupyter Notebook environment.
2. Ensure you have your dataset downloaded and unzipped.
3. Update the dataset directory inside the notebook.
4. Run the cells iteratively to produce a new `.h5` model.

---

## ☁️ Cloud Deployment (GCP)

To deploy the solution to Google Cloud Computing (GCP Cloud Functions):

1. **Upload your model** (`potatoes.h5` or `potato-model.tflite`) to a GCP Storage Bucket.
2. Edit `gcp/main.py` or `gcp/extra/main_with_tf_lite.py` to target your `leaflens-tf-models` bucket.
3. Authenticate with GCP CLI:
   ```bash
   gcloud auth login
   ```
4. Deploy to Cloud Functions:
   ```bash
   cd gcp
   gcloud functions deploy predict --runtime python38 --trigger-http --memory 512 --project your_project_id
   ```

---

## 🏆 Trademark

**LeafLens** is a trademark of **@Maharsh Doshi**. All previous branding has been removed entirely.
