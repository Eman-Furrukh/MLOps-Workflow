# 🚀 MLOps Project: Scalable Machine Learning Deployment for Innovate Analytics Inc.

Welcome to our final semester project! This repository contains the complete MLOps pipeline for building, training, and deploying a scalable machine learning application, following industry-grade practices using CI/CD, containerization, orchestration, and data versioning.

---

## 👨‍👩‍👧‍👦 Team Members

|      Name      |                        Role                      |
|----------------|--------------------------------------------------|
| Eman-Furrukh   | GitHub Management & CI/CD, Airflow, DVC          |
| shamail-123    | Dockerization, MLFlow                            |
| mahrukh272004  | Kubernetes Deployment & Monitoring, Jenkins      |

---

## 📁 Repository Structure
```bash
mlops-project/
├── .github/workflows/ # GitHub Actions CI
├── docker/ # Dockerfile and compose
├── jenkins/ # Jenkins pipeline config
├── k8s/ # Kubernetes deployment files
├── src/ # ML application source code
├── tests/ # Unit tests
├── data/ # Raw & processed data
├── docs/ # Sprint logs & architecture diagram
├── dvc.yaml # DVC pipeline config
├── requirements.txt # Python dependencies
├── README.md # This file
└── .gitignore # Ignored files & directories
```

---

## ⚙️ Technologies Used

- **Python 3.9**
- **Flask / FastAPI**
- **Airflow**
- **GitHub Actions**
- **Docker & DockerHub**
- **Jenkins**
- **Kubernetes (Minikube)**
- **DVC (Data Version Control)**
- **MLflow (for experiment tracking)**

---

## 🔁 Workflow Overview

1. **Plan and collaborate** via GitHub Projects and Issues
2. **Develop** features using Git branching and PRs
3. **Version** data with DVC
4. **Train and track** ML models using MLflow
5. **Automate CI/CD** using GitHub Actions + Jenkins
6. **Containerize** with Docker
7. **Deploy** on Minikube using Kubernetes

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/mlops-project.git
cd mlops-project
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app locally
```bash
python src/app.py
```

---

## 🧪 Running Tests
```bash
pytest tests/
```

---

## 🐳 Build and Run with Docker
```bash
docker build -t mlops-app:latest .
docker run -p 5000:5000 mlops-app
```

---

## 🔁 Jenkins CI/CD (Local or EC2)
Jenkinsfile is located in jenkins/Jenkinsfile
Configure your GitHub webhook and DockerHub credentials
Set up the pipeline to trigger on push

---

## ☸️ Kubernetes Deployment (Minikube)
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service mlops-service
```

---

## 📊 Experiment Tracking with MLflow
```bash
mlflow ui --port 5001
```
View at http://localhost:5001

---

## 📦 Data Versioning with DVC
```bash
dvc init
dvc add data/raw/collect_data.csv
git add data/.gitignore collect_data.csv.dvc
git commit -m "Add versioned dataset"
```

##Test casses

| Test Case | Description | Verification Points |
|-----------|-------------|---------------------|
| Test Case 1 | Verifies that `fetch_weather()` returns valid data with correct types and structure 
| Test Case 2 | Tests that `write_to_csv()` correctly creates files and writes data
| Test Case 3 | Validates that preprocessing creates the expected features and handles different weather conditions 
|Test Case 4 | Checks that model training creates a valid model file 
| Test Case 5 | Verifies that the trained model can make predictions 
| Bonus Test Case| Tests error handling for empty data and failed API calls 


##Flake8 Linting Workflow
Trigger: Runs on every pull request to the dev branch

Environment: Ubuntu with Python 3.9

Key Steps:

Checks out repository code

Sets up Python environment

Installs Flake8 and project dependencies

Runs two Flake8 checks:

Critical errors only (E9,F63,F7,F82)

Full style check with 100-character line length limit

Purpose: Enforces consistent Python code style and catches syntax errors before merging


##Test Execution Workflow
Purpose: Automatically runs test cases on Python code changes

Trigger Conditions:

On every pull request to the test branch

On every direct push to the test branch

Execution Environment:

Ubuntu latest

Python 3.9

Workflow Steps:

Checkout: Retrieves the latest code

Setup: Configures Python environment

Dependencies: Installs required packages from requirements.txt

Testing: Executes all test cases using python test.py


