# LÉEME PRIMERO (para el equipo)

Proyecto "Monitor de obras de infraestructura educativa paralizadas" (USMP, Data Analytics). Todo el trabajo se hace en **Jupyter**.

## 1. Qué necesitas instalado
* Windows, **Python 3.10 o superior** (marcar "Add Python to PATH" al instalar), **Google Chrome** y **VS Code** con la extensión **Jupyter**.
* Internet (solo para la instalación y para las descargas).

## 2. Cómo armar el proyecto (una vez)
1. Crea una carpeta, por ejemplo `C:\data_analytic` (cualquier ruta sirve; mejor sin espacios).
2. Descomprime **todos los zip dentro de esa misma carpeta**: `proyecto_codigo_y_docs.zip`, `proyecto_datos_raw.zip` y `proyecto_datos_raw_mef.zip`.
   Debe quedar `src\`, `docs\`, `notebooks\`, `data\raw\`, `data\final\`, `ejecutar.bat`...
3. Doble clic en **`ejecutar.bat --sin-descarga`** (o en una terminal: `ejecutar.bat --sin-descarga`).
   La primera vez crea el entorno `.venv` e instala las librerías (unos minutos); después procesa todo en ~3 minutos. **No abre ningún portal.**
4. Si termina con `PIPELINE COMPLETO: terminado sin fallos`, todo está bien.

## 3. Cómo trabajar en Jupyter (VS Code)
1. VS Code → *Archivo → Abrir carpeta* → la carpeta del proyecto (instala la extensión **Jupyter**).
2. Abre **`notebooks\proyecto_completo.ipynb`**: es el cuaderno único, **lleva todo el código adentro** y reproduce todo el proyecto paso a paso.
3. Arriba a la derecha → *Seleccionar kernel* → *Python Environments* → **`.venv`**. (Si pide instalar `ipykernel`, acepta.) Luego *Run All*.
4. Opciones en la primera celda: `DESCARGAR` (False por defecto), `INCLUIR_INFOBRAS` (False: es una foto y cambiaría los números), `FORZAR`.

## 4. Qué leer, en este orden
0. **`data\final\dashboard_obras.csv`** — el CSV único para el dashboard (Power BI). Se filtra siempre por la columna `tipo_registro`.
1. `docs\producto_final.md` — qué contiene ese CSV, cómo usarlo en Power BI, el NLP de causas y los límites que hay que decir al presentar.
2. `docs\hallazgos_pdf.md` — qué se validó, qué no coincide y por qué (secciones 4.3 y 10).
3. `docs\inventario_datos.md` — qué datos hay y cuáles faltan.
4. `docs\diccionario.csv` — qué significa cada columna de cada tabla.
5. `docs\pendientes_extraccion.md` — estado de las tareas y decisiones que siguen abiertas.

## 5. Reglas que no se rompen
* `data\raw` **no se modifica nunca**.
* **Sin datos personales** (no guardar nombres de residentes, inspectores, contratistas ni auditores).
* Nombres de lugares en **MAYÚSCULAS y sin tildes**; ubigeos y códigos como **texto** (`"010101"`).
* Cada cifra con su procedencia; si la fuente trae un total, **validar la suma**.
* INFOBRAS no se vuelve a leer sin avisar: cambia el listado y los números del producto. Si se hace, **una sola persona a la vez** (dos lecturas simultáneas ya nos dieron duplicados). Pausas de cortesía de 2 a 5 s.
* Tablas nuevas: agregarlas en `src\inventario_datos.py` y describir **todas** sus columnas en `src\diccionario_pdf.py` (si falta una, el programa falla a propósito).
* Antes de entregar: `ejecutar.bat --sin-descarga` sin fallos y las demás tablas sin cambios.

## 6. Si algo falla
* `docs\log_descargas.txt` y `docs\log_pdf.txt` guardan todo lo ocurrido.
* El programa nunca borra lo descargado. Para repetir un paso, volver a ejecutarlo: lo ya hecho se salta.
* Los datos de INFOBRAS son del **27-oct y 11-nov-2026**, la Contraloría llega al corte de **jun-2026** y el MEF se descargó el **12-nov-2026** (archivo actualizado el 11-nov). No los actualicen sin avisar: cambian los números.
* **Sin nombres de personas:** la auditoría (`datos_personales.auditar`) detiene el proceso si encuentra alguno. Si un texto nuevo trae nombres, hay que ampliar `utils.omitir_nombres`.
