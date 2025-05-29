# QR Code Generator - DevOps Deployment Project

![QR Code Generator Demo](assets/demo-screenshot.png)

A full-stack QR code generator application with Next.js frontend and FastAPI backend, demonstrating modern DevOps practices including containerization, CI/CD pipelines, and cloud deployment.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Local Development](#local-development)
  - [Dockerization](#dockerization)
- [CI/CD GitHub-Actions](#cicd-(github-actions))
- [Infrastructure as Code](#infrastructure-as-code)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Features
- Generate QR codes for any URL
- Responsive web interface (Next.js)
- REST API backend (FastAPI)
- Containerized with Docker
- Automated CI/CD pipeline
- Infrastructure as Code (Terraform)
- Scalable Kubernetes deployment
- Monitoring with Prometheus/Grafana

## Technology Stack
**Frontend:**  
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)

**Backend:**  
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**DevOps:**  
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Prerequisites
Before you begin, ensure you have installed:
- Docker 20.10+
- Docker Compose 2.0+
- Node.js 16+
- Python 3.9+
- kubectl (for Kubernetes deployment)
- Terraform (for cloud provisioning)

## Getting Started

### Local Development
1. Clone the repository and Install Python dependencies and Start the FastAPI server with hot reload:
   ```bash
   git clone https://github.com/yourusername/devops-qr-code.git
   cd devops-qr-code
   cd api
   python -m venv .venv
   cp .env.example .env
   pip install -r requirements.txt

2. Start the frontend
    ```bash
    cd ../front-end-nextjs
    npm install
    npm run dev

3. The API and Frontend will be available at:
    - Local URL: http://localhost:8000
    - Interactive Docs (Swagger UI): http://localhost:8000/docs
    - Alternative Docs (Redoc): http://localhost:8000/redoc
    - Frontend: http://localhost:3000

### Dockerization
    Create a Dockerfile to dockerized both the frontend and the backend then Build & Run Containers
    
4. Backend
    ```bash
    cd api/
    docker build -t wabsense/devops-qr-code-api .
    docker run -d --name devops-qr-code-api -p 8000:8000 wabsense/devops-qr-code-api

5. Frontend
    ```bash
    cd front-end-nextjs/
    docker build -t wabsense/devops-qr-code-frontend .
    docker run -d --name devops-qr-code-frontend -p 3000:3000 wabsense/devops-qr-code-frontend

6. Push images to DockerHub
    ```bash
    docker push wabsense/devops-qr-code-api
    docker push wabsense/devops-qr-code-frontend

### 3. CI/CD (GitHub-Actions)
## Automate builds on every git push: check the build-deploy.yaml file
8. Required Setup: Create a Docker Hub access token:

- Go to Docker Hub → Account Settings → Security
- Click "New Access Token"
- Give it a name and select permissions
- Copy the generated token and use it as your DOCKER_HUB_TOKEN secret

9. Add these secrets to your GitHub repository:

- Go to your GitHub repo → Settings → Secrets and variables → Actions
- Add these repository secrets:

- DOCKER_USERNAME: Your Docker Hub username
- DOCKER_PASSWORD or DOCKER_HUB_TOKEN: Your Docker Hub password or access token



### Infrastructure as Code
## Cloud infrastructure is provisioned using Terraform:
10. Infrastructure 
 - create all neccesary files and run
    ```bash
    terraform init
    terraform plan
    terraform apply
    aws eks update-kubeconfig --region us-east-1 --name qrcode-k8s-cluster
 - View [Infrastructure:](./infrastructure/)


### Kubernetes Deployment
## Deploy to eks-cluster using k8s: Yaml files
10. Deployments
 - create all neccesary files and run
    ```bash
    kubectl apply -f backend.yaml
    kubectl apply -f frontend.yaml
    chmod +x fix-s3-permissions.sh
    ./fix-s3-permissions.sh
 - View [Deployments:](./k8s-deployment/)

## Goal

The goal is to get hands-on with DevOps practices like Containerization, CICD and monitoring.

## Author

[Wahab Mustapha](https://github.com/wabsence)

## License

[MIT](./LICENSE)
    