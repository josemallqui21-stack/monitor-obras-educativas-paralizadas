# Documentación técnica del proyecto

Monitor de obras de infraestructura educativa paralizadas en el Perú (USMP, Data Analytics).

Este documento reúne en un solo lugar cómo se obtuvieron los datos, con qué reglas se prepararon, cómo se validaron, qué contiene el producto final, cuáles son sus límites y qué cambios tuvo el proyecto. Las tablas, el diccionario de variables y los resultados de cada validación están en los archivos CSV de la carpeta `docs/`.

**Contenido**

1. [Fuentes y obtención de datos](#fuentes)
   - [Portales y método de descarga](#fuentes-portales)
   - [Restricciones de acceso y reglas de cortesía](#fuentes-restricciones)
   - [Datos disponibles y cobertura](#fuentes-cobertura)
2. [Reglas de preparación](#reglas)
   - [ESCALE: infraestructura por distrito](#reglas-escale)
   - [ENLA: aprendizajes por región](#reglas-enla)
   - [INFOBRAS y ubicación de las obras](#reglas-infobras)
   - [MEF: gasto por obra](#reglas-mef)
   - [Clasificación de las causas de paralización](#reglas-causas)
   - [Protección de datos personales](#reglas-datos-personales)
3. [Validación y hallazgos](#validacion)
   - [Lectura de los informes PDF](#validacion-pdf)
   - [Contraste con los anexos Excel](#validacion-excel)
   - [Errores encontrados en las fuentes](#validacion-errores-fuente)
   - [INFOBRAS frente a la lista de la Contraloría](#validacion-infobras)
   - [Comprobaciones del producto y auditorías](#validacion-producto)
   - [Reproducibilidad](#validacion-reproducibilidad)
4. [Producto final](#producto)
   - [Estructura del CSV único](#producto-estructura)
   - [Las 429 obras](#producto-obras)
   - [Uso en Power BI](#producto-powerbi)
   - [Cómo reproducirlo](#producto-reproducir)
5. [Límites del dato](#limites)
   - [Lo que no existe en la fuente](#limites-fuente)
   - [Lo que el portal no entregó](#limites-portal)
   - [Lo que quedó fuera del alcance](#limites-alcance)
   - [Cuidados al interpretar](#limites-interpretacion)
6. [Cambios y pendientes](#cambios)
   - [Lectura ampliada de INFOBRAS (8 de noviembre)](#cambios-infobras)
   - [Cierre del proyecto (12 de noviembre)](#cambios-cierre)
   - [Correcciones finales (13 de noviembre)](#cambios-correcciones)
   - [Decisiones abiertas](#cambios-pendientes)

---

<a id="fuentes"></a>
## 1. Fuentes y obtención de datos

<a id="fuentes-portales"></a>
### 1.1 Portales y método de descarga

El proyecto trabaja con cinco fuentes públicas: ESCALE (Censo Educativo del MINEDU), ENLA (evaluaciones de aprendizaje de la UMC), los informes de obras paralizadas de la Contraloría, el portal INFOBRAS y el Formato 12-B del MEF. Antes de programar cualquier descarga, el 23 de octubre de 2026 el equipo hizo un reconocimiento de cada portal con un navegador Chrome visible controlado por Selenium, y anotó la ruta de clics, el formato de los archivos y las restricciones de acceso.

En ESCALE los datos están en la sección "Archivo de Datos", dentro de la carpeta del Censo Educativo, como archivos `.zip` por año (2004 a 2025). El portal no ofrece indicadores ya calculados de agua, desagüe o electricidad, por lo que se calcularon desde los archivos de local. Como los nombres de esos archivos cambian cada año (por ejemplo, servicios básicos se llama `41_Local_Servicios_Basicos` en 2022 y `48_Loc_P200_ServBa` en 2024), el programa los busca por patrón y no por nombre fijo. Solo se descargaron los archivos necesarios: 20 de alrededor de 270.

Para ENLA, el sitio de la UMC publica reportes en PDF y bases de estudiantes en Google Drive, pero no tablas regionales descargables. Los resultados por región se obtuvieron del sistema SICRECE, a través de su acceso público con el rol "Estudiante de pregrado", que el equipo autorizó expresamente. SICRECE dibuja los resultados en un gráfico; el programa elige los filtros en pantalla y guarda la respuesta de datos (JSON) que la propia página recibe. No se usaron credenciales, microdatos de estudiantes ni OCR.

De la Contraloría se descargaron desde gob.pe 21 informes de obras paralizadas (junio de 2022 a junio de 2026) y 32 anexos en Excel. De INFOBRAS se leyó el listado de obras de Educación en estado "Paralizada" y la ficha pública de cada obra. Del MEF se descargó el Formato 12-B desde su portal de datos abiertos.

<a id="fuentes-restricciones"></a>
### 1.2 Restricciones de acceso y reglas de cortesía

Se revisó el `robots.txt` de cada sitio. El repositorio institucional del MINEDU prohíbe el acceso automatizado, por lo que no se usó, aunque habría simplificado la obtención de ENLA. ESCALE no publica `robots.txt` y la UMC solo bloquea su zona de administración. No se encontraron los términos de uso de ESCALE ni de la UMC.

El sitio de la UMC solo funciona por `http://`, porque su certificado HTTPS está roto; el navegador automatizado se configuró para confiar únicamente en ese origen. Todas las descargas usan un identificador visible ("Proyecto academico USMP - Data Analytics"), pausas aleatorias de 2 a 5 segundos, una sola sesión a la vez y un máximo de tres reintentos. Si una fuente falla, el programa toma una captura, lo registra y continúa con la siguiente. Cada archivo descargado queda anotado en `docs/registro_fuentes.csv` (509 registros) y los archivos originales de `data/raw` nunca se modifican.

<a id="fuentes-cobertura"></a>
### 1.3 Datos disponibles y cobertura

ESCALE cubre de 2022 a 2025 a nivel de distrito. ENLA tiene resultados de 2022 (muestral), 2023 (muestral), 2024 (censal, solo 4.° de primaria) y 2025 (muestral), a nivel de región; la ENLA 2026 fue convocada y luego dejada sin efecto. La Contraloría aporta cifras agregadas por corte desde junio de 2022 y datos obra por obra desde septiembre de 2023, que es el primer corte con anexo detallado. INFOBRAS es una lectura puntual del 27 de octubre y del 11 de noviembre de 2026, y el MEF corresponde a la descarga del 12 de noviembre de 2026.

En total el proyecto genera 28 tablas de apoyo en `data/processed` y un CSV único para el tablero. La relación completa de tablas, con sus filas y periodos, está en `docs/inventario_datos.csv`, y la descripción de cada columna en `docs/diccionario.csv` (685 columnas descritas).

---

<a id="reglas"></a>
## 2. Reglas de preparación

<a id="reglas-escale"></a>
### 2.1 ESCALE: infraestructura por distrito

La tabla `escale_infraestructura.csv` tiene una fila por distrito y año (7 546 filas). Se considera público un local que tiene al menos un servicio educativo de gestión pública en el padrón del mismo año, y activo si figura en ese padrón. Los locales del censo que no aparecen en el padrón quedan fuera porque no se pueden clasificar.

El porcentaje de locales con agua, desagüe y electricidad de red pública se calcula sobre los locales que tienen dato, no sobre el total. Si a un local le falta un servicio con certeza, cuenta como "sin los tres servicios" aunque otro dato esté vacío; si hay duda, queda como "sin dato". Los códigos de cada servicio cambian entre años (en 2025 los servicios pasaron a la tabla lineal), y la correspondencia por año está configurada en el código.

El censo no tiene una categoría de "reparación total". En su lugar se usan dos medidas del estado estructural de las edificaciones en uso: riesgo de colapso o riesgo estructural, y muros, columnas, vigas o techos en mal estado. Un local cuenta en cada medida si al menos una de sus edificaciones cumple la condición.

Los nombres de departamento, provincia y distrito se armonizan por ubigeo, porque la fuente de 2023 trae nombres truncados y caracteres dañados. Todos los nombres de lugares se guardan en mayúsculas y sin tildes (la Ñ se conserva), y los códigos como texto para no perder los ceros a la izquierda.

Para 2025 se agregaron 16 indicadores más por distrito, como internet, agua y luz todos los días, rampas, antigüedad y estado de los techos (`escale_distrito_ampliado.csv`), y una tabla de 923 locales que declaran tener una obra en construcción con su código CUI (`escale_obras_en_local.csv`).

<a id="reglas-enla"></a>
### 2.2 ENLA: aprendizajes por región

`enla_regiones.csv` contiene el porcentaje de estudiantes en nivel satisfactorio en Lectura y Matemática para las 26 regiones de SICRECE: las 23 regiones sin Lima, más Lima Metropolitana, Lima Provincias y Callao. `enla_niveles_logro.csv` trae los cuatro niveles de logro. Se valida que haya 26 regiones y que los cuatro niveles sumen 100 con un margen de 0,6 por redondeo.

Los valores de 2022 se compararon con las tablas del reporte nacional de la Evaluación Muestral 2022 y coincidieron en los 104 casos. La columna `evaluacion` distingue los años muestrales del censal (2024), que no son estrictamente comparables. SICRECE no permite el desglose urbano/rural cuando se consulta por región.

<a id="reglas-infobras"></a>
### 2.3 INFOBRAS y ubicación de las obras

De cada obra se leyó la ficha completa: estado, avance físico, montos, días paralizada, comentarios mensuales, avances y tramos de paralización. Como la ficha completa las coordenadas con JavaScript unos segundos después de abrirse, el lector espera a que desaparezca el aviso "Cargando coordenadas" antes de leerlas.

El ubigeo de cada obra se asignó comparando sus nombres de lugar con el maestro de distritos de ESCALE: 404 obras coincidieron de forma exacta, 21 después de normalizar el nombre y 4 se asignaron a mano con el motivo documentado en `docs/nombres_sin_ubigeo.csv`. En esas cuatro, INFOBRAS publicaba una ubicación errónea: dos obras figuraban en Huancavelica y son de Ica, y dos en Chavín de Huántar y son de Huanta. El departamento sigue al ubigeo corregido y el valor publicado se conserva en `departamento_infobras`.

<a id="reglas-mef"></a>
### 2.4 MEF: gasto por obra

El cruce con el MEF se hace por el código CUI de cada obra. Antes de integrarlo, el equipo exploró tres opciones (el Sistema de Seguimiento de Inversiones, la Consulta Amigable y el portal de datos abiertos) y eligió el Formato 12-B de datos abiertos, porque permite una descarga masiva sin consultar obra por obra. De él se toman el devengado acumulado, el PIM y la problemática declarada. El devengado mide avance financiero, no físico, por lo que no tiene por qué coincidir con el avance de INFOBRAS.

<a id="reglas-causas"></a>
### 2.5 Clasificación de las causas de paralización

La causa de cada obra se obtiene de tres fuentes: la causal oficial de la Contraloría, los comentarios de INFOBRAS de los meses paralizados y la problemática del MEF. Los textos se normalizan y se comparan con 14 grupos de palabras clave (12 causas y 2 grupos de estado, como "obra concluida"). Cada grupo suma un punto por el primer patrón encontrado y medio punto por cada patrón adicional, con un máximo de dos, para que ningún grupo gane solo por tener más palabras. En clima, conflictos sociales, controversias, pandemia e interferencias se descartan las menciones negadas (por ejemplo, "las condiciones climatológicas permiten la ejecución").

Las fuentes se combinan con pesos: causal oficial 3, comentarios del último tramo 2, MEF 1,5 y tramos anteriores 0,5. La causa principal es la de mayor puntaje, y se guardan hasta dos causas secundarias y un nivel de confianza (alta cuando dos fuentes coinciden). Para los gráficos, los grupos se resumen en 8 macro-categorías. No se forzó un equilibrio artificial entre categorías, porque las causas reales están concentradas en lo financiero y lo contractual, igual que en las cifras nacionales de la Contraloría.

Como respaldo hay un modelo TF-IDF con regresión logística (pesos balanceados por clase) que solo actuaría si las reglas no encuentran ninguna causa. En la versión final no clasificó ninguna obra. Su macro-F1 de 0,885 en validación cruzada de cinco pliegues mide cuánto reproduce las reglas, no su exactitud frente a una revisión independiente. Una revisión manual de 30 obras al azar encontró 28 clasificaciones coherentes y 2 discutibles (`docs/muestra_validacion_causas.csv`).

<a id="reglas-datos-personales"></a>
### 2.6 Protección de datos personales

Los comentarios de INFOBRAS y los textos del MEF incluyen a veces nombres de residentes, supervisores o ingenieros. El proyecto los elimina al leer cada texto, limpia lo ya guardado y no conserva los campos narrativos del MEF que no se usan. Una auditoría final revisa todas las tablas y detiene el proceso si encuentra un nombre; su resultado actual es cero hallazgos. Los datos crudos no se redistribuyen, porque el padrón de ESCALE y el archivo del MEF contienen datos de personas.

---

<a id="validacion"></a>
## 3. Validación y hallazgos

<a id="validacion-pdf"></a>
### 3.1 Lectura de los informes PDF

Se procesaron 39 PDF: 21 informes de la Contraloría, 14 documentos de ENLA y 4 diccionarios de ESCALE. Ninguno era un escaneo, así que no fue necesario el OCR. De 3 826 tablas detectadas se conservaron las que tienen cifras; cada valor extraído guarda el archivo, la página y el número de tabla de donde proviene. Los informes de 2022 no tienen tablas reconocibles, por lo que se leyeron desde el texto de la página, teniendo en cuenta que usan espacios como separador de miles y que algunos mapas expresan los montos en millones.

<a id="validacion-excel"></a>
### 3.2 Contraste con los anexos Excel

Los anexos Excel de la propia Contraloría son la única fuente independiente de los PDF, y se usaron para validarlos en los 13 cortes que tienen base obra por obra. Los totales nacionales de obras y costo coinciden con una diferencia máxima de 0,29 %, y 322 de las 325 cifras por departamento son idénticas (las otras tres difieren en menos de 0,3 %). De las 248 comprobaciones internas de los PDF solo falla una, que corresponde a un error del propio informe. De las 52 comparaciones con los Excel, 4 quedan fuera del 10 %, todas en los cortes de septiembre de 2023 y septiembre de 2025.

La serie oficial del sector Educación pasa de 231 obras paralizadas en junio de 2022 a un máximo de 413 en septiembre de 2024, y cierra en 337 obras en junio de 2026, con un costo actualizado de S/ 4 020 millones. En los dos cortes donde el PDF trae mal la cifra de Educación, la serie usa el valor del Excel y lo marca en la columna `educacion_corregida`.

<a id="validacion-errores-fuente"></a>
### 3.3 Errores encontrados en las fuentes

La validación permitió detectar errores en los propios informes de la Contraloría. En septiembre de 2025 la tabla de sectores tiene los rótulos cruzados: el PDF atribuye 73 obras a Educación cuando, según el Excel, son 196 (las 73 corresponden a Salud). En septiembre de 2024 la fila "Total" de la tabla de causales está copiada del informe de junio. En junio de 2023 la tabla de sectores suma 1 825 obras pero su total dice 1 826. En septiembre de 2023 el PDF agrupa los sectores de un modo que no se pudo reconstruir, con una diferencia de −12,7 % en Educación, y en junio de 2026 los niveles de gobierno aparecen intercambiados.

Ninguno de estos valores se corrigió en silencio: se conservan tal como vienen, se marcan como discrepancia y, donde existe, el producto usa la cifra del anexo Excel. También se encontraron inconsistencias en INFOBRAS. En 6 obras el avance físico del encabezado no coincide con el último avance de su propia tabla, y la causal oficial de la ficha casi nunca informa ("Catalogo de Obra" en 158 de 198 obras), por lo que la causa útil está en los comentarios libres.

<a id="validacion-infobras"></a>
### 3.4 INFOBRAS frente a la lista de la Contraloría

El criterio inicial era que la base propia no se apartara más de 10 % de la cifra oficial, y no se cumple. INFOBRAS marcaba 198 obras de Educación paralizadas el 27 de octubre de 2026, mientras que la lista de la Contraloría a junio de 2026 tiene 341, una diferencia de −41,9 %. Solo 110 obras están en ambas, y esas 110 coinciden en monto y departamento, lo que indica que la lectura es correcta y que se trata de poblaciones distintas: INFOBRAS refleja el estado del día de la consulta y la Contraloría el de su corte.

Para entender la diferencia, el 11 de noviembre se leyó la ficha de las 231 obras de la lista oficial que no figuraban paralizadas: 130 estaban en ejecución, 95 finalizadas, 5 sin ejecución y 1 paralizada. De las 88 obras de INFOBRAS que no están en la lista oficial, solo 8 se paralizaron después del corte; el motivo de las otras 80 no se pudo verificar. Por eso el producto trabaja con la unión de ambas fuentes (429 obras) y documenta el origen de cada una.

<a id="validacion-producto"></a>
### 3.5 Comprobaciones del producto y auditorías

El producto final pasa 43 comprobaciones automáticas sin fallos (`docs/validacion_final.csv`). Entre ellas: llaves sin repetir, ubigeo de seis dígitos, sumas regionales iguales a los totales, series iguales a los informes, coordenadas dentro del territorio peruano, menos de 10 % de obras sin causa reconocible y ninguna macro-categoría de causa por encima del 50 %. Las tablas de los anexos Excel tienen además 914 comprobaciones propias, de las cuales 56 no pasan por las inconsistencias de origen descritas arriba.

La auditoría de calidad del CSV único revisa estructura, códigos, rangos, fechas y consistencia entre tipos de registro, y detiene el proceso si encuentra un error. El resultado es cero errores y tres avisos que vienen de la fuente: 98 filas de la Contraloría con costo cero o vacío, 9 con saldo mayor que el costo y 206 obras con al menos una alerta de calidad. La auditoría de datos personales no encontró ningún nombre.

<a id="validacion-reproducibilidad"></a>
### 3.6 Reproducibilidad

El pipeline puede repetirse sin duplicar trabajo: lo que ya está descargado y es válido se omite, y una segunda corrida produce tablas idénticas, comprobado comparando la huella (hash) de cada archivo. El proyecto se probó también descomprimiendo el paquete en una carpeta nueva y ejecutando el cuaderno sin la carpeta `src`, con el mismo resultado. Las correcciones de cada integrante se aplicaron después de reproducirlas en una copia del proyecto y comparar las tablas celda por celda.

---

<a id="producto"></a>
## 4. Producto final

<a id="producto-estructura"></a>
### 4.1 Estructura del CSV único

El producto es un solo archivo, `data/final/dashboard_obras.csv` (UTF-8, separado por comas, 5 053 filas y 110 columnas), acompañado de su diccionario `dashboard_obras_diccionario.csv`. Está en formato largo: la columna `tipo_registro` indica qué representa cada fila, y siempre hay que filtrar por ella, porque los tipos no se suman entre sí.

| tipo_registro | filas | qué representa |
|---|---|---|
| `obra_infobras` | 429 | una obra de Educación/Cultura con todos sus datos |
| `obra_corte_contraloria` | 3 982 | una obra en un corte de la Contraloría (13 cortes, sep-2023 a jun-2026) |
| `departamento_corte` | 310 | obras de Educación por departamento y corte |
| `pais_educacion_corte` | 21 | sector Educación del país por corte |
| `pais_total_corte` | 21 | total nacional de todos los sectores por corte |
| `causal_corte` | 264 | causales oficiales por corte |
| `contexto_region` | 26 | indicadores de ESCALE y ENLA por región |

Las medidas comunes a todos los tipos son `n_obras`, `n_obras_paralizadas`, `costo_actualizado_soles` y `saldo_inversion_soles`. Las cinco tablas con las que se arma el archivo están en `data/interim/componentes`.

<a id="producto-obras"></a>
### 4.2 Las 429 obras

Las filas `obra_infobras` combinan las 198 obras que INFOBRAS marcaba paralizadas el 27 de octubre con las 231 obras de Educación de la lista de la Contraloría que ese día no lo estaban. Según la ficha leída el 11 de noviembre de 2026, 179 siguen paralizadas, 150 están en ejecución, 95 finalizaron y 5 no tienen ejecución. Las 179 paralizadas suman un expediente técnico de S/ 765 millones y una mediana de 190 días paralizadas, y se concentran en Puno, Cusco, Ayacucho, Cajamarca y Apurímac.

Cada obra trae su ubicación (todas tienen ubigeo y coordenadas para el mapa), estado y avance, la causal oficial y su causa clasificada, el gasto del MEF cuando el CUI aparece en el Formato 12-B (361 de 414 CUI válidos), los servicios de control de la Contraloría, los indicadores de ESCALE de su distrito y los resultados de ENLA de su región. La columna `alertas_calidad` señala los datos dudosos que vienen de la fuente sin modificar ningún valor. Entre las paralizadas, las causas principales son la falta de recursos financieros (39 %) y el incumplimiento contractual (21 %).

<a id="producto-powerbi"></a>
### 4.3 Uso en Power BI

El archivo se carga con Obtener datos, Texto/CSV. Las columnas `cod_departamento`, `ubigeo`, `codigo_infobras` y `cui` deben cambiarse a tipo texto para no perder los ceros. Cada página del tablero debe tener un filtro por `tipo_registro`, y para contar conviene usar `SUM(n_obras)` o `SUM(n_obras_paralizadas)` en lugar de contar filas. Para el mapa se usan `latitud_mapa` y `longitud_mapa`: 412 son las coordenadas exactas de INFOBRAS y 17 son aproximadas, identificadas en `coordenada_origen` para mostrarlas de forma distinta. Abrir el CSV con doble clic en Excel borra los ceros de los códigos; para R existe el script `docs/leer_en_R.R`.

<a id="producto-reproducir"></a>
### 4.4 Cómo reproducirlo

Con los datos crudos en `data/raw`, el comando `python src\pipeline_completo.py --sin-descarga` (o `ejecutar.bat --sin-descarga`) rehace todas las tablas y el CSV final en unos cinco minutos, sin consultar los portales. Sin esa opción, el programa también consulta ESCALE, ENLA, la Contraloría y el MEF. INFOBRAS solo se vuelve a leer si se pide de forma explícita (`--fuentes infobras`), porque cambia el listado y los números del producto. El cuaderno `notebooks/proyecto_completo.ipynb` contiene todo el código y reproduce el mismo proceso paso a paso.

---

<a id="limites"></a>
## 5. Límites del dato

<a id="limites-fuente"></a>
### 5.1 Lo que no existe en la fuente

Diecisiete obras no tienen coordenadas en INFOBRAS. Para el mapa se aproximan con el local escolar que declara el CUI de la obra o con el centro de los colegios del distrito; en las obras con coordenadas reales, ese método queda a unos 3 km de mediana. Antes de septiembre de 2023 la Contraloría solo publica cifras agregadas, sin detalle por obra. Además, 98 filas de la Contraloría traen costo cero o vacío, 3 obras sin ejecución tienen expediente técnico cero, y 53 obras no aparecen en el MEF (15 de ellas con CUI "NO ASOCIADO").

<a id="limites-portal"></a>
### 5.2 Lo que el portal no entregó

SICRECE no devolvió resultados para 6.° de primaria 2022, 2.° de primaria 2023 ni 5.° de secundaria 2025, después de tres intentos en cada caso. Tampoco respondió a las consultas por UGEL o provincia, por lo que ENLA solo está disponible por región.

<a id="limites-alcance"></a>
### 5.3 Lo que quedó fuera del alcance

Los 16 indicadores ampliados de ESCALE son solo de 2025, porque extenderlos a 2022–2024 exige mapear los nombres de variable de cada año; quedan 123 variables candidatas sin extraer. Del anexo de servicios de control solo se usó el corte de marzo de 2026, porque el de junio no se publicó. INFOBRAS no se actualizó después del 11 de noviembre.

<a id="limites-interpretacion"></a>
### 5.4 Cuidados al interpretar

Las fuentes describen momentos distintos: ESCALE y ENLA llegan a 2025, la Contraloría a junio de 2026 e INFOBRAS a noviembre de 2026. El estado de una obra cambia rápido: de las 198 obras paralizadas el 27 de octubre, 20 ya estaban en ejecución quince días después. La causal oficial puede ser antigua y los comentarios de INFOBRAS más recientes; cuando ambos dicen algo claro, coinciden solo en el 49 % de los casos.

En ESCALE, el año 2023 tiene un 8,5 % de locales públicos sin datos de servicios, lo que puede sesgar esa cifra, y el riesgo estructural de 2024 no es comparable con los demás años porque se declaró mucho menos. El devengado del MEF supera al costo en 41 obras y el avance físico difiere más de 30 puntos del de INFOBRAS en 61. Por último, que una región tenga más obras paralizadas y peores resultados de aprendizaje o de infraestructura no demuestra que una cosa cause la otra.

Un hallazgo que no es falta de datos: Loreto y Tumbes no tienen obras de Educación paralizadas en ninguna de las dos fuentes, aunque sí obras de otros sectores. En el mapa valen cero, no "sin dato".

---

<a id="cambios"></a>
## 6. Cambios y pendientes

<a id="cambios-infobras"></a>
### 6.1 Lectura ampliada de INFOBRAS (8 de noviembre)

Se incorporó el ubigeo de cada obra (módulo `ubigeo_obras.py`) y una lectura ampliada de INFOBRAS con los avances mensuales, el historial de paralizaciones y el estado actual de las 231 obras de la lista oficial. Como esa lectura se hizo en una fecha distinta, se guardó en tablas propias (`infobras_avances`, `infobras_paralizaciones`, `infobras_fichas_ampliadas`) sin reemplazar la lectura del 27 de octubre. En la misma etapa se exploraron las fuentes de gasto del MEF.

<a id="cambios-cierre"></a>
### 6.2 Cierre del proyecto (12 de noviembre)

Se unieron las entregas del equipo: datos por obra y panel histórico de la Contraloría, PIM, modalidad de ejecución, servicios de control y la serie corregida de Educación. Se integró el gasto del MEF, se ampliaron ESCALE y ENLA, se rehízo la clasificación de causas sobre las 429 obras y se construyó el CSV único con su auditoría de calidad. En esta revisión se corrigieron varios defectos: nombres de personas en comentarios libres, coordenadas que no se habían leído en 383 obras, códigos de departamento sin el cero inicial, la ubicación de cuatro obras, una tilde en "JUNÍN" y reglas de clasificación demasiado amplias.

<a id="cambios-correcciones"></a>
### 6.3 Correcciones finales (13 de noviembre)

Se agregaron las columnas `latitud_mapa`, `longitud_mapa` y `coordenada_origen` para que las 429 obras puedan ubicarse en el mapa, junto con dos comprobaciones nuevas de coordenadas (de 41 a 43). La comprobación de obras sin causa pasó a mostrar el tope real (42 obras, el 10 %). Los cambios se reprodujeron en una copia del proyecto: las 107 columnas anteriores quedaron idénticas y se ajustaron las coordenadas nuevas a seis decimales.

<a id="cambios-pendientes"></a>
### 6.4 Decisiones abiertas

Quedan cuatro decisiones: volver a leer INFOBRAS en una fecha acordada (por una sola persona, porque dos lecturas simultáneas ya generaron duplicados), extender los indicadores ampliados de ESCALE a 2022–2024, insistir en ENLA por UGEL o provincia si SICRECE llega a responder, y terminar las páginas del tablero en Power BI a partir del CSV único.
