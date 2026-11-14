# Cambios de la lectura ampliada de INFOBRAS y el ubigeo (A1, A4 + B1 + B2, C1) — 2026-11-08

## Archivos nuevos
| Archivo | Para qué |
|---|---|
| `src/ubigeo_obras.py` | A1: asigna `ubigeo` y `ubigeo_metodo` a cada obra (exacto / normalizado / manual) |
| `docs/nombres_sin_ubigeo.csv` | A1: las 13 obras que no coincidían exacto, cómo se resolvieron y por qué (se regenera solo) |
| `docs/nota_gasto_mef.md` | C1: nota sobre el devengado por CUI del MEF |
| `docs/cambios_mani.md` | este archivo |

## Archivos modificados (compartidos: revisar al juntar)
| Archivo | Cambio |
|---|---|
| `src/config.py` | bloque nuevo **al final**: «INFOBRAS, pasada ampliada». No cambia nada existente |
| `src/scraper_infobras.py` | `leer_ficha` ahora llama a `_leer_ficha` (mismo resultado); `descargar_listado` y `aplicar_filtros_y_buscar` aceptan filtros opcionales (sin argumentos hacen lo mismo que antes); sección nueva al final «Pasada ampliada» + `__main__` |
| `src/texto_nlp.py` | Fase 4: lee `ubigeo` como texto y llama a `ubigeo_obras.agregar_ubigeo` antes de guardar `fichas_infobras.csv` (2 líneas) |
| `src/main_pdf.py` | después de la Fase 4 llama a `scraper_infobras.construir_csv_ampliados()` (sin cache no hace nada) |
| `src/diccionario_pdf.py` | `ubigeo` y `ubigeo_metodo` en `fichas_infobras`; bloque nuevo con las 3 tablas de la pasada ampliada; lee `ubigeo` como texto |
| `src/inventario_datos.py` | 3 tablas nuevas al final de `TABLAS` |
| `notebooks/trabajo_mani.ipynb` | celdas de A1, A4+B1+B2 y C1 |

## Tablas
* `fichas_infobras.csv`: **2 columnas nuevas** (`ubigeo`, `ubigeo_metodo`, después de `distrito`). Las demás columnas y filas, iguales.
* Nuevas (aparecen solo después de correr la pasada por INFOBRAS): `infobras_avances.csv`, `infobras_paralizaciones.csv`, `infobras_fichas_ampliadas.csv` y `docs/validacion_infobras_ampliada.csv`.
* Las demás tablas de `data/processed` no cambian (comprobado comparando contra la versión del 2026-11-08).

## Para decidir
1. **4 obras con la ubicación mal en INFOBRAS** (543835 y 135083 dicen Huancavelica pero son de Ica; 510315 y 156196 dicen Chavín de Huántar pero son de Huanta). Solo se corrigió el ubigeo; `departamento` y `cod_departamento` siguen como los publica INFOBRAS, así que **dos obras cuentan en Huancavelica cuando son de Ica**. ¿Corregimos también el departamento?
2. La pasada ampliada lee las fichas **en una fecha nueva** (no el 27 de octubre). Por eso va en tablas aparte con su `fecha_lectura` y **no** reemplaza `fichas_infobras.csv`.
3. `escale_infraestructura.csv` guarda nombres con eñe (`CAÑETE`, `ICHUÑA`), contra la regla de «sin tildes». No lo toqué (no es mi parte).
