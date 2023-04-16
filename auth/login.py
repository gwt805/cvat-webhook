from config import config
import requests
from loguru import logger

def client():
    cvat_base_url = config.BASE_URL
    session = requests.Session()
    res = session.post(f"{cvat_base_url}/api/auth/login", json={"username": "guoweitao", "password": "Gwt200805.@"}).json()
    return cvat_base_url, session