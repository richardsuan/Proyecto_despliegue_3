from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from model.config.core import config

class LabelEncoderTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns
        self.encoders = {col: LabelEncoder() for col in columns}

    def fit(self, X, y=None):
        for col in self.columns:
            self.encoders[col].fit(X[col])
        return self

    def transform(self, X):
        X_copy = X.copy()
        for col in self.columns:
            X_copy[col] = self.encoders[col].transform(X_copy[col])
        return X_copy

def create_pipeline(model_name: str) -> Pipeline:
    model_config = config.model_configs[model_name]
    
    # LabelEncoder for categorical variables
    label_encoder = LabelEncoderTransformer(columns=model_config.categorical_vars)
    
    # Column transformer to handle all preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('label_encode', label_encoder, model_config.categorical_vars)
        ],
        remainder='passthrough'
    )
    
    # Select the model based on the model name
    if model_name == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=model_config.n_estimators, 
            max_depth=model_config.max_depth,
            random_state=model_config.random_state
        )
    elif model_name == 'logistic_regression':
        model = LogisticRegression(
            solver=model_config.solver,
            max_iter=model_config.max_iter,
            random_state=model_config.random_state
        )
    else:
        raise ValueError(f"Model {model_name} not supported.")
    
    return Pipeline(
        [
            # Preprocessor
            ("preprocessor", preprocessor),
            # Model
            (model_name, model)
        ]
    )