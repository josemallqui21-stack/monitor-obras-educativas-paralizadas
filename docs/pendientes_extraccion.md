# Estado de las tareas de extracción (2026-11-12)

Todas las tareas de extracción anteriores están **hechas**, salvo las que se indican como «no hecho». El detalle de cada una está en
`docs/hallazgos_pdf.md` (sección 10) y en `docs/cambios_infobras.md`.

| # | Tarea | Estado | Dónde |
|---|---|---|---|
| A1 | Ubigeo de cada obra de INFOBRAS | **Hecho** | `ubigeo`, `ubigeo_metodo` en `fichas_infobras`; revisión en `docs/nombres_sin_ubigeo.csv` |
| A2 | Datos por obra de los anexos Excel | **Hecho** | `contraloria_obras_corte.csv` |
| A3 | Panel histórico por obra | **Hecho** | `contraloria_obras_panel.csv` (desde sep-2023) |
| A4 | Qué pasó con las 231 obras | **Hecho** | `infobras_fichas_ampliadas.csv` |
| B1 | Avances mensuales de INFOBRAS | **Hecho** | `infobras_avances.csv` |
| B2 | Historial de paralizaciones | **Hecho**, detalle por tramo | `infobras_paralizaciones.csv` |
| B3 | PIM por departamento y sector | **Hecho** | `contraloria_pim.csv` |
| B4 | Modalidad, evento y servicios de control | **Hecho** | `contraloria_modalidad_ejecucion.csv`, `contraloria_evento_infobras.csv`, `contraloria_servicios_control_*.csv` |
| B5 | Rangos de 2022 | **Hecho** | `contraloria_distribuciones.csv` |
| B6 | Principales obras | **Hecho** | `contraloria_principales_obras.csv` |
| B7 | Serie corregida de Educación | **Hecho** | `obras_educacion_corregida` en `cifras_oficiales_contraloria.csv`; `pais_educacion_corte` en el CSV único |
| B8 | Informes nuevos de la Contraloría | **Hecho** (revisado el 2026-11-12): el último es el de junio de 2026 | — |
| C1 | Gasto devengado por obra (MEF) | **Hecho**: Formato 12-B por CUI | `mef_f12b_obras.csv` |
| C2 | Más variables de ESCALE | **Hecho para 2025** (16 indicadores por distrito); 2022-2024 no (cambian los nombres de variable) | `escale_distrito_ampliado.csv`, `docs/catalogo_variables_escale.csv`, `escale_obras_en_local.csv` |
| C3 | ENLA: más niveles, grados y geografía | **Hecho** para todos los grados que devuelve SICRECE (2.°, 4.° y 6.° de primaria; 2.° de secundaria) y los 4 niveles de logro; UGEL/provincia y 5.° de secundaria: el portal no responde | `enla_regiones.csv`, `enla_niveles_logro.csv` |
| C4 | Servicios de control (anexo 03) | **Hecho** (corte mar-2026): conteos por obra | `contraloria_servicios_control_obra.csv` |
| D1 | NLP de causas de paralización | **Hecho**: reglas + modelo de apoyo + macro-categorías | `src/nlp_causas.py`, `docs/nlp_causas_metricas.csv` |
| D2 | CSV único para el dashboard | **Hecho** | `data/final/dashboard_obras.csv` |
| D3 | Auditoría de calidad | **Hecho**: 0 errores | `src/auditoria_calidad.py`, `docs/auditoria_calidad.csv` |

## Lo que sigue abierto (decisiones, no extracción)
1. ¿Se vuelve a leer INFOBRAS? Cambiaría el listado y los números del producto (ver `docs/producto_final.md`).
2. ¿Se necesitan los indicadores ampliados de ESCALE también para 2022-2024? Exige mapear los nombres de variable de cada año.
3. ¿Hace falta ENLA por UGEL o provincia? SICRECE no respondió a esa consulta.
4. Construir las páginas del dashboard en Power BI con el CSV único (la guía de uso está en `docs/producto_final.md`).
