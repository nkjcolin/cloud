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

## Kubernetes Deployment 

# Create Deployment 
```bash
kubectl create -f deployment.yaml
```

## Accessing the Application
```bash
http://localhost:5000
```
