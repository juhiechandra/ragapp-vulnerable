import docker


def get_docker_client():
    return docker.from_env()
    client = docker.from_env()
    client.images.pull("ragapp/ragapp:latest")
    client.images.pull("ragapp/manager:latest")
    return client
