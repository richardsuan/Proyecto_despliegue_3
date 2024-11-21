import sys
from pathlib import Path
from pyspark.sql import SparkSession
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
import yaml
from utils.functions import get_args
# Añadir el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from model.pipeline import create_pipeline
from model.processing.data_manager import save_pipeline

# Cargar la configuración general de la aplicación
config_path = project_root / 'model/config/config.yml'
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

def load_model_config(model_name: str):
    model_config_path = project_root / 'model/config' / config['model_configs'][model_name]
    with open(model_config_path, 'r') as file:
        model_config = yaml.safe_load(file)
    return model_config

def run_training(model_name: str) -> None:
    model_config = load_model_config(model_name)
    
    # Imprimir el directorio de trabajo actual
    print("Directorio de trabajo actual:", os.getcwd())
    
    # Crear una sesión de Spark
    spark = SparkSession.builder.appName("DataPreprocessing").getOrCreate()

    # Cargar los datos con Spark
    data_path = project_root / config['app_config']['train_data_file']
    
    if not data_path.exists():
        print(f"Error: El archivo {data_path} no existe.")
        sys.exit(1)

    df1 = spark.read.csv(str(data_path), header=True, inferSchema=True, sep=',')

    # Convertir a Pandas
    df_filtrado = df1.toPandas()
            
    # Verificar que la variable dependiente esté presente
    if model_config['target'] not in df_filtrado.columns:
        print(f"Error: La columna '{model_config['target']}' no se encuentra en el DataFrame.")
        sys.exit(1)

    # Separar características y variable objetivo
    X = df_filtrado.drop(columns=[model_config['target']])
    y = df_filtrado[model_config['target']]

    label_encoders = {}
    # Codificar variables categóricas
    for col in X.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    le_target = LabelEncoder()
    y = le_target.fit_transform(y)
    # Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=model_config['test_size'], random_state=model_config['random_state'])

    pipeline = create_pipeline(model_name)
    pipeline.fit(X_train, y_train)
    save_pipeline(pipeline_to_persist=pipeline, model_name=model_name, label_encoders=label_encoders, label_encoder_target=le_target)

if __name__ == "__main__":    
    model_name = get_args()    
    run_training(model_name)