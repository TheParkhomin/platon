from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pyhocon import ConfigFactory


class DatabaseOptions(BaseModel):
    min_size: Optional[int] = None
    max_size: Optional[int] = None


class DatabaseConfig(BaseModel):
    url: str
    options: Optional[DatabaseOptions] = None


class PlatonConfig(BaseModel):
    database: DatabaseConfig
    hash_salt: str
    jwt_secret: str


def config_factory(folder: str = "settings") -> PlatonConfig:
    package_dir = Path(folder)
    conf_path = package_dir / "default.conf"
    factory = ConfigFactory.parse_file(conf_path)
    return PlatonConfig(**factory.get_config("config"))
