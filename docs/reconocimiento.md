# Reconocimiento de fuentes (Fase 0)

Fecha del reconocimiento: 2026-10-23. Navegador: Chrome visible controlado con Selenium 4.51
(User-Agent "Proyecto academico USMP - Data Analytics"). No se descargó ningún archivo de datos;
solo se abrieron páginas y se tomaron capturas en `docs\capturas\`.

## 1. Hallazgos clave

1. **ESCALE sí tiene 2022-2025** (último año publicado: 2025). Los datos están en "Archivo de Datos"
   como archivos `.zip` por año. El módulo de local educativo son los archivos `Loc_*` / `Local_*`.
2. **ESCALE no trae indicadores ya calculados de agua, desagüe ni electricidad.** La serie "Indicadores
   desde 2016" (2016-2025) solo incluye pizarras, carpetas e Internet en infraestructura. La
   infraestructura hay que calcularla desde los archivos de local (`Loc_P200_ServBa`, etc.).
3. **Los nombres de archivo cambian cada año** (ej. servicios básicos: `41_Local_Servicios_Basicos` en
   2022, `39_Loc_P200_ServBa` en 2023, `48_Loc_P200_ServBa` en 2024; en 2025 no aparece un archivo con
   ese nombre). El script debe descubrir por patrón, no por nombre fijo.
4. **"ENLA" como nombre existe solo desde 2023.** 2022 es la Evaluación Muestral (EM 2022). 2021 (EM) y
   2020 (ECE) fueron suspendidas. La ENLA 2026 fue ordenada y luego dejada sin efecto, así que el
   último año con resultados es **2025**.
5. **ENLA no ofrece tablas regionales como archivo directo.** Hay PDFs nacionales, bases de datos en
   Google Drive, visores embebidos y el sistema SICRECE. Los reportes regionales no se pudieron confirmar.
6. **Restricciones de acceso detectadas** (ver sección 3): el repositorio institucional prohíbe bots y
   `umc.minedu.gob.pe` falla por HTTPS.

## 2. Entorno creado

- Raíz: `C:\data_analytic\` con `data\raw\{escale,enla}`, `data\interim`, `data\processed`, `src`, `docs\capturas`.
- Entorno virtual: `C:\data_analytic\.venv` (Python 3.13).
- Librerías (`requirements.txt`): selenium (4.51.0), pandas, openpyxl, beautifulsoup4, lxml, pdfplumber, pyreadstat, tqdm.
- Selenium Manager descargó el driver de Chrome solo; no se instaló nada a mano.

## 3. Robots, términos y incidencias

| Sitio | robots.txt | Resultado |
|---|---|---|
| escale.minedu.gob.pe | No existe (HTTP 404) | No declara restricciones. Términos de uso: **no localizados ni leídos**. |
| umc.minedu.gob.pe | Solo `Disallow: /wp-admin/` | Permitido para páginas y PDFs. Términos de uso: **no localizados ni leídos**. |
| repositorio.minedu.gob.pe | Segundo grupo `User-agent: *` con `Disallow: /` (línea 151) | **Prohíbe el acceso automatizado general. No se usará.** |
| sicrece.minedu.gob.pe | No hay robots real (devuelve la página de la app) | Sin reglas declaradas. Términos de uso: no localizados. |
| utile.sistemasumc.com | 404 | Sin reglas declaradas. |

Incidencias:
- `https://umc.minedu.gob.pe` falla (certificado autofirmado y cierre de conexión, `ERR_HTTP2_PROTOCOL_ERROR`
  en Chrome). **Por `http://umc.minedu.gob.pe` funciona.** Todo el reconocimiento de UMC se hizo por HTTP;
  no se envió ninguna credencial ni dato personal.
- `https://sistemas15.minedu.gob.pe:8888/` (enlace "SICRECE" en UMC) no respondió (timeout).
- La portada de ESCALE enlaza a `http://11.35.92.170/padron/...`, una IP interna no accesible.

## 4. ESCALE: método real y ruta de clics

Portal Liferay. Método dominante: **(c) enlace directo a archivo**, navegando una biblioteca de
documentos con carpetas por año y paginación de 25 archivos por página.

Ruta: Inicio → ARCHIVO DE DATOS (`/bases-de-datos`) → "UE >>" (`/uee`) → carpeta **A. Censo Educativo**
(`.../GMv7/view/10481`) → carpeta del año → botón "Siguiente" para ver todas las páginas → clic en el
nombre del archivo (página de detalle con tamaño y versión) → "Descargar".

Enlace directo de descarga (confirmado en dos archivos):
`https://escale.minedu.gob.pe/documents/10156/{idCarpetaAnio}/{archivo}.zip`

La carpeta A. Censo Educativo tiene carpetas de **2004 a 2025**.

| Año | idCarpeta | Archivos (páginas) | Diccionario local ("LE") | Archivos de local / infobras |
|---|---|---|---|---|
| 2022 | 7802615 | 72 (3 págs): 68 zip + 4 pdf | `00_Diccionario de Datos LE 2022.pdf` | 22 |
| 2023 | 8520583 | 53 (3 págs): 49 zip + 4 pdf | `00_Diccionario de datos LE 2023.pdf` | 23 |
| 2024 | 9538443 | 65 (3 págs): 61 zip + 4 pdf | `00_Diccionario de datos_LE_2024.pdf` | 23 |
| 2025 | 10632985 | 79 (4 págs): 75 zip + 4 pdf | `00_Diccionario de datos_LE_2025.pdf` | 22 |

Cada año incluye además: diccionario CE, diccionario CE resultados, diccionario marco censal, `00_Padron.zip`
(2025 agrega `00_Padlocal.zip`), matrícula, docentes, cédulas lineales y subcarpetas "Cedulas censales en PDF"
(todos los años) y "Presentaciones" (2022 y 2023; no aparece en 2024 ni 2025).

Archivos de local relacionados con infraestructura (nombres exactos vistos):

- **2022:** `34_Local_Lineal_01/02`, `35_Local_Niveles`, `37_Local_Topografico`, `40_Local_Internet`,
  `41_Local_Servicios_Basicos`, `42_Local_Sec302`, `43_Local_Sec303`, `44_Local_Sec400`, `45_Local_Sec500`,
  `46_Local_Sec600`, `47_Local_Sec605`, `48_Local_Sec700`, `49-51_Local_Recursos_801/802/803`, `62_Local_Sec901`.
- **2023:** `31_Loc_Lineal_1`, `32_Loc_Lineal_2`, `39_Loc_P200_ServBa`, `41_Loc_P302_Cerco`, `43_Loc_P401_Edific`,
  `44_Loc_P501_Aulas`, `47_Loc_P701_SsHh`, `49_Loc_P802_Equip`, entre otros.
- **2024:** `40_Loc_Lineal_1`, `41_Loc_Lineal_2`, `42_Loc_12_infobra`, `48_Loc_P200_ServBa`, `52_Loc_P401_Edific`,
  `53_Loc_P501_Aulas`, `56_Loc_P701_SSHH`, entre otros.
- **2025:** `00_Padlocal`, `51_Loc_lineal_1`, `52_Loc_lineal_2`, `55_loc_p214_infobra`, `62_Loc_P53_Edific`,
  `63_Loc_P61_Aulas`, `66_loc_p81_sshh`, entre otros. **No hay archivo con nombre de servicios básicos**;
  puede estar dentro de `Loc_lineal_1/2` (por confirmar con el diccionario LE 2025 en la Fase 1).

Tamaños observados (página de detalle): `48_Loc_P200_ServBa.zip` 2024 = 1.386,2 KB;
`51_Loc_lineal_1.zip` 2025 = 8.632,6 KB. La fecha mostrada en el detalle (04/02/25 y 23/03/26) es la de
publicación del archivo, **no** la fecha de corte del dato.

Existen archivos llamados `*_infobra*` (2024 y 2025). Podrían enlazar el censo con INFOBRAS (obras); no se
abrieron.

Otras secciones de ESCALE revisadas:

- **Magnitudes** (`/magnitudes`): asistente de 4 pasos (año 2008-2025; magnitud; forma de presentar; ámbito
  con departamento, provincia, distrito, DRE, UGEL) y botón "Obtener cuadro". Método **(a) página
  interactiva con filtros**. Solo se vieron 6 cuadros (matrícula, docentes, personal no docente, servicios
  educativos, y dos de matrícula por edad/grado). **No se vio ningún cuadro de infraestructura del local**,
  aunque el texto introductorio menciona "locales educativos". No se ejecutó ninguna consulta.
- **Indicadores / Serie desde 2016** (`/ueetendencias2016`): texto indica Excel descargable con valores
  provinciales y distritales; **no se localizó el control de descarga**. Sin agua/desagüe/electricidad.
- **Padrón de servicios educativos** (`/web/inicio/padron-de-iiee`): filtros de nombre, códigos (IE, modular,
  local), departamento/provincia/distrito, DRE/UGEL, gestión, nivel, forma de atención y estado. Lista
  servicios, no infraestructura. No se ejecutó la búsqueda.
- **Estadística Online** (`/censo-escolar-eol/`): solo "Cédulas borrador" y "Pasos" (portal de recojo de
  datos del censo, no de consulta).

## 5. ENLA / UMC: método real

Portal WordPress en `http://umc.minedu.gob.pe`. Métodos: **(c) enlaces directos** a PDF
(`/wp-content/uploads/...`), **(c) enlaces a Google Drive** para bases, y **(d) contenido cargado por
JavaScript** en SICRECE y en visores embebidos (iframes de `utile.sistemasumc.com` y Calaméo).

Ruta: Inicio → Evaluaciones → Evaluaciones nacionales (`/enla/`) → "Resultados {año}"; o Inicio →
Resultados (`/uresultados/`).

| Año | Evaluación | URL de resultados | Qué hay |
|---|---|---|---|
| 2022 | EM 2022 (muestral) | `/resultadosem2022/` | Reporte nacional, presentación, factores asociados, habilidades socioemocionales, reporte técnico (PDF); bases `2P/4P/6P/2S_EM_2022.zip` por enlaces bit.ly |
| 2023 | ENLA 2023 | `/resultadosenla2023/` | Resumen ejecutivo, 3 presentaciones, reporte técnico (PDF); bases en Drive: muestral 2P, 4P, 2S; censal 4P EIB |
| 2024 | ENLA 2024 | `/resultadosenla2024/` | Reporte técnico `RT_ENLA2024.pdf`, infografías (PDF); bases en Drive: censal 4P, muestral 6P; remite a SICRECE |
| 2025 | ENLA 2025 | `/resultadosenla2025/` | `Resultados-ENLA-2025-Primaria.pdf`, `...-Secundaria.pdf`, `Recursos-ENLA-2025.pdf`; bases en Drive: muestral 4P, 4P EIB, 2S, 2S EIB, 5S, 5S EIB; remite a SICRECE |
| 2026 | ENLA 2026 | — | Ordenada (R.M. 285-2026-MINEDU) y dejada sin efecto. **Sin resultados.** |

Años suspendidos (fuera del rango pero relevantes): EM 2021, ECE 2020, ECE 2017.

**SICRECE** (`https://sicrece.minedu.gob.pe/#/home`): aplicación Angular. Perfiles que requieren sesión
(Especialista, Directivo, Docente, Familia/Estudiante, vía `identidad.minedu.gob.pe`) y "ACCESO PÚBLICO".
Al elegir acceso público aparece un cuestionario "¿Cuál es tu rol?" con botón "Ingresar". En el reconocimiento no se envió;
**después el usuario lo autorizó** (rol "Estudiante de pregrado") y se exploró: el perfil público tiene las pestañas "Resultado regional",
"Búsqueda avanzada" (tipo de evaluación, año, nivel, grado, áreas y ámbito NACIONAL/DRE) y "Biblioteca de descargas". La muestral cubre 2018, 2019 y
2022 a 2025; la censal 2007 a 2016, 2018, 2019 y 2024. Los resultados se dibujan en un gráfico `<canvas>`; los datos llegan al navegador como JSON
(ver `reglas_datos.md`). Es el método (d) del inventario: datos cargados por JavaScript.

## 6. Tabla de inventario

| Fuente | Año | Ruta de clics | Filtros | Formato de salida | Disponible | Observaciones |
|---|---|---|---|---|---|---|
| ESCALE Archivo de Datos | 2022 | Archivo de Datos → UE → A. Censo Educativo → 2022 → págs 1-3 | Ninguno (listado paginado) | .zip (contenido interno por confirmar) + PDF | Sí | 72 archivos; servicios básicos = `41_Local_Servicios_Basicos` |
| ESCALE Archivo de Datos | 2023 | ... → 2023 → págs 1-3 | Ninguno | .zip + PDF | Sí | 53 archivos; `39_Loc_P200_ServBa` |
| ESCALE Archivo de Datos | 2024 | ... → 2024 → págs 1-3 | Ninguno | .zip + PDF | Sí | 65 archivos; `48_Loc_P200_ServBa` (1,4 MB) |
| ESCALE Archivo de Datos | 2025 | ... → 2025 → págs 1-4 | Ninguno | .zip + PDF | Sí | 79 archivos; sin archivo de servicios básicos explícito; `00_Padlocal` nuevo |
| ESCALE Magnitudes | 2008-2025 | Magnitudes → año → magnitud → forma → ámbito → Obtener cuadro | Año, depto, prov, distrito, DRE, UGEL | Cuadro en pantalla (exportación no verificada) | Parcial | Sin cuadro de infraestructura visto |
| ESCALE Indicadores | 2016-2025 | Indicadores → Serie desde 2016 | Ninguno visto | Excel (control no localizado) | Parcial | Sin agua/desagüe/electricidad |
| UMC | 2022 (EM) | Evaluaciones → Evaluaciones nacionales → EM 2022 | Ninguno | PDF + .zip (bit.ly) | Sí | Muestral; regional por confirmar |
| UMC | 2023 (ENLA) | ... → ENLA 2023 | Ninguno | PDF + .zip (Drive) | Sí | Resumen ejecutivo y presentaciones |
| UMC | 2024 (ENLA) | ... → ENLA 2024 | Ninguno | PDF + .zip (Drive) + SICRECE | Sí | Resultados detallados remiten a SICRECE |
| UMC | 2025 (ENLA) | ... → ENLA 2025 | Ninguno | PDF Primaria/Secundaria + .zip (Drive) + SICRECE | Sí | Último año con resultados |
| UMC | 2026 | — | — | — | **No** | ENLA 2026 dejada sin efecto |
| SICRECE | 2007-actual | sicrece.minedu.gob.pe → Acceso Público → rol → Ingresar | No explorados | JavaScript (Angular) | No confirmado | Pide formulario de rol |
| Repositorio MINEDU | — | — | — | — | **No usar** | robots.txt prohíbe bots |

## 7. Pendiente de confirmar o decidir

1. **SICRECE acceso público:** pide elegir un rol antes de entrar. ¿Autorizas elegir "Estudiante de
   pregrado" (es tu rol real) y pulsar "Ingresar"? Sin eso no se sabe si SICRECE ofrece resultados por región.
2. **Formato interno de los .zip de ESCALE** (.sav, .dbf, .csv): se verá en la Fase 1 con un solo archivo.
3. **¿Los PDFs de ENLA 2025 traen tablas por región, grado, urbano/rural?** Solo se vio el enlace. No hay
   confirmación de resultados urbano/rural ni de que existan los 26 valores regionales por año.
4. **Cobertura ENLA:** gran parte de las bases son muestrales (2P, 4P, 2S, 5S...). Si la muestra permite
   resultados regionales no está verificado.
5. **Microdatos en Drive:** las bases ENLA son de estudiantes. Para cumplir la regla de no guardar datos
   personales conviene evitarlas si los PDFs o SICRECE ya dan los porcentajes regionales.
6. **Términos de uso** de ESCALE y UMC: no se localizaron. Conviene revisarlos antes de la Fase 2.
7. **Descarga desde Google Drive** con Selenium puede pedir pasos adicionales; no se probó.

## 8. Capturas (`docs\capturas\`)

`escale_01` a `escale_14` (inicio, UE, bases de datos, años del censo 2022-2025 y sus páginas, indicadores,
magnitudes, estadística online, serie 2016, padrón, detalle de archivos), `umc_01` a `umc_08` (inicio, ENLA,
resultados, suspensiones, EM 2022, ENLA 2023-2025) y `sicrece_01` a `sicrece_03`.
