#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:18:43 2024

@author: jaimeunriza
"""

from fastapi import FastAPI
from pydantic import BaseModel
import joblib  # Cambia si usaste otra librería para guardar tu modelo
import pandas as pd

# Cargar el modelo
modelo = joblib.load('modelo/modelo.pkl')  # Usamos "modelo" consistentemente

# Crear la instancia de FastAPI
app = FastAPI()


class PrediccionEntrada(BaseModel):
    municipio: int
    departamen: int
    categoria_mtv11: int
    TIPO_ECOSI: int
    GRADO_TRAN: int
    GRAN_BIOMA: int
    BIOMA_PREL: int
    BIOMA_IAvH: int
    ECOS_SINTE: int
    ECOS_GENER: int
    UNIDAD_SIN: int
    CLIMA: int
    PAISAJE: int
    RELIEVE: int
    SUELOS: int
    AMB_EDAFOG: int
    DESC_AMB_E: int
    COBERTURA: int
    ANFIBIOS: int
    AVES: int
    MAGNOLIOPS: int
    MAMIFEROS: int
    REPTILES: int
    NOMAH: int
    NOMZH: int
    NOMSZH: int
    IPHE_CATEGORIA: int
    IUEA_CATEGORIA: int
    HHV2020: float
    HHA_2020: float
    IARC_CATEGORIA: int
    IUA_MEDIO_CAREGORIA: int
    IUA_sECO_CATEGORIA: int
    CATIACAL_M: int
    CIACAL_S: int
    cat: int
    IVH_MEDIO_CATEGORIA: int
    IVH_SECO_CATEGORIA: int
    S_UC_FASE: int
    OTRAS_FA_1: int
    PENDIENT_1: int
    EROSION_1: int
    S_CLIMA: int
    CLIMA_1: int
    S_PAISAJE: int
    PAISAJE_1: int
    TIPO_RELIE: int
    MATERIAL_P: int
    SUBGRUPO: int
    PERFILES: int
    PORCENTAJE: int
    PROFUNDIDA: int
    TEXTURA: int
    FERTILIDAD: int
    ACIDEZ: int
    DRENAJE: int
    HUMEDAD: int
    ALUMINIO: int
    SALINIDAD_1: int
    SODICIDAD: int
    SATURACION: int
    CALCAREO: int
    Significad: int
    layer: int
    codigo: float
    FA: int



@app.post("/predecir/")
def predecir(datos: PrediccionEntrada):
    try:
        # Convertir los datos de entrada en un DataFrame
        entrada_dict = datos.dict()
        entrada_df = pd.DataFrame([entrada_dict])

        # Realizar la predicción
        prediccion = modelo.predict(entrada_df)  # Realiza la predicción

        # Devolver el resultado
        return {"prediccion": prediccion[0]}  # No convertimos a int
    except Exception as e:
        return {"error": str(e)}
    return {"prediccion": int(prediccion[0])}