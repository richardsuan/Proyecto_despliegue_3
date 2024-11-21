from typing import Any, List, Optional

from pydantic import BaseModel
from .input import Input

# Esquema de los resultados de predicción
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]

# Esquema para inputs múltiples
class MultipleDataInputs(BaseModel):
    inputs: List[Input]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "FID_puntos_comerciales": 124298,
                        "municipio": "Ipiales",
                        "departamen": "Nariño",
                        "cod_depart": 52,
                        "cod_dane_mpio": 52356,
                        "categoria_mtv11": "Condicionada",
                        "cod_precios": "2.1.1",
                        "Vigencia": 2017,
                        "FID_ECOSISTEMAS_2017": 325495,
                        "OBJECTID_1": 325495,
                        "TIPO_ECOSI": "Terrestre",
                        "GRADO_TRAN": "Transformado",
                        "GRAN_BIOMA": "Zonobioma Humedo Tropical",
                        "BIOMA_PREL": "Zonobioma Humedo Tropical",
                        "BIOMA_IAvH": "Zonobioma Humedo Tropical Piedemonte Amazonas",
                        "ECOS_SINTE": "Agroecosistema",
                        "ECOS_GENER": "Agroecosistema de mosaico de pastos y espacios naturales",
                        "UNIDAD_SIN": "Agroecosistema de mosaico de pastos y espacios naturales de clima Calido Humedo en Crestas y espinazos con suelo de Condiciones oxidantes y evolucion moderada o incipiente y Pendientes escarpadas o Miscelaneo Rocoso",
                        "AMBIENTE_A": "N.A.",
                        "SUBSISTEMA": "N.A.",
                        "ZONA_HIDRO": "N.A.",
                        "ORIGEN": "N.A.",
                        "TIPO_AGUA": "N.A.",
                        "CLIMA": "Calido Humedo",
                        "PAISAJE": "Lomerio",
                        "RELIEVE": "Crestas y espinazos",
                        "SUELOS": "Typic Dystrudepts, Typic Udorthents",
                        "AMB_EDAFOG": "9 y 11",
                        "DESC_AMB_E": "Condiciones oxidantes y evolucion moderada o incipiente y Pendientes escarpadas o Miscelaneo Rocoso",
                        "COBERTURA": "Mosaico de pastos y espacios naturales",
                        "UNI_BIOTIC": "Piedemonte Amazonas",
                        "ANFIBIOS": "ab-ac-ai-aj-ak-am-av-ay-c-ch-ck-cm-y",
                        "AVES": "aa-ai-aj-al-am-an-ao-ap-ba-bb-c-dy-dz-ea-eb-ec-et-fg-fj-fq-y-z",
                        "MAGNOLIOPS": "cc-cd-cf-cw-df-dg-dh-dk-dw-dx-dy-fl-fm-fn-fo-fp-fq-fr-fs-ft-fu-ge",
                        "MAMIFEROS": "ab-ac-ae-af-ah-ai-ak-bi-bs-bt-bx-i-p-q-r-s-u",
                        "REPTILES": "ah-aj-ak-al-au-bd-by-bz-cd-co-r-s-t-v-w-y-z",
                        "No_Anfibio": 13,
                        "No_Aves": 22,
                        "No_Magnoli": 22,
                        "No_Mamifer": 17,
                        "No_Reptile": 17,
                        "SHAPE_Leng": 0.086285968,
                        "AH": 4,
                        "NOMAH": "Amazonas",
                        "ZH": 47,
                        "NOMZH": "Putumayo",
                        "SZH": 4702,
                        "NOMSZH": "Río San_Miguel",
                        "IPHE_VALOR": 0.221219472,
                        "IPHE_CATEGORIA": "Bajo",
                        "IEUA_VALOR": 0.204276301,
                        "IUEA_CATEGORIA": "Alto",
                        "HHV2020": 141.8291411,
                        "HHA_2020": 2.69724E-05,
                        "IARC_VALOR": 0.000535979,
                        "IARC_CATEGORIA": "Muy Bajo",
                        "IUA_MEDIO_VALOR": 0.002623792,
                        "IUA_MEDIO_CAREGORIA": "Muy Bajo",
                        "IUA_SECO_VALOR": 0.006245184,
                        "IUA_sECO_CATEGORIA": "Muy Bajo",
                        "IACAL_M": 1.4,
                        "CATIACAL_M": "Baja",
                        "IACAL_S": 2.4,
                        "CIACAL_S": "Moderada",
                        "irh": 0.74,
                        "cat": "Moderada",
                        "IVH_MEDIO_VALOR": 2,
                        "IVH_MEDIO_CATEGORIA": "Baja",
                        "IVH_SECO_VALOR": 2,
                        "IVH_SECO_CATEGORIA": "Baja",
                        "FID_Correlacion_5048_md": 694,
                        "UCSuelo": "CA",
                        "S_UC": "CA",
                        "S_UC_FASE": "CA",
                        "OTRAS_FA_1": "Cuerpos de agua",
                        "PENDIENT_1": "Cuerpos de agua",
                        "EROSION_1": "Cuerpos de agua",
                        "S_CLIMA": "Cuerpos de agua",
                        "CLIMA_1": "Cuerpos de agua",
                        "S_PAISAJE": "Cuerpos de agua",
                        "PAISAJE_1": "Cuerpos de agua",
                        "TIPO_RELIE": "Cuerpos de agua",
                        "MATERIAL_P": "Cuerpos de agua",
                        "SUBGRUPO": "Cuerpos de agua",
                        "AVES": "Cuerpos de agua"
                    }
                ]
            }
        }