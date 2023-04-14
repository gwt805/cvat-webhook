from loguru import logger
from login import client


base_url, cvat = client()

def get_task_info(task_id):
    task_info = cvat.get(f"{base_url}/tasks/{task_id}").json()
    keyframe_count = task_info["size"]
    return keyframe_count

def get_project_info(project_id):
    project_info = cvat.get(f"{base_url}/projects/{project_id}").json()
    project_name = project_info["name"]
    return project_name