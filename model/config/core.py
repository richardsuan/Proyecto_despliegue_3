from pathlib import Path
from typing import Dict, List, Optional, Sequence
from pydantic import BaseModel
from strictyaml import YAML, load
import model
import yaml

# Project Directories
PACKAGE_ROOT = Path(model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config/config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained"

class AppConfig(BaseModel):
    package_name: str
    train_data_file: str
    test_data_file: str
    pipeline_save_file: str

class ModelConfig(BaseModel):
    target: str
    features: List[str]
    test_size: float
    random_state: int
    n_estimators: Optional[int] = None
    max_depth: Optional[int] = None
    solver: Optional[str] = None
    max_iter: Optional[int] = None
    temp_features: List[str] = []
    qual_vars: List[str]
    categorical_vars: Sequence[str]
    qual_mappings: Dict[str, int]
    version: str

class Config(BaseModel):
    app_config: AppConfig
    model_configs: Dict[str, ModelConfig]

def find_config_file() -> Path:
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")

def fetch_config_from_yaml(cfg_path: Optional[Path] = None) -> YAML:
    if not cfg_path:
        cfg_path = find_config_file()
    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")

def load_model_config(model_config_path: Path) -> Dict:
    with open(model_config_path, 'r') as file:
        model_config = yaml.safe_load(file)
    return model_config

def create_and_validate_config(parsed_config: YAML = None) -> Config:
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()
    model_configs = {}
    for model_name, model_config_path in parsed_config.data['model_configs'].items():
        model_config_full_path = PACKAGE_ROOT / 'config' / model_config_path
        model_config = load_model_config(model_config_full_path)
        model_configs[model_name] = ModelConfig(**model_config)
    _config = Config(
        app_config=AppConfig(**parsed_config.data['app_config']),
        model_configs=model_configs,
    )
    return _config

config = create_and_validate_config()