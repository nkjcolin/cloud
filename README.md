# Restaurant Reservation Management System

## Overview

This project implements a distributed restaurant reservation management system capable of handling high traffic and providing high availability. We achieve this by using Kubernetes to deploy Docker containers containing a Flask-based application.

## Dockerizing the Application

### Building the Docker Image

To Dockerize this Flask application, follow these steps:

1. Open a terminal and navigate to the root directory of the application.

2. Build the Docker image using the following command, replacing `docker_username/python-flask` with your desired image name:

```bash
docker build -t docker_username/python-flask:latest .
```

### Pulling the Docker Image (Optional)

```bash
docker image pull hub_username/python-flask:latest
```

### Running the Docker Container
```bash
docker container run -d -p 5000:5000 docker_username/python-flask:latest
```

### Accessing the Application
```bash
http://localhost:5000
```

## EC2 Kubernetes Set Up & Deployment 

### Update the instance packages
```bash
sudo apt update
```

### Install Docker & Conntrack
```bash
sudo apt -y install docker.io
sudo apt install conntrack
```


### Installation of kubectl and minikube 
```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x ./kubectl && sudo mv ./kubectl /usr/local/bin/kubectl
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

### Add the current user to the docker group
```bash
sudo usermod -aG docker $USER && newgrp docker
```

### Docker login
```bash
docker login 
```

### Create Deployment & Service 
```bash
kubectl create -f deployment.yaml
```

### Forward the traffic from 5000 port to 80
```bash
nohup kubectl port-forward svc/my-flask-app-service 5000:80 --address 0.0.0.0 &
```

### Access the web application 
```bash
public_ip_adress:5000
```


