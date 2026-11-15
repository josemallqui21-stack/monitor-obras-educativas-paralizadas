# Pipeline ESCALE y ENLA: infraestructura educativa y aprendizajes por región

Proyecto académico "Monitor de obras de infraestructura educativa paralizadas" (USMP, Data Analytics).
Con **un solo comando** abre Chrome (visible), entra a los portales del MINEDU, descarga lo necesario, lo registra y deja dos tablas limpias en CSV.

> **Un solo comando para todo:** `python src\pipeline_completo.py` (o doble clic en `ejecutar.bat`). Hace 9 pasos: descarga (ESCALE, ENLA, Contraloría y
> MEF; INFOBRAS solo si se pide), tablas de ESCALE y ENLA, limpieza de datos personales, proyecto PDF, **producto final** (un solo CSV para el dashboard: `data/final/dashboard_obras.csv`), diccionario,
> auditoría de datos personales, inventario (`docs/inventario_datos.md`) y auditoría de calidad del CSV único (`docs/auditoria_calidad.csv`). Opciones: `--sin-descarga` (solo procesar), `--fuentes escale,enla,contraloria,mef,infobras`,
> `--forzar`, `--headless`. Se puede repetir sin miedo: lo ya hecho se salta y los resultados salen idénticos.
> **En Jupyter / VS Code:** `notebooks/proyecto_completo.ipynb` es **un solo cuaderno con todo el código adentro** (no necesita la carpeta `src`): hace lo mismo paso a paso, con los resultados (kernel `.venv`, *Run All*). Se regenera desde `src` con `python generar_cuaderno.py`.
> **Qué usar para el tablero (Power BI):** `data/final/dashboard_obras.csv` (y su diccionario `dashboard_obras_diccionario.csv`); cómo usarlo y sus límites: `docs/producto_final.md`.

## Cómo corre en GitHub (automático)

[![Pipeline](https://github.com/ochaccachavez-crypto/monitor-obras-educativas-paralizadas/actions/workflows/procesar.yml/badge.svg)](https://github.com/ochaccachavez-crypto/monitor-obras-educativas-paralizadas/actions/workflows/procesar.yml)

**Flujo `procesar.yml`** (pestaña **Actions**): corre solo cada vez que se sube un cambio al código, o con el botón *Run workflow*. Instala Python y las librerías y ejecuta
`python src/pipeline_completo.py --desde-tablas`, que rehace el **producto final** desde las tablas ya procesadas (`data/processed`): NLP de causas, tablas, **CSV único del dashboard**,
diccionario y las tres auditorías (datos personales, comprobaciones y calidad). Si algún paso falla o la auditoría de calidad encuentra un error, la corrida sale en rojo.
Si el CSV cambió, el flujo lo guarda en `data/final`.

**Qué NO está en el repositorio y por qué:** los datos crudos (`data/raw`, ~450 MB) y los archivos temporales (`data/interim`). Algunos crudos traen datos personales
(el archivo del MEF tiene nombres de ingenieros en sus textos y el padrón de ESCALE el nombre, teléfono y correo del director de cada colegio), y el del MEF supera el límite de GitHub.
Las tablas de `data/processed` y `data/final` sí están y fueron auditadas: no tienen nombres de personas.

**Al bajar el repositorio** el cuaderno, `proyecto_completo.py` y `ejecutar.bat --sin-descarga` detectan que no hay datos crudos y parten solos de las tablas procesadas (pasos 5 a 9, menos de 1 minuto); no hace falta ninguna opción.

**Para repetir todo desde los portales (en la computadora, con Chrome):** `ejecutar.bat` (hace los 9 pasos: descarga, tablas, PDF, NLP, CSV único, auditorías) o abrir
`notebooks/proyecto_completo.ipynb` / `python proyecto_completo.py`. Con datos ya descargados: `ejecutar.bat --sin-descarga`.

**El resultado** es `data/final/dashboard_obras.csv`. Power BI lo lee directo desde GitHub: *Obtener datos → Web →*
`https://raw.githubusercontent.com/ochaccachavez-crypto/monitor-obras-educativas-paralizadas/main/data/final/dashboard_obras.csv`.

## Qué hace

1. **ESCALE** (Censo Educativo): recorre las carpetas de cada año desde 2022, y descarga los archivos de local educativo, servicios básicos,
   edificaciones, padrón y el diccionario de datos.
2. **ENLA** (UMC / SICRECE): descarga los PDF de reportes de la UMC y, en el acceso público de SICRECE, consulta los resultados por región.
3. **Contraloría** (gob.pe): descarga los informes de obras paralizadas desde 2022 y sus anexos en Excel, en `data/raw/contraloria/{año de corte}`
   (se ejecuta sola con `--solo contraloria`).
4. **INFOBRAS** (Contraloría): busca las obras de Educación en estado Paralizada, descarga el listado y lee la ficha pública de cada obra
   (`--solo infobras`).
5. Convierte todo en tablas, las valida y escribe el diccionario de datos.
6. **Proyecto PDF** (`src/main_pdf.py`): inventaría los PDF descargados, extrae sus tablas y su texto, y arma las tablas con las cifras oficiales
   de la Contraloría (ver la sección «Proyecto PDF e INFOBRAS»).

Es **re-ejecutable**: lo que ya está descargado se salta y solo se agrega lo nuevo (por ejemplo, un año recién publicado).

## Requisitos

- Windows, Python 3.10 o superior y Google Chrome. El driver de Chrome lo descarga Selenium solo.
- Conexión a internet. Si un portal no responde, el programa lo avisa y sigue con el siguiente.

## Instalación (una sola vez)

`ejecutar.bat` lo hace solo la primera vez. A mano:

```
cd C:\data_analytic
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Cómo ejecutar

Doble clic en `ejecutar.bat`, o desde una terminal:

```
python src\main.py
```

Opciones (valen igual con `ejecutar.bat`):

| Opción | Efecto |
|---|---|
| `--anio-inicio 2022` | Primer año a descargar (por defecto 2022) |
| `--solo escale` o `--solo enla` | Ejecuta una sola fuente |
| `--forzar` | Descarga de nuevo aunque ya exista |
| `--headless` | Navegador sin ventana (por defecto se ve) |

La primera corrida completa (desde cero) tarda unos 10 minutos por las pausas de cortesía y la extracción.
La segunda no descarga nada: consulta los portales, recalcula las tablas y tarda unos 5 minutos.

## Qué produce

| Archivo | Contenido |
|---|---|
| `data/processed/escale_infraestructura.csv` | Una fila por distrito y año (2022 a 2025): locales públicos, % con agua, desagüe y electricidad de red pública, % rural, % con riesgo estructural y % con estructura en mal estado |
| `data/processed/enla_regiones.csv` | Una fila por región, año, grado y evaluación: % de estudiantes en nivel Satisfactorio en Lectura y Matemática (4.° primaria y 2.° secundaria) |
| `data/processed/*.xlsx` | Las mismas dos tablas en Excel, con la hoja `datos` (números como números, ubigeo como texto) y la hoja `diccionario` |
| `notebooks/proyecto_completo.ipynb` | **El cuaderno único**: lleva adentro el código de los 30 módulos (celdas `%%modulo`) y reproduce todo el proyecto (los 9 pasos) con los resultados. Es el que se corre en VS Code |
| `proyecto_completo.py` | **El mismo flujo de inicio a fin, solo código** (sin explicaciones): `python proyecto_completo.py`, o en VS Code *Run Cell* en cada bloque `# %%`. El código de cada módulo está en `src/` |
| `generar_cuaderno.py` | Arma el cuaderno copiando el código de `src` y también `proyecto_completo.py` (`--ejecutar` corre el cuaderno y guarda los resultados) |
| `docs/leer_en_R.R` | Para R: lee `dashboard_obras.csv` con los tipos correctos y la descripción de cada columna (atributo `label`) |
| `data/raw/escale/{año}`, `data/raw/enla/{año}` | Archivos tal cual se descargan (nunca se modifican). Nombre: `{fuente}_{año}_{descripción}_{AAAA-MM-DD}.{ext}` |
| `data/interim/` | Archivos descomprimidos, solo para la extracción |
| `docs/log_descargas.txt` | Todo lo ocurrido, con fecha y hora |
| `docs/registro_fuentes.csv` | Una fila por archivo: fuente, URL, archivo, año, filtros usados, fecha, tamaño y estado (ok, error u omitido) |
| `docs/diccionario.csv` | Qué significa cada columna de las tablas finales: tipo, descripción, unidad, fuente, años con dato y notas (la misma información va en la hoja `diccionario` de cada Excel) |
| `docs/reconocimiento.md`, `docs/reglas_datos.md` | Cómo es cada portal y las reglas con que se calculó cada columna |
| `docs/capturas/` | Capturas de pantalla del reconocimiento y de cualquier paso que falle |

## Proyecto PDF e INFOBRAS (Contraloría)

Sirve para **validar tu base contra las cifras oficiales** de la Contraloría y para enriquecer el análisis (causas de paralización, montos,
departamentos). Orden de trabajo:

```
python src\pipeline_completo.py --sin-descarga   (todo lo que sigue, de una vez, sin consultar portales)
python src\main.py --solo contraloria            (solo bajar los informes PDF y anexos Excel -> data/raw/contraloria)
python src\main.py --solo infobras               (volver a leer INFOBRAS: cambia el listado y los números; una sola persona)
python src\main_pdf.py                           (solo las fases 1 a 5 del proyecto PDF; --hasta 3 para parar antes)
```

| Fase | Qué hace | Salida |
|---|---|---|
| 1 | Inventario de PDF/PPT: fuente, año, páginas, si tiene texto seleccionable o es un escaneo, tablas detectadas | `docs/inventario_pdf.csv` |
| 2 | Texto y tablas de cada PDF, con las tablas clasificadas por tipo | `data/interim/pdf/{informe}/`, `docs/catalogo_tablas.csv` |
| 3 | Tablas finales y validaciones (sumas contra el total del informe y contra los anexos Excel) | `data/processed/*.csv`, `docs/validacion_*.csv` |
| 4 | Texto: citas sobre educación, términos frecuentes y grupo de causa por palabras clave | `citas_educacion.csv`, `frecuencia_terminos.csv`, `causa_grupo` en `fichas_infobras.csv` |
| 5 | Diccionario y documentación (el script único lo escribe después del producto final) | `docs/diccionario.csv`, `docs/hallazgos_pdf.md`, `docs/producto_final.md`, `docs/leer_en_R.R` |

Las tablas de apoyo (`data/processed`, UTF-8; cada cifra de un PDF lleva `fuente_pdf`, `pagina` y `tabla_n`): `cifras_oficiales_contraloria`, `contraloria_*`
(causales, distribuciones, obras por corte y panel, PIM, modalidad, evento, servicios de control, principales obras), `infobras_*` (fichas, avances, paralizaciones),
`mef_f12b_obras` (devengado por CUI), `escale_obras_en_local`, `enla_regiones`, `enla_niveles_logro`, `enla_pdf`, `citas_educacion` y `frecuencia_terminos`.
El **producto final** es un solo CSV, `data/final/dashboard_obras.csv`, en formato largo (la columna `tipo_registro` dice qué es cada fila: obras de INFOBRAS, obras por corte de la Contraloría,
series por departamento y país, causales y contexto por región). Las cinco tablas con las que se arma están en `data/interim/componentes`. Para leerlo en R: `docs/leer_en_R.R` (usa `readr`).
**Lee `docs/hallazgos_pdf.md` antes de usar las cifras**: explica qué se validó, qué no coincide y por qué.

Re-ejecutable: un PDF ya procesado no se vuelve a procesar (salvo `--forzar`); cada fase deja su rastro en `docs/log_pdf.txt`.
Los PDF originales nunca se modifican.

## Cómo funciona

- **Descubre, no memoriza.** Los años y los archivos se leen de los portales. Los nombres de archivo de ESCALE cambian cada año, así que se eligen por patrón (`config.py`, `ESCALE_PATRONES`).
- **Una fuente que falla no detiene a las demás.** Cada paso se reintenta hasta 3 veces; si sigue fallando, se toma una captura en `docs/capturas`, se anota en el log y se sigue.
- **ESCALE.** Un local es público si tiene algún servicio de gestión pública en el padrón. Se calculan los tres servicios de red pública con el código que define el diccionario de cada año (los formatos de 2022, 2023, 2024 y 2025 son distintos).
- **ENLA.** Los números de SICRECE solo se dibujan en un gráfico; el programa elige los filtros con clics y guarda en `data/raw/enla` la respuesta de datos que la propia página recibe. No se usa OCR.

## Limitaciones (léelas antes de usar los datos)

- **Años:** ESCALE tiene datos de 2022 a 2025 (último publicado). ENLA solo tiene 2022 (muestral), 2023 (muestral), 2024 (censal, solo 4.° de primaria) y 2025 (muestral). 2020, 2021 y 2026 no tienen evaluación.
- **Nivel geográfico:** ESCALE llega a distrito. ENLA llega a región (DRE): 23 departamentos sin Lima, Callao, Lima Metropolitana y Lima Provincias.
- **No existe "reparación total".** El censo no tiene esa categoría. Se usan dos medidas del estado estructural de las edificaciones en uso: riesgo de colapso o riesgo estructural, y estructura (muros, columnas, vigas o techos) en mal estado.
- **ENLA no tiene desglose urbano/rural por región:** SICRECE lo desactiva cuando se consulta por región.
- **2023 (servicios):** el 8,5 % de los locales públicos no tiene datos de servicios en la base publicada. Quedan como "sin dato"; la cifra de 2023 puede estar sesgada.
- **2024 (riesgo estructural):** la respuesta de riesgo se declara mucho menos que en los otros años; esa columna no es comparable en 2024.
- **Cambios de definición:** 2024 cambió la pregunta de servicios y 2025 pasó los servicios a la tabla lineal; en 2025 la electricidad "de terceros" también cuenta como red pública (efecto de 0,18 puntos).
- **MUESTRAL y CENSAL no son estrictamente comparables** (columna `evaluacion`).
- El detalle y las cifras están en `docs/reglas_datos.md`.

## Si el portal cambia

Todo lo que puede cambiar está en un solo lugar, **`src/config.py`**: URLs, textos de botones, selectores y patrones de archivos.

| Si falla... | Revisa en `config.py` |
|---|---|
| ESCALE no encuentra la carpeta o los años | `ESCALE_URL_INICIO`, `ESCALE_CARPETA_CENSO` |
| ESCALE no descarga o no encuentra archivos | `ESCALE_BOTON_DESCARGAR`, `ESCALE_SELECTOR_ARCHIVOS`, `ESCALE_PATRONES` |
| Un año nuevo de ESCALE trae otras columnas | `ESCALE_SERVICIOS_TABLA`, `ESCALE_SERVICIOS_COLUMNAS`, `ESCALE_EDIFICACIONES` |
| UMC no descarga PDF | `ENLA_URL_INICIO`, `ENLA_REGEX_PAGINA_ANIO`, `ENLA_REGEX_PDF`, `ENLA_EXCLUIR` |
| SICRECE no entra o no encuentra los filtros | `SICRECE_*` (acceso público, orden de las listas, nombres de casillas) |
| SICRECE busca pero no llega respuesta | `SICRECE_API_REPORTE` (la parte final de la dirección de la respuesta) |

Para saber qué falló, abre `docs/log_descargas.txt` y la captura de pantalla de `docs/capturas/` con el mismo nombre.

## Reglas de cortesía y fuentes

- User-Agent identificable ("Proyecto academico USMP - Data Analytics"), pausa aleatoria de 2 a 5 segundos entre descargas, sin sesiones en paralelo y máximo 3 reintentos.
- ESCALE no tiene `robots.txt`. El de UMC solo bloquea `/wp-admin/`. **El repositorio institucional del MINEDU prohíbe los bots en su `robots.txt`, por eso no se usa.** No se encontraron los términos de uso de ESCALE ni de UMC; revísalos si vas a publicar.
- UMC solo funciona por `http://` (su certificado HTTPS está roto), y para poder descargar se confía solo en ese sitio en el Chrome automatizado.
- SICRECE se usa por su **acceso público**, con el rol "Estudiante de pregrado" que pide su cuestionario de entrada. No se usan perfiles con sesión ni credenciales.
- No se guardan datos personales: ESCALE se agrega por distrito y ENLA por región.
- `requirements.txt` trae las librerías del curso; hoy el código usa selenium, pandas, numpy y pdfplumber.

## Recorrido para la presentación

1. Se abre Chrome con `ejecutar.bat` y se ve cómo entra a ESCALE, elige la carpeta del Censo Educativo, recorre las páginas de cada año y descarga los archivos.
2. Después va a la UMC y baja los PDF de resultados de cada año.
3. Entra a SICRECE (acceso público), elige tipo de evaluación, año, nivel y grado, marca Lectura, Matemática y regiones, y pulsa Buscar.
4. La consola muestra el resumen (descargados, omitidos, errores) y la validación; los resultados quedan en `data/processed`.
5. Al ejecutar otra vez, todo aparece como "ya estaba descargado, se omite".
