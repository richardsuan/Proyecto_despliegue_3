from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError
from app.config import settings
from model.config.core import config
from app.schemas import Input

# model/processing/validation.py

def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_configs[settings.MODEL_NAME].features
        if validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    # Si todas las filas se eliminan, devolver el DataFrame original
    if validated_data.empty:
        return input_data

    return validated_data

def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[Optional[pd.DataFrame], Optional[dict]]:
    """Check model inputs for unprocessable values."""    
    relevant_data = input_data[config.model_configs[settings.MODEL_NAME].features].copy()
    print("soy relevant_data", relevant_data)
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    if validated_data.empty:
        return None, {"error": "No hay datos válidos después de eliminar filas con valores nulos."}

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class MultipleDataInputs(BaseModel):
    inputs: List[Input]
