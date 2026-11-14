# Correcciones del 13-nov-2026

Probado sobre la carpeta del proyecto (`proyecto_codigo_y_docs_1.zip`): pasos 5 a 9 del pipeline con sus mismos datos procesados.
Resultado: **43 comprobaciones (0 fallan)**, auditoría de calidad **0 errores**, auditoría de datos personales **0 hallazgos**.
**Ninguna tabla cambió** (data/processed, componentes y dashboard_obras.csv comparados celda por celda): solo se agregan 3 columnas.

## Archivos modificados
| Archivo | Cambio |
|---|---|
| `src/inventario_datos.py` | Cuadro de necesidades actualizado (ubigeo, tiempo de paralización, causas y MEF ya están; cifras del 12-nov) |
| `src/producto_final.py` | Comprobación «obras sin causa»: el esperado muestra el tope real (42 = 10 %) y no 429. Nuevas columnas `latitud_mapa`, `longitud_mapa`, `coordenada_origen` en obras_maestra (función `coordenadas_mapa`) |
| `src/dashboard.py` | Las 3 columnas nuevas en el CSV único y su diccionario; 2 comprobaciones nuevas de coordenadas; sin PerformanceWarning (`reindex`) |
| `src/auditoria_calidad.py` | Las columnas de coordenadas nuevas se revisan como las de INFOBRAS (pueden ser negativas; deben caer dentro del Perú) |
| `generar_cuaderno.py` | La celda de preparación encuentra la carpeta del proyecto aunque VS Code no la tenga abierta; el texto del NLP aclara que el modelo no clasificó ninguna obra y que su F1 mide consistencia con las reglas; el texto de Power BI usa `latitud_mapa`; sección nueva «Límites y calidad del dato» |
| `docs/limites_y_calidad.md` | NUEVO: límites y calidad del dato con sus cifras |
| `docs/producto_final.md` | Menciones del mapa actualizadas |

## Coordenadas para el mapa
`latitud`/`longitud` NO cambian (siguen siendo las de INFOBRAS, 412 obras). Para las 17 sin coordenadas: el local de ESCALE 2025 que declara el CUI
de la obra (1 obra) o el centro de los colegios del distrito según el Padrón 2025 (16 obras). Probado con las obras que sí tienen coordenadas:
el centro del distrito queda a 3,2 km de mediana de la ubicación real (90 % a menos de 14 km).

## Falta (en la computadora que tiene todo data/raw)
El cuaderno va **regenerado sin resultados** (`python generar_cuaderno.py`). Para guardarlo con resultados y actualizar el inventario:
    python generar_cuaderno.py --ejecutar        (unos 8 minutos)
No se pudo ejecutar fuera de su computadora: el paso 2 rehace ENLA desde data/raw y faltaban los archivos de SICRECE y del MEF descargados después del 27-oct.


## Revisión del 13-nov (verificado antes de aplicar)
* Se reprodujo en una copia del proyecto: mismo CSV que el entregado (0 celdas distintas) y las 107 columnas anteriores sin cambios.
* Corrección adicional: `latitud_mapa` y `longitud_mapa` se guardaban con 4 decimales en el CSV único (hasta 5 m de diferencia); ahora 6, igual que `latitud` y `longitud`.
