# Inventario de datos del proyecto

Generado automaticamente por `src/inventario_datos.py` (2026-11-14). Cifras leidas de los archivos.

## Tablas finales (data/processed)

| tabla | fuente | que_es | una_fila_por | filas | columnas | periodo |
|---|---|---|---|---|---|---|
| escale_infraestructura | ESCALE (Censo Educativo) | Infraestructura de locales educativos publicos: servicios basicos, ruralidad, riesgo estructural | distrito y año | 7546 | 13 | 2022 a 2025 |
| enla_regiones | SICRECE (MINEDU-UMC) | % de estudiantes en nivel Satisfactorio en Lectura y Matematica | region, año, grado y evaluacion | 234 | 6 | 2022 a 2025 |
| mef_f12b_obras | MEF (Portal de Datos Abiertos) | Devengado, PIM, ultimo devengado y problematica de cada obra (por CUI), del Formato 12-B | CUI | 3742 | 16 | 2018-05-21 11:22:07 a 2026-11-10 21:41:25 |
| escale_obras_en_local | ESCALE (Censo Educativo 2025) | Locales que declaran estar en construccion, con el CUI de la obra | local | 923 | 8 | 2025 a 2025 |
| dashboard_obras | PRODUCTO FINAL | EL CSV UNICO para Power BI: obras, cortes de la Contraloria, series por departamento y pais, causales y contexto (filtrar por tipo_registro) | tipo_registro (obra, corte, departamento...) | 5053 | 110 | 2022-06-30 a 2026-11-11 |
| obras_maestra | PRODUCTO FINAL | Una fila por obra de Educacion/Cultura (429): INFOBRAS + ubigeo + Contraloria + MEF + ESCALE + causa | obra | 429 | 93 | 2026-11-11 |
| resumen_region | PRODUCTO FINAL | Una fila por region ENLA (26): obras paralizadas, causas, Contraloria, ESCALE y ENLA | region | 26 | 44 | 2025 |
| serie_pais_educacion | PRODUCTO FINAL | Cifras oficiales por corte: pais y sector Educacion (con la cifra corregida) | corte | 21 | 12 | 2022-06-30 a 2026-06-30 |
| serie_educacion_departamento | PRODUCTO FINAL | Obras de Educacion por departamento y corte (anexos Excel) | corte y departamento | 310 | 9 | 2023-09-30 a 2026-06-30 |
| causales_por_corte | PRODUCTO FINAL | Causales oficiales por corte con el grupo de causa del proyecto | corte y causal | 264 | 11 | 2022-06-30 a 2026-06-30 |
| enla_niveles_logro | SICRECE (MINEDU-UMC) | Los 4 niveles de logro (previo al inicio, en inicio, en proceso, satisfactorio) en Lectura y Matematica | region, año, grado, evaluacion y area | 468 | 12 | 2022 a 2025 |
| enla_pdf | PDF de la EM 2022 (MINEDU-UMC) | Lo mismo que enla_regiones, leido del PDF; trae tambien 2019 | region, año, grado y area | 208 | 9 | 2019 a 2022 |
| fichas_infobras | INFOBRAS (Contraloria) | Obras educativas en estado Paralizada: ubicacion, entidad, montos, avance, causal, dias paralizada, grupo de causa | obra | 198 | 37 | 2026-10-27 |
| cifras_oficiales_contraloria | Informes de obras paralizadas (Contraloria) | Cifras oficiales: total nacional, por sector (incluye Educacion) y por departamento | corte y ambito (pais, sector, departamento) | 686 | 21 | 2022-06-30 a 2026-06-30 |
| contraloria_causales | Informes de obras paralizadas (Contraloria) | Causales de paralizacion declaradas por las entidades, con obras y montos | corte y causal | 264 | 12 | 2022-06-30 a 2026-06-30 |
| contraloria_distribuciones | Informes de obras paralizadas (Contraloria) | Nivel de gobierno, rango de costo y rango de avance fisico | corte y categoria | 415 | 13 | 2022-06-30 a 2026-06-30 |
| contraloria_educacion_departamento | Anexos Excel (Contraloria) | Obras de Educacion paralizadas por departamento | corte y departamento | 310 | 10 | 2023-09-30 a 2026-06-30 |
| contraloria_obras_corte | Anexos Excel (Contraloria) | Datos por obra y corte: causal oficial, nivel de gobierno, sector, avance fisico, tipo, año de inicio, plazo, provincia, distrito, evento, CUI | obra y corte (13 cortes) | 30348 | 27 | 2023-09-30 a 2026-06-30 |
| contraloria_obras_panel | Anexos Excel (Contraloria) | Panel historico por obra: primer y ultimo corte, numero de cortes, si sigue, reingresos y avance por corte | obra | 5020 | 32 | 2023-09-30 a 2026-06-30 |
| contraloria_pim | Informes de obras paralizadas (Contraloria) | Obras con y sin presupuesto (PIM) por departamento y total nacional | corte y departamento (o nacional) | 104 | 18 | 2025-09-30 a 2026-06-30 |
| contraloria_modalidad_ejecucion | Informes de obras paralizadas (Contraloria) | Obras y costo por modalidad de ejecucion y nivel de gobierno | corte, tabla, modalidad y nivel | 556 | 13 | 2023-02-28 a 2026-06-30 |
| contraloria_evento_infobras | Informes de obras paralizadas (Contraloria) | Obras y costo por evento registrado en INFOBRAS y nivel de gobierno | corte, evento y nivel | 208 | 13 | 2023-02-28 a 2026-06-30 |
| contraloria_servicios_control_total | Informes de obras paralizadas (Contraloria) | Servicios de control efectuados por tipo (previo, simultaneo, posterior) | corte y tipo de servicio | 63 | 8 | 2022-06-30 a 2026-06-30 |
| contraloria_servicios_control_nivel_gobierno | Informes de obras paralizadas (Contraloria) | Servicios de control por tipo y nivel de gobierno | corte, tipo y nivel | 252 | 10 | 2022-06-30 a 2026-06-30 |
| contraloria_servicios_control_departamento | Informes de obras paralizadas (Contraloria) | Servicios de control por departamento y tipo (2023 en adelante) | corte y departamento | 450 | 11 | 2023-02-28 a 2026-06-30 |
| contraloria_principales_obras | Anexos Excel (Contraloria) | Principales obras paralizadas por departamento (entidad, costo, causal, modalidad) | obra y corte | 5954 | 18 | 2023-09-30 a 2026-03-31 |
| citas_educacion | Informes de obras paralizadas (Contraloria) | Oraciones de los informes sobre educacion, con archivo y pagina | oracion | 10 | 6 | 2022-09-30 a 2025-03-31 |
| frecuencia_terminos | Informes de obras paralizadas (Contraloria) | Terminos y pares de terminos mas frecuentes por año | año, tipo y termino | 400 | 6 | 2022 a 2026 |
| infobras_avances | INFOBRAS (Contraloria) | Avances mensuales de cada obra: fisico programado y real, estado del mes (B1) | obra y mes | 12858 | 10 | 2010 a 2026 |
| infobras_paralizaciones | INFOBRAS (Contraloria) | Meses en estado Paralizado de cada obra, agrupados en tramos, con causal, fecha y dias (B2) | obra y mes paralizado | 8739 | 17 | 2010 a 2026 |
| infobras_fichas_ampliadas | INFOBRAS (Contraloria) | Ficha actual de las 198 obras paralizadas y de las obras de Educacion de la Contraloria que ya no estan como Paralizada, con su estado (A4) y ubigeo | obra | 429 | 34 | 2026-11-11 |

## Archivos descargados (data/raw, nunca se modifican)

| fuente | archivos | mb | anios |
|---|---|---|---|
| contraloria | 53 | 72.0 | 2022, 2023, 2024, 2025, 2026 |
| enla | 23 | 66.8 | 2022, 2023, 2024, 2025 |
| escale | 24 | 117.4 | 2022, 2023, 2024, 2025 |
| infobras | 2 | 10.9 | 2026 |
| mef | 1 | 180.1 | 2026 |

## Necesidades del proyecto y que cubrimos

| necesidad | estado | donde | comentario |
|---|---|---|---|
| Lista de obras educativas paralizadas (estado, monto, ubicacion) | SI | obras_maestra (infobras_fichas_ampliadas) | 429 obras: las 198 paralizadas en INFOBRAS al 27-oct + las de Educacion de la Contraloria (jun-2026); estado leido el 11-nov-2026 (179 siguen paralizadas). Es una foto, no una serie |
| Serie historica de obras paralizadas por obra | PARCIAL | contraloria_obras_corte, contraloria_obras_panel; infobras_avances | Contraloria: 13 cortes (sep-2023 a jun-2026); antes solo cifras agregadas de los PDF. INFOBRAS: avance mensual de cada una de las 429 obras |
| Cifras oficiales para validar la base (pais, Educacion, departamento) | SI | cifras_oficiales_contraloria | 21 cortes; INFOBRAS y la Contraloria son poblaciones distintas (198 vs 341 obras de Educacion, 110 en comun; ver hallazgos_pdf.md) |
| Causas de paralizacion | SI | obras_maestra.causa_grupo_final / causa_macro; contraloria_causales | Por obra: NLP con 3 fuentes (causal oficial, comentarios de INFOBRAS, problematica del MEF); 417 de 429 con causa. Comentarios y causal oficial coinciden en 49 % de las obras con ambas |
| Montos (costo actualizado, saldo, expediente tecnico) | SI | cifras_oficiales_contraloria, contraloria_obras_corte, obras_maestra | 98 filas de la Contraloria con costo 0 o vacio y 9 con saldo mayor que el costo (marcadas, sin corregir) |
| Gasto devengado por obra (MEF) | PARCIAL | mef_f12b_obras, obras_maestra | Formato 12-B por CUI: 361 de las 414 obras con CUI valido aparecen; 15 tienen CUI NO ASOCIADO |
| Tiempo de paralizacion | SI | infobras_paralizaciones, obras_maestra | Las 429 obras: meses paralizados agrupados en tramos, con fecha y dias (8 739 meses; detalle leido del primer y ultimo mes de cada tramo). Los PDF no lo traen |
| Nivel de gobierno | PARCIAL | contraloria_obras_corte; contraloria_distribuciones | Por obra solo en las obras de la lista de la Contraloria; en INFOBRAS solo el nombre de la entidad |
| Departamento / provincia / distrito de cada obra | SI | obras_maestra (ubigeo, latitud, longitud) | Ubigeo INEI en las 429 (4 corregidas a mano: INFOBRAS traia mal la ubicacion). Coordenadas en 412; 17 no las tienen en INFOBRAS |
| Infraestructura escolar por distrito | SI | escale_infraestructura, escale_distrito_ampliado | 5 indicadores 2022 a 2025; 16 indicadores mas solo para 2025 |
| Aprendizajes (ENLA) por region | SI | enla_regiones, enla_niveles_logro, enla_pdf | 2022 a 2025 (+2019 en enla_pdf); solo por region (no hay UGEL ni distrito); SICRECE no devolvio 3 combinaciones de año y grado |
| Texto citable de los informes | PARCIAL | citas_educacion | Pocas citas: los informes hablan poco de educacion |
| Presupuesto asignado (PIM) por departamento | PARCIAL | contraloria_pim | Solo 4 cortes (set-2025 a jun-2026): los informes anteriores no traen la tabla |
| Datos de ESCALE o ENLA de 2026 | NO | - | Aun no publicados |

SI = cubierto; PARCIAL = hay algo pero con limites (ver comentario); NO = no tenemos.
Detalle de columnas: `docs/diccionario.csv`. Validaciones y limites: `docs/hallazgos_pdf.md`.
