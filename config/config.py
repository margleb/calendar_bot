from dataclasses import dataclass
from functools import lru_cache
from os import getenv
from typing import TypeVar, Type

from pydantic import SecretStr, BaseModel, PostgresDsn
from yaml import load

try:
    from yaml import CLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

@dataclass
class BotConfig(BaseModel):
    token: SecretStr

class DbConfig(BaseModel):
    dsn: PostgresDsn
    is_echo: bool

ConfigType = TypeVar("ConfigType", bound=BaseModel)

@lru_cache
def read_config_file()-> dict:
    config = getenv("BOT_CONFIG")
    if config is None:
        raise ValueError('Config file not found.')
    with open(config, 'r') as file:
        result = load(file, Loader=SafeLoader)
    return result

@lru_cache
def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    config_dict = read_config_file()
    if root_key not in config_dict:
        raise ValueError('Key not found.')
    return model.model_validate(config_dict[root_key])