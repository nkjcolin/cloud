# Restaurant Reservation Management System

## Overview

The Restaurant Reservation Management System (RRMS) is a distributed web application designed to recommend restaurants based on user preferences, facilitate reservations, and manage high traffic while ensuring maximum uptime. Users can filter and search for restaurants based on tags like 'healthy/average/unhealthy' or 'light/medium/heavy', view detailed information about restaurants including their ratings, descriptions, and opening hours, and finally, make reservations.

## Features
Restaurant Recommendations: Users can choose tags to filter restaurants according to their preferences, such as the type of cuisine or ambiance.

Detailed Restaurant Profiles: Each restaurant listing provides an overall rating, the number of users who have rated it, a description, and its opening hours.

Reservation System: Once a user selects a restaurant, they can fill out a form to make a reservation, helping restaurants manage their bookings efficiently.

Web Scraping for Reviews: An innovative feature, web scraping ensures our ratings and reviews are always updated, refining our restaurant recommendation algorithm.

## Project Overview 
![Overview](/documents/overview.png)

## Technical Stack
Flask-Based Application: The backbone of our application is built using the Flask framework.

Docker: We utilize Docker to containerize the application, ensuring a consistent environment across development and deployment.

Kubernetes: Kubernetes handles the deployment and service configuration, ensuring scalability and high availability of the RRMS.

AWS Resources:
- **RDS (Relational Database Service)**: 
  - We employ AWS RDS for a scalable and managed cloud database solution.

- **EKS (Elastic Kubernetes Service)**:
  - AWS EKS manages our Kubernetes cluster, including worker nodes. It provides the robustness and efficiency required for large-scale deployments.

- **Auto-scaling and Load Balancing**: 
  - To manage high traffic efficiently, the system is equipped with auto-scaling policies that dynamically adjust resources.
  - A load balancer distributes incoming traffic uniformly across EC2 instances, ensuring optimal performance.

## Menu Page
![Menu](/documents/menu.png)
## Menu Description
![Menu Item](/documents/menu-item.png)
## Booking Form
![Booking](/documents/booking.png)




## Dockerizing the Application

### Building the Docker Image

To Dockerize this Flask application with gRPC, follow these steps:

1. Open a terminal and navigate to the root directory of the application.

2. Build the Docker image using the following command:

```bash
docker build -t flask/python-flask reservation-webapp/
docker build -t grpc/python reservation-webapp/booking/
```

### Pulling the Docker Image (Optional)

```bash
docker image pull nkjcolin/cloud:flask
docker image pull nkjcolin/cloud:grpc
```

### Create a network within docker
```bash
docker network create my-network
```

### Running the Docker Container
```bash
docker container run -d --name grpc --network my-network -p 50051:50051 grpc/python
```
```bash
docker container run -d --name flask --network my-network -p 5000:5000 flask/python-flask
```
### docker-compose (Optional)
```bash
docker-compose up
```

### Accessing the Application
```bash
http://localhost:5000
```

## Localhost Kubernetes Set up & Deployment

### Docker login
```bash
docker login 
```

### Using the docker image above,

```bash
docker tag grpc/python:grpc nkjcolin/cloud:grpc
```

```bash
docker tag flask/python:flask nkjcolin/cloud:flask
```

### Create Deployment & Service 
```bash
kubectl create -f deployment.yaml
```

### Forward the traffic from 5000 port to 80

```bash
kubectl port-forward svc/flask 5000:80
```

```bash
kubectl port-forward svc/grpc 50051:50051
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

## (EKS) Specify configuration details to interact with EKS cluster
```bash
aws eks update-kubeconfig --region us-east-1 --name eks-cluster_name
```
### (EKS) Installation of Stress library 
```bash
sudo yum update
sudo amazon-linux-extras install epel -y
sudo yum install -y stress
```
### (EKS) Simulate high traffic in ec2 instance
```bash
sudo nohup stress --cpu 2 --timeout 600 &
```
### (EKS) Kill off high traffic in ec2 instance
```bash
sudo pkill stress
```
### (EKS) Monitor CPU Usage in ec2 instance
```bash
top
```
