from auth.login import client

base_url, cvat = client()

def get_project_info(project_id):
    project_info = cvat.get(f"{base_url}/api/projects/{project_id}").json()
    project_name = project_info["name"]
    return project_name

def get_task_info(task_id):
    task_info = cvat.get(f"{base_url}/api/tasks/{task_id}").json()
    task_name = task_info["name"]
    return task_name

def get_job_info(job_id):
    job_info = cvat.get(f"{base_url}/api/tasks/{job_id}").json()
    task_id = job_info["name"]
    return task_id

def get_issue_info(issue_id):
    issue_info = cvat.get(f"{base_url}/api/tasks/{issue_id}").json()
    frame = issue_info["frame"]
    job_id = issue_info["job"]
    return job_id, frame