import dataclasses
import json
from pathlib import Path


@dataclasses.dataclass
class Config:
    username: str
    access_key_id: str
    secret_access_key: str
    region: str
    bucket: str
    datasets: dict


def load_config() -> Config:
    here = Path(__file__).parent
    config_path = Path(here, "config.json")
    with config_path.open() as fp:
        values = json.load(fp)
    config = Config(**values)
    return config
