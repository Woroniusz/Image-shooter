
# Documentation
## How to run docker:
### command:
```bash
sudo bash script/build_docker_compose.sh
```
### description:
This command builds the Docker images and starts the containers defined in the `docker-compose.yml` file. It uses the `script/build_docker_compose.sh` script to automate the process.


### how to run local:
#### backend
create .venv into backend
```bash
uv venv

```
switch to the virtual environment
```bash
source .venv/bin/activate
```

install torch and torchvision are required for the detectron2
```bash
uv run pip install torch torchvision
```

install rest of the requirements
```bash
uv sync --no-build-isolation
```

```bash
uv run shooter
```

#### frontend
Go to 
```bash
cd frontend/shooter
```
install the requirements
```bash
uv sync 
```
run the server
```bash
source .venv/bin/activate
python manage.py runserver
```




## How to configure project:
### backend:
all configuration are located in the `backend/config.toml` file.


