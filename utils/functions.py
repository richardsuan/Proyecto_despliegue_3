from pathlib import Path
import yaml
import sys

def get_args():
    config_path = Path(__file__).resolve().parent.parent / 'model/config/config.yml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    if len(sys.argv) != 2:
        print("Usage: python train_pipeline.py <model_name>")
        print("Or Usage: python main.py <model_name>")
        sys.exit(1)

    model_name = sys.argv[1]
    if model_name not in config['model_configs']:
        print(f"Model {model_name} not found in configuration.")
        sys.exit(1)    
    return model_name