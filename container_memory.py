import docker
import re

def check_container_name(container_name):
    pattern = r'^wsk.*md5$'
    return re.match(pattern, container_name) is not None

def list_containers_recently_created_with_memory():
    client = docker.from_env()
    containers = client.containers.list(all=True)
    sorted_containers = sorted(containers, key=lambda c: c.attrs['Created'], reverse=True)
    return sorted_containers

def get_container_memory():
    recently_created_containers = list_containers_recently_created_with_memory()
    for container in recently_created_containers:
        if check_container_name(container.name):

            stats = container.stats(stream=False)
            memory_usage = stats['memory_stats']['usage']
            #image_name = container.image.tags[0] if container.image.tags else "N/A"

            return memory_usage, container.name



