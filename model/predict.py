import logging
import typing as t
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from model.config.core import config, TRAINED_MODEL_DIR
from model.processing.data_manager import load_pipeline, load_label_encoders
from model.processing.validation import validate_inputs
from app.config import settings
import numpy as np
from loguru import logger

# Cargar la versión del modelo y los archivos necesarios
_version = config.model_configs[settings.MODEL_NAME].version
pipeline_file_name = f"{config.app_config.pipeline_save_file}-{settings.MODEL_NAME}-{_version}.pkl"
_abandono_pipe = load_pipeline(file_name=pipeline_file_name)
_label_encoders, _label_encoder_target = load_label_encoders(model_name=settings.MODEL_NAME)

def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""
    
    # Convertir los datos de entrada a un DataFrame de Pandas
    data = pd.DataFrame(input_data)
    logger.info("***************** sin errores cero")
    logger.info(data)
    
    # Validar los datos de entrada
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}
    
    if validated_data is None:
        return results

    logger.info("***************** sin errores uno")
    logger.info(validated_data)    
    
    # Imprimir los valores internos de todos los LabelEncoders
    logger.info("***************** sin errores uno???")  
    # Codificar las variables categóricas
    for col, le in _label_encoders.items():
        logger.info(f"Col: {col}")
        if col in validated_data.columns:
            logger.info(f"Codificando columna: {col}")
            try:
                # Reemplazar valores None con una etiqueta especial antes de codificar
                validated_data[col] = validated_data[col].fillna('missing')
                validated_data[col] = le.transform(validated_data[col])
            except ValueError as e:
                logger.error(f"Error al codificar la columna: {col}")
                logger.error(f"Valores no vistos: {set(validated_data[col].dropna().unique()) - set(le.classes_)}")
                # Manejar valores no vistos durante el entrenamiento
                unseen_labels = set(validated_data[col].dropna().unique()) - set(le.classes_)
                if unseen_labels:
                    # Expandir las clases del codificador para incluir 'missing'
                    le.classes_ = np.append(le.classes_, 'missing')
                    # Reemplazar etiquetas no vistas con 'missing'
                    validated_data[col] = validated_data[col].apply(
                        lambda x: 'missing' if x in unseen_labels else x
                    )
                # Volver a transformar los datos después del reemplazo
                validated_data[col] = le.transform(validated_data[col])
    
    logger.info("***************** sin errores dos")
    logger.info(validated_data)
    
    # Seleccionar las características relevantes
    features = config.model_configs[settings.MODEL_NAME].features
    logger.info("***************** sin errores tres")
    
    # Verificar que todas las características relevantes estén presentes en los datos validados
    missing_features = set(features) - set(validated_data.columns)
    if missing_features:
        errors = f"Faltan las siguientes características en los datos de entrada: {missing_features}"
        results["errors"] = errors
        return results
    
    # Rellenar las columnas faltantes con valores por defecto
    for feature in missing_features:
        validated_data[feature] = 'missing'
    
    # Asegurarse de que las columnas numéricas tengan valores válidos
    numeric_features = ['PROFUNDIDA', 'HHV2020', 'HHA_2020']
    for feature in numeric_features:
        if feature in validated_data.columns:
            validated_data[feature] = pd.to_numeric(validated_data[feature], errors='coerce').fillna(0.0)
    
    logger.info("***************** sin errores tres.cinco")
    logger.info(validated_data[features])
    
    # Realizar la predicción
    predictions = _abandono_pipe.predict(validated_data[features])
    logger.info("***************** sin errores cuatro")
    logger.info(predictions)
    
    # Decodificar las predicciones
    predictions_decoded = _label_encoder_target.inverse_transform(predictions)
    logger.info("***************** sin errores cinco")
    logger.info(predictions_decoded)
    
    if not errors:
        results = {
            "predictions": [pred for pred in predictions_decoded], 
            "version": _version,
            "errors": errors,
        }

    return results