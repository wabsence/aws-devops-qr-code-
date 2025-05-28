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
  - [Kubernetes Deployment](#kubernetes-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Infrastructure as Code](#infrastructure-as-code)
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








## Goal

The goal is to get hands-on with DevOps practices like Containerization, CICD and monitoring.

## Author

[Wahab Mustapha](https://github.com/wabsence)

## License

[MIT](./LICENSE)
    