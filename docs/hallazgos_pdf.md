# Hallazgos del proyecto PDF (informes de la Contraloría) e INFOBRAS

Fecha de la corrida: 2026-10-27. Todo se regenera con `python src\main_pdf.py` (fases 1 a 5) después de `python src\main.py --solo contraloria` y
`--solo infobras`. Los PDF originales no se modificaron. Las cifras de este documento salen de los CSV de `data/processed` y `docs`.

## 1. Resumen para quien tenga prisa

* Se leyeron **39 PDF** (21 informes de la Contraloría, 14 de ENLA y 4 diccionarios de ESCALE) y **no había ningún PPT**. Ninguno es un escaneo
  completo, así que **no se hizo OCR**.
* Los **totales nacionales** (obras y costo) de los informes coinciden con los anexos Excel de la propia Contraloría en 13 cortes con una
  diferencia máxima de 0,29 %. Las 325 cifras por departamento comparadas con el Excel coinciden en 322 casos.
* **Tu base de INFOBRAS no está dentro del ±10 % de la cifra oficial**: tiene 198 obras de Educación/Cultura paralizadas frente a 341 que lista la
  Contraloría a junio de 2026 (−41,9 %). Las 110 obras que están en ambas coinciden al 100 % en monto y departamento; la diferencia es de
  población, no de errores de lectura (sección 5).
* La **causal oficial de INFOBRAS casi no informa** ("Catalogo de Obra" en 158 de 198 obras y "-" en 38); la causa útil está en los comentarios libres,
  y la mitad de las obras (50,5 %) no escribió nada útil sobre la causa.
* Hay **errores en los propios informes** que quedan documentados (sección 4.3): rótulos desordenados en set-2025, totales mal copiados, etc.

## 2. Fase 1: inventario (`docs/inventario_pdf.csv`)

| fuente | texto | documentos | paginas |
|---|---|---|---|
| contraloria | seleccionable | 21 | 1191 |
| enla | mixto | 8 | 714 |
| enla | seleccionable | 6 | 246 |
| escale | mixto | 3 | 302 |
| escale | seleccionable | 1 | 79 |

* `seleccionable`: todas las páginas probadas tienen texto. `mixto`: alguna página no tiene texto (portadas y láminas con gráficos). **Ningún PDF es `escaneado`.**
* Páginas sin texto en los informes de la Contraloría: como máximo 1 por informe (la última o una de anexos). En ENLA son láminas con gráficos (hasta 15 en la
  presentación de resultados EM 2022). **No se usó OCR** y no hizo falta: las tablas regionales de ENLA existen en texto (sección 6).
* `n_tablas` del inventario es lo que pdfplumber detecta por página; el catálogo (Fase 2) cuenta las tablas ya unidas entre páginas.

## 3. Fase 2: texto y tablas (`data/interim/pdf/{informe}/`, `docs/catalogo_tablas.csv`)

Por cada PDF: `texto_pNN.txt`, `texto_completo.txt` y `tablas_pNN_tM.csv`. Criterios de limpieza (en el código de `src/tablas_pdf.py`):

1. Las celdas combinadas de los PDF llegan como `None`: se quitan y cada fila queda «compactada».
2. Solo se guardan tablas con números (≥ 2 celdas numéricas en alguna fila). Las demás (viñetas, cuadros de texto, fragmentos de encabezado) quedan
   en el catálogo como `descartada: sin numeros`: 3024 de 3826 detectadas.
3. El título es la línea «Tabla N. …» más cercana encima de la tabla; el tipo se asigna por palabras del título (no por el número, que cambia entre informes).
4. Una tabla sin título que empieza en la página siguiente a otra sin fila «Total» se une a ella (p. ej. la tabla por departamento ocupa dos páginas).
5. En las celdas se quitan saltos de línea, comas de miles, `S/` y `%`; los números con cero a la izquierda se dejan como texto. Los encabezados no van
   en el CSV sino en el catálogo (`encabezado`). Cada fila lleva `fuente_pdf`, `pagina` y `tabla_n`.

Tipo `continuacion` en el catálogo = tabla con números pero sin título que no se pudo unir a otra (cuadros de láminas de ENLA/ESCALE y listas de obras).

## 4. Fase 3: tablas finales y validación

### 4.1 Qué se produjo (`data/processed`)

| Tabla | Filas | Qué contiene |
|---|---|---|
| `cifras_oficiales_contraloria.csv` | 686 | por corte (21): total nacional, cada sector (incl. Educación) y cada departamento: obras, costo actualizado, saldo |
| `contraloria_causales.csv` | 264 | causales de paralización por corte (el catálogo de causales cambia entre informes) |
| `contraloria_distribuciones.csv` | 367 | nivel de gobierno, rango de costo y rango de avance físico por corte (2022: solo nivel de gobierno) |
| `contraloria_educacion_departamento.csv` | 310 | obras de Educación por departamento, calculadas con los anexos Excel (13 cortes) |
| `enla_pdf.csv` | 208 | % satisfactorio por región (26) desde el PDF de la EM 2022 (años 2019 y 2022) |
| `fichas_infobras.csv` | 198 | una fila por obra educativa paralizada, leída de INFOBRAS |

### 4.2 Serie validada (país y sector Educación)

| corte | obras país | costo país (mil millones S/) | obras Educación | costo Educación (millones S/) | ¿coincide con Excel? (Educación) |
|---|---|---|---|---|---|
| 2022-06-30 | 2346 | 29.73 | 231 | 1376 | sin Excel |
| 2022-09-30 | 2302 | 41.87 | 220 | 1448 | sin Excel |
| 2022-12-31 | 1879 | 21.6 | 155 | 938 | sin Excel |
| 2023-02-28 | 1751 | 22.78 | 151 | 808 | sin Excel |
| 2023-05-31 | 1609 | 22.65 | 136 | 717 | sin Excel |
| 2023-06-30 | 1826 | 24.09 | 267 | 1391 | sin Excel |
| 2023-07-31 | 2055 | 25.42 | 288 | 1479 | sin Excel |
| 2023-08-31 | 2010 | 26.98 | 284 | 1483 | sin Excel |
| 2023-09-30 | 2066 | 27.1 | 324 | 1686 | **NO** |
| 2023-10-31 | 2171 | 28.2 | 352 | 1726 | sí |
| 2023-12-31 | 2298 | 26.99 | 346 | 1622 | sí |
| 2024-03-31 | 2324 | 33.17 | 367 | 1933 | sí |
| 2024-06-30 | 2256 | 36.12 | 327 | 1924 | sí |
| 2024-09-30 | 2648 | 43.56 | 413 | 2592 | sí |
| 2024-12-31 | 2476 | 43.12 | 364 | 2274 | sí |
| 2025-03-31 | 2572 | 43.16 | 360 | 2234 | sí |
| 2025-06-30 | 2428 | 44.3 | 220 | 1628 | sí |
| 2025-09-30 | 2215 | 42.33 | 73 | 5057 | **NO** |
| 2025-12-31 | 2416 | 67.14 | 223 | 2108 | sí |
| 2026-03-31 | 2241 | 73.17 | 197 | 2803 | sí |
| 2026-06-30 | 2262 | 62.83 | 337 | 4020 | sí |

Fuente: `cifras_oficiales_contraloria.csv`. «Educación» es el sector **tal como lo agrupa cada informe** (en jun-2026 suma EDUCACION y EDUCACION/CULTURA).
No se interpretan saltos entre cortes (p. ej. el costo total sube en dic-2025): el Excel de la Contraloría trae los mismos valores, así que son oficiales.

Causales del último corte (2026-06-30), las 5 mayores:

| causal | obras | % de obras |
|---|---|---|
| FALTA DE RECURSOS FINANCIEROS Y LIQUIDEZ | 625 | 27.6 |
| INCUMPLIMIENTO DE CONTRATO | 592 | 26.2 |
| DISCREPANCIAS, CONTROVERSIAS Y ARBITRAJE | 185 | 8.2 |
| DEFICIENCIA EN EL EXPEDIENTE TECNICO | 164 | 7.3 |
| OTROS | 158 | 7.0 |

### 4.3 Discrepancias y errores encontrados (qué pasó y qué se hizo)

| Corte | Hallazgo | Tratamiento |
|---|---|---|
| 2023-06-30 | La tabla de sectores del PDF suma 1.825 obras y su fila Total dice 1.826. **Error del informe.** | Se conserva tal cual; es la única de las 242 comprobaciones internas que falla. |
| 2023-09-30 | Educación: PDF 324 obras, Excel 283 (−12,7 %); costo −11,3 %. El informe agrupa sectores de una forma que no se pudo reconstruir con las columnas del Excel. | Marcado `coincide_excel = FALSE` y `observacion`. Fuera del 10 %. |
| 2024-09-30 | La fila «Total» de la tabla de causales (2.256 obras) está copiada del informe de junio 2024; las causales sí suman 2.648. Además, en la tabla de avance físico una fila de 10 obras está rotulada «Total». | La primera se descarta y la segunda se conserva como categoría aparte (`FILA ROTULADA TOTAL EN EL PDF`). |
| 2025-09-30 | **Rótulos desordenados** en la tabla de sectores: el PDF pone Educación = 73, Agricultura = 196 y Salud = 287; el Excel dice Educación = 196, Agricultura = 287, Salud = 73. | La cifra de Educación del PDF (73) queda marcada `coincide_excel = FALSE`; usar 196 (ver `contraloria_educacion_departamento.csv`). Fuera del 10 %. |
| 2023-02-28 | pdfplumber perdió la primera fila (Loreto) de la segunda página de la tabla por departamento. | Se recuperó del texto de la página (se registra en el log). |
| 2023-12-31 | Una celda con espacio suelto (`2,849,716 ,176`). | Se lee como 2.849.716.176. |
| 2025-12-31 | «Falta de personal clave» tiene saldo mayor que su costo actualizado, y hay «Nulidad de oficio» con costo «-». | Se guarda como viene (guion = 0). Revisar antes de usar esos valores. |
| 2022 (3 informes) | pdfplumber no detecta las tablas; usan espacio como separador de miles; el mapa por departamento está en **millones de soles con 1 decimal** (set y dic; jun está en soles). | Lectura desde el texto de cada página; las cifras de los mapas de set/dic llevan `observacion` (precisión de 100 mil soles). Rangos de costo y avance de 2022 **no se leyeron**. |
| 2022 | Total nacional, nivel de gobierno, sector y causales de 2022 cuadran con el total del informe (diferencias de 0 a 2 soles). | — |

Comparación con los anexos Excel (`docs/validacion_excel.csv`): totales nacionales de obras y costo con diferencia máxima 0,29 %; por departamento,
322 de 325 cifras idénticas (las otras 3 difieren menos de 0,3 %). Los cortes sin base obra por obra en los anexos (los 3 de 2022 y los de feb a ago de 2023) no se
pudieron comparar.

## 5. Validación de tu base (INFOBRAS) contra la Contraloría (`docs/validacion_infobras.csv`)

| comprobacion | valor | detalle |
|---|---|---|
| obras Educacion/Cultura en la lista de la Contraloria | 341.0 | contraloria_2026_anexo_01_obras_paralizadas_junio_2026_2026-10-27.xlsx (corte 2026-06-30) |
| obras paralizadas de Educacion/Cultura en INFOBRAS | 198.0 | fichas leidas el 2026-10-27 |
| diferencia INFOBRAS vs Contraloria (%) | -41.9 | supera el 10 %: son poblaciones distintas (ver hallazgos) |
| obras presentes en ambas | 110.0 | mismo codigo INFOBRAS |
| de las comunes, monto del expediente tecnico igual (<=0.5 %) | 110.0 | de 110 |
| de las comunes, mismo departamento | 110.0 | de 110 |
| obras de INFOBRAS que no estan en la lista de la Contraloria | 88.0 | motivo no verificado; hipotesis: la lista de la Contraloria sigue su propio criterio (inventario MEF / Invierte.pe) y no el estado de INFOBRAS |
|   de ellas, paralizadas despues del corte | 8.0 | fecha_paralizacion > 2026-06-30 |
| obras de la lista de la Contraloria que INFOBRAS ya no marca Paralizada | 231.0 | motivo no verificado (reactivadas, concluidas u otro estado en INFOBRAS) |

* Las **110 obras en común** tienen el mismo monto de expediente técnico y el mismo departamento: la lectura de INFOBRAS es consistente con la fuente oficial.
* **No cumple el criterio de ±10 %.** Las poblaciones son distintas: INFOBRAS filtra «Estado = Paralizada» el día de la lectura (27-oct-2026), mientras que la
  lista de la Contraloría es de junio de 2026 y 231 de sus obras de Educación/Cultura ya no están marcadas como paralizadas en INFOBRAS; 88 obras
  paralizadas en INFOBRAS no están en la lista (solo 8 se paralizaron después del corte). **El motivo de las otras 80 no está verificado**; una hipótesis es que la
  Contraloría usa su propio criterio (inventario del MEF / Invierte.pe) y no el estado de INFOBRAS.
* Para comparar por departamento: `contraloria_educacion_departamento.csv` (cortes de la Contraloría) contra `fichas_infobras.csv`; el ejemplo está en `docs/leer_pdf_en_R.R`.
* Tiempo de paralización: **no aparece en los PDF**. En INFOBRAS, `dias_paralizado` (último avance paralizado) tiene mediana 134 días, mínimo 28 y máximo 4198.
* Otros avisos de INFOBRAS: 25 obras sin coordenadas; la obra 543835 tiene **dos registros para abril-2026** (avance 11,68 y 24,4), el encabezado muestra 24,4;
  el estado «Paralizada» es el de hoy, no el del corte.

## 6. ENLA por región desde los PDF (`enla_pdf.csv`)

* Solo el **reporte nacional de la EM 2022** trae las tablas «Resultados regionales según niveles de logro»: 4 tablas (lectura y matemática × 4.° primaria y
  2.° secundaria) con 26 regiones, que comparan **2019 y 2022** (208 filas = 26 × 2 × 2 × 2).
* Los reportes de ENLA 2023 y 2024 solo traen tablas de **cobertura** (instituciones y estudiantes evaluados), no de logros; los PDF de 2025 son resúmenes nacionales.
* Los 104 valores de 2022 son **idénticos** a los de SICRECE (`enla_regiones.csv`). Los valores de 2019 solo existen aquí. Lima Metropolitana y Lima Provincias
  van por separado (código de departamento 15 en ambas).

## 7. Fase 4: texto (opcional)

**Qué solo estaba en texto** (y se decidió extraer): (a) frases sobre educación en la narrativa de los informes; (b) los términos más frecuentes; (c) el texto libre de INFOBRAS
(comentarios), que es donde está la causa real de cada obra. **Qué no se hizo y por qué:** no se usó spaCy ni scikit-learn (expresiones regulares y conteos bastan y son más
fáciles de auditar y corregir); no se extrajeron entidades de personas (regla de datos personales); no se afirma causalidad.

* `citas_educacion.csv`: 10 oraciones. Es poco porque **los informes dicen muy poco de educación en la narrativa**; casi todo
  está en tablas. Ejemplo citable: informe dic-2023, p. 15: «…seguido por el sector Educación con una inversión de S/ 166 millones con 36 obras paralizadas…».
* `frecuencia_terminos.csv`: 40 términos y 40 pares por año, sin palabras vacías.
* **Grupos de causa** (reglas en `config.CAUSAS_REGLAS`, visibles y editables). Resultado sobre las 198 obras:

| grupo de causa | obras | % |
|---|---|---|
| sin_informacion | 100 | 50.5 |
| recursos_financieros | 30 | 15.2 |
| otros | 29 | 14.6 |
| incumplimiento_contractual | 17 | 8.6 |
| materiales_logistica | 7 | 3.5 |
| obra_concluida_o_en_marcha | 5 | 2.5 |
| controversias_arbitraje | 3 | 1.5 |
| pandemia | 2 | 1.0 |
| conflictos_sociales | 2 | 1.0 |
| clima | 2 | 1.0 |
| expediente_tecnico | 1 | 0.5 |

* Prueba de las reglas: aplicadas a las 13 causales oficiales de la Contraloría dan el grupo esperado en **13 de 13**.
* Muestra aleatoria de 30 (`docs/muestra_validacion_causas.csv`, revisada a mano): **27 coinciden con mi lectura** y 3 son discutibles (dos obras con causal declarada
  «Transporte» cuyo comentario habla de otra cosa, y una con «observaciones técnicas» y «recursos económicos deshabilitados»). Esto es una revisión informal, no una validación experta.
* **'otros' = 14,6 %** (límite del proyecto: 25 %). Son comentarios con contenido pero sin causa reconocible (notas de avance, «obra culminada por administración directa», etc.).
  **'sin_informacion' = 50,5 %**: «No se registraron comentarios», «Obra paralizada», etc. No es un fallo de las reglas sino del dato.
* Mejoras posibles: si se quiere bajar 'otros', agregar reglas para notas administrativas (cierre de oficio, nueva gestión); y no tratar la causal «Transporte» como causa (aparece en 2 obras).

## 8. Límites y lo que falta

* Modalidad de ejecución, evento INFOBRAS y servicios de control se extrajeron a `data/interim/pdf` pero **no se consolidaron** en tablas finales (sus tablas tienen celdas vacías
  legítimas y cambian de forma entre informes).
* Los rangos de costo y avance físico de 2022 no se leyeron. Lista de «principales obras por departamento» (2022-set 2025): disponible por informe en `data/interim/pdf`, sin consolidar.
* Los cortes de 2022 y los de feb a ago de 2023 no tienen anexo Excel con base obra por obra: no se pudo hacer la comparación independiente.
* Las cifras de la Contraloría son de seguimiento de obras con CUI; no comparar directamente con el censo de ESCALE.

## 9. Cómo reproducir

```
cd C:\data_analytic
.venv\Scripts\python.exe src\main.py --solo contraloria
.venv\Scripts\python.exe src\main.py --solo infobras
.venv\Scripts\python.exe src\main_pdf.py            (segunda vez: omite lo ya hecho, ~30 s)
```

Prueba hecha el 2026-10-27: se borraron todas las salidas del proyecto PDF y se regeneraron desde `data/raw`: **13 de 14 huellas idénticas** (la restante es
`validacion_infobras.csv`, cuyo texto de explicación se suavizó después de guardar la huella). En la segunda corrida: 0 documentos reprocesados, 39 omitidos.

## 10. Cierre del proyecto (2026-11-12)

### 10.1 Qué se incorporó después de la revisión inicial
* **Trabajo del equipo** (revisado y unido el 2026-11-12): ubigeo de cada obra (198/198), lectura ampliada de INFOBRAS (429 fichas con todos los avances
  y paralizaciones), datos por obra y panel histórico de la Contraloría (13 cortes, 5020 obras), PIM, modalidad, evento, servicios de control, principales obras y rangos de 2022.
* **MEF (Formato 12-B):** devengado por CUI (`mef_f12b_obras.csv`); 361 de 414 obras con CUI válido aparecen.
* **ESCALE:** locales que declaran estar en construcción con el CUI de la obra (`escale_obras_en_local.csv`; 923 locales, 32 obras de nuestra tabla vinculadas) y catálogo de las 331 variables
  de los archivos descargados (`docs/catalogo_variables_escale.csv`; 123 podrían describir infraestructura y no se usan).
* **ENLA:** los 4 niveles de logro por región (`enla_niveles_logro.csv`, 364 filas) a partir de los mismos JSON de SICRECE.
* **ESCALE ampliado, ENLA con más grados y anexo 03:** 16 indicadores de infraestructura por distrito (2025), 2.° y 6.° de primaria de ENLA (SICRECE) y los servicios de control por obra del anexo 03 de la Contraloría.
* **Auditoría de calidad** (`src/auditoria_calidad.py`, `docs/auditoria_calidad.csv`) y columna `alertas_calidad` en el CSV único.
* **NLP de causas rehecho** (`src/nlp_causas.py`): ahora usa los comentarios de INFOBRAS de las 429 obras (antes solo 198), combina las tres fuentes con pesos, detecta varias causas, aplica negación,
  agrega un modelo de apoyo con pesos por clase y macro-categorías; las menciones sin causa («no hay restricciones», «obra concluida») ya no caen en «otros» (33 → 11 obras).
* **Producto final:** un solo CSV para el dashboard (`data/final/dashboard_obras.csv`); ver `docs/producto_final.md`.

### 10.2 Errores encontrados y corregidos
| Qué | Cómo se corrigió |
|---|---|
| **Nombres de personas** en comentarios libres de INFOBRAS (supervisores y residentes de 2 obras) y, sobre todo, en los textos narrativos del MEF (decenas de ingenieros) | Filtro `utils.omitir_nombres` al leer cada comentario, limpieza de lo ya guardado, **no se guardan** los campos narrativos del MEF que no se usan y una **auditoría** (`datos_personales.auditar`) que detiene el proceso si encuentra algún nombre en las tablas. Resultado actual: 0 hallazgos |
| **Coordenadas perdidas** en 383 de las 429 obras: la ficha de INFOBRAS dice «Cargando coordenadas…» y las rellena con JavaScript 1 a 3 s después de abrir | El lector espera a que desaparezca el aviso (`esperar_carga`); las que faltaban se completaron (`--coordenadas`): ahora 412 de 429 obras tienen. Las 17 restantes no tienen coordenadas en INFOBRAS |
| `cod_departamento` sin cero a la izquierda (`1` en vez de `01`) en `fichas_infobras.csv` | Se lee como texto y se completa a 2 dígitos |
| 2 obras (135083 y 543835) que INFOBRAS publica en Huancavelica y son de Ica | `departamento` y `cod_departamento` siguen al ubigeo; lo que publica INFOBRAS queda en `departamento_infobras` |
| «JUNÍN» con tilde en `escale_obras_en_local` | Nombres de lugares sin tildes en todas las tablas (la Ñ se conserva) |
| Decimales largos (`56.910000000000004`) | Los CSV se guardan redondeados a 4 decimales |
| Clasificación de causas: reglas demasiado amplias («social», «profesionales», «financiero»), comentarios «no hay restricciones» en «otros», clima detectado en «las condiciones climatológicas permiten…» | Reglas más precisas, grupos de estado, negación y puntaje por grupo con tope |
| Informes PDF con errores (rótulos desordenados en set-2025, totales copiados de otro informe, niveles de gobierno intercambiados en jun-2026) | Registrados en las secciones 4.3 y siguientes; el producto usa la cifra del anexo Excel donde el PDF está mal |

### 10.3 Lo que respondió el equipo
* De las 231 obras de la Contraloría que INFOBRAS no marcaba paralizadas el 27-oct, el 11-nov están: {'EN EJECUCIÓN': 130, 'FINALIZADO': 95, 'SIN EJECUCIÓN': 5, 'PARALIZADA': 1}.
* De las 198 que sí lo estaban el 27-oct, el 11-nov están: {'PARALIZADA': 178, 'EN EJECUCIÓN': 20}. **INFOBRAS cambia rápido: es una foto.**
* Las 198 obras aparecen en algún corte de la Contraloría; 896 obras del panel aparecen en un solo corte y 925 salieron de la lista y volvieron a entrar.

### 10.4 Lo que no se hizo y por qué
* **ENLA por UGEL o provincia y 5.° de secundaria:** el portal SICRECE no devolvió respuesta para esas combinaciones (3 intentos); los grados que sí devuelve están todos.
* **ESCALE ampliado para 2022-2024:** los nombres de las variables cambian cada año; los 16 indicadores nuevos son solo de 2025. Quedan en el catálogo las demás variables (123 candidatas).
* **Fechas de inicio/fin de obra de ESCALE:** vienen cortadas en el propio archivo del Censo; no se publican.
* **Cortes de la Contraloría anteriores a sep-2023:** no tienen anexo con base por obra; solo existen las cifras agregadas de los PDF. El anexo 03 (servicios de control) solo se usa del corte de marzo de 2026 (el de junio no lo publica).
* **Actualizar INFOBRAS:** es una decisión aparte (`--fuentes infobras` o `python src/scraper_infobras.py --ampliado`, una sola persona, ~2,5 h); cambia el listado y los números del producto.
