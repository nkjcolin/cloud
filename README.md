pip/pip3 install pipenv

try pipenv --version, something should pop up

after cloning repository, open folder in vscode and in vscode terminal run:

pipenv sync

local venv should be created in your computer, select the interpreter in that venv as your project interpreter

access local webserver in browser type "127.0.0.1:5000"


Dockerise the app 

docker build -t docker_username/python-flask:latest . 

docker container run -d -p 5000:5000 docker_username/python-flask:latest
