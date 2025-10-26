# MBDAaaS - Model-Based Big Data Analytics-as-a-Service

## Overview
This project implements a **Model-Based Big Data Analytics-as-a-Service (MBDAaaS)** framework based on research for bridging the gap between security experts and data scientists.

## Features
- **Security-First Architecture**: Built-in data anonymization and privacy controls
- **Role-Based Access**: Separate configurations for security experts, data scientists, and business analysts
- **Modular Design**: Declarative, procedural, and deployment model layers
- **Service Catalog**: Abstract services with platform-specific implementations
- **Container Orchestration**: Docker and Kubernetes ready
- **Monitoring**: Built-in performance and quality metrics

## Project Structure
```
EPICS/
��� catalog/          # Service catalog and mappings
��� configs/          # Configuration files
��� data/             # Data storage (raw, processed, anonymized)
��� docs/             # Documentation
��� experiments/      # Experimental workflows
��� logs/             # Application and security logs
��� models/           # ML models (declarative, procedural, deployment)
��� monitoring/       # Performance and quality monitoring
��� notebooks/        # Jupyter notebooks
��� orchestration/   # Docker and Kubernetes configs
��� pipelines/        # Data and ML pipelines
��� results/          # Experiment results
��� roles/            # Role-based configurations
��� security/         # Security and privacy modules
��� services/         # Microservices
��� src/              # Source code
��� tests/            # Unit and integration tests
```

## Quick Start

### 1. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run the Application
```
python main.py
```

## Docker Deployment
```
cd orchestration/docker
docker-compose up -d
```

## Kubernetes Deployment
```
kubectl apply -f orchestration/kubernetes/
```

## Documentation
- [Architecture](docs/architecture.md)
- [Security Guidelines](docs/security_guidelines.md)
- [User Roles](docs/user_roles.md)
- [API Reference](docs/api_reference.md)

## License
MIT License

## Contributors
VRSEC IT Department - EPICS Project Team
