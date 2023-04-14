import config
import requests

def client():
    cvat_base_url = config.BASE_URL
    session = requests.Session()
    session.post(f"{cvat_base_url}/auth/login", {"username": "guoweitao", "password": "Gwt200805.@"}).json()["key"]
    return cvat_base_url, session