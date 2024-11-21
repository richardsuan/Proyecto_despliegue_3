import sys
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pyspark.sql import SparkSession
import pandas as pd
from model.train_pipeline import run_training

# model/test_train_pipeline.py


# Añadir el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))


@pytest.fixture
def mock_config():
    return {
        'app_config': {
            'package_name': 'modelo-prediccion-tierras',
            'train_data_file': 'model/datasets/tabla_df.csv',
            'test_data_file': 'model/datasets/tabla_df.csv',
            'pipeline_save_file': 'modelo-prediccion-tierras-output'
        },
        'model_configs': {
            'random_forest': {
                'target': 'rango_precios_var_dependiente',
                'features': ['FID_puntos_comerciales', 'municipio', 'departamen'],
                'test_size': 0.25,
                'random_state': 42,
                'n_estimators': 850,
                'max_depth': 19,
                'temp_features': ['AVES'],
                'qual_vars': ['rango_precios_var_dependiente'],
                'categorical_vars': ['municipio', 'departamen', 'categoria_mtv11'],
                'qual_mappings': {'Attrited Customer': 1, 'Existing Customer': 0}
            }
        }
    }

@patch('model.train_pipeline.config', new_callable=MagicMock)
@patch('model.train_pipeline.SparkSession', new_callable=MagicMock)
@patch('model.train_pipeline.create_pipeline', new_callable=MagicMock)
@patch('model.train_pipeline.save_pipeline', new_callable=MagicMock)
def test_run_training_file_not_found(mock_save_pipeline, mock_create_pipeline, mock_spark, mock_config, mock_config_fixture):
    mock_config.model_configs = mock_config_fixture['model_configs']
    mock_config.app_config.train_data_file = 'non_existent_file.csv'
    
    with pytest.raises(SystemExit):
        run_training('random_forest')

@patch('model.train_pipeline.config', new_callable=MagicMock)
@patch('model.train_pipeline.SparkSession', new_callable=MagicMock)
@patch('model.train_pipeline.create_pipeline', new_callable=MagicMock)
@patch('model.train_pipeline.save_pipeline', new_callable=MagicMock)
def test_run_training_target_column_not_found(mock_save_pipeline, mock_create_pipeline, mock_spark, mock_config, mock_config_fixture):
    mock_config.model_configs = mock_config_fixture['model_configs']
    mock_config.app_config.train_data_file = 'model/datasets/tabla_df.csv'
    
    mock_spark.read.csv.return_value.toPandas.return_value = pd.DataFrame({
        'FID_puntos_comerciales': [1, 2],
        'municipio': ['A', 'B'],
        'departamen': ['X', 'Y']
    })
    
    with pytest.raises(SystemExit):
        run_training('random_forest')

@patch('model.train_pipeline.config', new_callable=MagicMock)
@patch('model.train_pipeline.SparkSession', new_callable=MagicMock)
@patch('model.train_pipeline.create_pipeline', new_callable=MagicMock)
@patch('model.train_pipeline.save_pipeline', new_callable=MagicMock)
def test_run_training_success(mock_save_pipeline, mock_create_pipeline, mock_spark, mock_config, mock_config_fixture):
    mock_config.model_configs = mock_config_fixture['model_configs']
    mock_config.app_config.train_data_file = 'model/datasets/tabla_df.csv'
    
    mock_spark.read.csv.return_value.toPandas.return_value = pd.DataFrame({
        'FID_puntos_comerciales': [1, 2],
        'municipio': ['A', 'B'],
        'departamen': ['X', 'Y'],
        'rango_precios_var_dependiente': [0, 1]
    })
    
    mock_pipeline = MagicMock()
    mock_create_pipeline.return_value = mock_pipeline
    
    run_training('random_forest')
    
    mock_pipeline.fit.assert_called_once()
    mock_save_pipeline.assert_called_once()