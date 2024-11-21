# Proyecto de Despliegue de Soluciones Analíticas - Estimación de Precios de la Tierra en Colombia


## Integrantes
Roberto Gonzalez Bustamante
Richard Anderson Suan Yara
Jaime Unriza

## Descripción del Proyecto
En Colombia, la falta de información precisa sobre los precios de la tierra rural limita el desarrollo rural y la productividad agropecuaria. Este proyecto busca resolver esta brecha de información, proporcionando una herramienta de estimación de precios de terrenos rurales a partir de datos biofísicos y socioeconómicos oficiales. Mediante el uso de un modelo de machine learning supervisado, el proyecto tiene como objetivo proporcionar una valoración más precisa de los terrenos rurales, optimizando la toma de decisiones en el mercado de tierras y en la planificación territorial.

## Contexto y Problemas Abordados
- **Productividad Agrícola Baja:**La ausencia de datos confiables sobre precios limita decisiones informadas de propietarios y entidades financieras.
- **Especulación de Precios:** Los precios inflados afectan a pequeños productores y distorsionan el mercado.
Informalidad y Conflictos Territoriales: La informalidad en la propiedad de tierras agrava los conflictos y limita el acceso a programas de desarrollo.
- **Planificación Territorial y Sostenibilidad:** La falta de datos confiables afecta la creación de políticas de uso del suelo y la conservación ambiental.

## Descripción del Conjunto de Datos

El conjunto de datos cuenta con 175,526 registros y fue recolectado entre 2020 y 2024 a partir de muestreos de campo y bases de datos oficiales de entidades como IGAC, IDEAM y UPRA. Los datos incluyen:

127 variables originales: que incluyen 4 de ubicación, 33 edáficas, 47 ecosistémicas, 27 hídricas y 20 climáticas.
Tipos de datos: 14 variables float64, 25 int64 y 90 object (categóricas).


# Ejecución del Proyecto

Para ejecutar este proyecto, sigue los siguientes pasos:

## 1. Instalar un entorno virtual

Primero, necesitas tener un entorno virtual para el proyecto. Si no tienes uno, puedes crear uno utilizando el siguiente comando:

```bash
python3 -m venv ./env-proyecto
```

## 2. Activar el entorno virtual

Una vez creado el entorno virtual, actívalo ejecutando el siguiente comando:

- En **Linux/Mac**:

    ```bash
    source ./env-proyecto/bin/activate
    ```

- En **Windows**:

    ```bash
    .\env-proyecto\Scripts\activate
    ```

## 3. Instalar las dependencias

Con el entorno virtual activado, instala las dependencias necesarias para el proyecto utilizando `pip`:

```bash
pip install tox
```
luego ejecutar el comando 
```bash
tox -e dep
```
esto puede tardar bastante ya que las librerias de pandas y sklearn son bastante pesadas

¡Listo! Ahora puedes ejecutar y trabajar en el proyecto dentro de tu entorno virtual.

---


## Agregar un Nuevo Modelo

Para agregar un nuevo modelo, sigue estos pasos:

1. **Crear el archivo de configuración del modelo**:
   - En el directorio `model/config/`, crea un archivo YAML con la configuración del nuevo modelo. Por ejemplo, `nuevo_modelo.yml`.
   - Define los parámetros del modelo en este archivo. Aquí tienes un ejemplo de configuración para un modelo de regresión logística:

     ```yaml
     target: "rango_precios_var_dependiente"
     features:
       - "FID_puntos_comerciales"
       - "municipio"
       - "departamen"
       - "cod_depart"
       - "cod_dane_mpio"
       - "categoria_mtv11"
     test_size: 0.2
     random_state: 42
     ```

2. **Actualizar el archivo de configuración general**:
   - Abre el archivo `model/config/config.yml`.
   - Agrega una entrada para el nuevo modelo en la sección `model_configs`. Por ejemplo:

     ```yaml
     model_configs:
       random_forest: "./model_configs/random_forest.yml"
       logistic_regression: "./model_configs/logistic_regression.yml"
       nuevo_modelo: "./model_configs/nuevo_modelo.yml"
     ```

3. **Implementar el modelo en el código**:
   - Abre el archivo [`model/train_pipeline.py`](model/train_pipeline.py).
   - Asegúrate de que el nuevo modelo esté correctamente referenciado en el código. Si es necesario, actualiza la función `create_pipeline` en [`model/pipeline.py`](model/pipeline.py) para incluir la lógica de tu nuevo modelo.

4. **Entrenar el nuevo modelo**:
   - Ejecuta el script de entrenamiento con el nombre del nuevo modelo:

     ```sh
     python model/train_pipeline.py nuevo_modelo
     ```