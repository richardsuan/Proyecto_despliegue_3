# Ejecución del Proyecto

Para ejecutar este proyecto, sigue los siguientes pasos:

## 1. Instalar un entorno virtual

Primero, necesitas tener un entorno virtual para el proyecto. Si no tienes uno, puedes crear uno utilizando el siguiente comando:

```bash
python3 -m venv ./proyecto
```

## 2. Activar el entorno virtual

Una vez creado el entorno virtual, actívalo ejecutando el siguiente comando:

- En **Linux/Mac**:

    ```bash
    source ./proyecto/bin/activate
    ```

- En **Windows**:

    ```bash
    .\proyecto\Scripts\activate
    ```

## 3. Instalar las dependencias

Con el entorno virtual activado, instala las dependencias necesarias para el proyecto utilizando `pip`:

```bash
pip install tox
```
luego ejecutar el comando 
```bash
tox -e dev
```
esto puede tardar bastante ya que las librerias de pandas y sklearn son bastante pesadas

¡Listo! Ahora puedes ejecutar y trabajar en el proyecto dentro de tu entorno virtual.

---

