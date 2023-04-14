from login import client

base_url, cvat = client()

def get_project_info(project_id):
    project_info = cvat.get(f"{base_url}/projects/{project_id}").json()
    project_name = project_info["name"]
    return project_name
