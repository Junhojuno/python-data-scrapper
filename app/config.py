"""외부에 공개하면 안되는 정보가 담긴 config"""
import json
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent.parent


def get_secret(
    key: str,
    domain: str = 'NAVER',
    default_value: Optional[str] = None,
    json_path: str = str(BASE_DIR / "secrets.json"),
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[domain][key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")


NAVER_MONGO_DB_NAME = get_secret("MONGO_DB_NAME", "NAVER")
NAVER_MONGO_URL = get_secret("MONGO_URL", "NAVER")

YOUTUBE_MONGO_DB_NAME = get_secret("MONGO_DB_NAME", "YOUTUBE")
YOUTUBE_MONGO_URL = get_secret("MONGO_URL", "YOUTUBE")

YOUTUBE_API_KEY = get_secret("API_KEY", "YOUTUBE")
NAVER_API_ID = get_secret("API_ID", "NAVER")
NAVER_API_SECRET = get_secret("API_SECRET", "NAVER")


if __name__ == "__main__":
    world = get_secret("hello")
    print(world)
