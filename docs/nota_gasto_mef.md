# C1. ¿El MEF tiene el gasto devengado por obra (CUI)?

Estado: exploración (2026-11-08). No se descargó nada ni se programó nada.

## Respuesta corta

**Sí.** El MEF publica el devengado de cada inversión identificada por su **CUI**, y `fichas_infobras.csv` ya trae el CUI de cada obra, así que el cruce sería directo (CUI = CUI). Lo que todavía no está confirmado es **si existe una descarga masiva (CSV) con el CUI**, o si hay que consultar obra por obra.

## Fuentes encontradas

| Fuente | Qué trae por CUI | Acceso | ¿Descarga masiva? |
|---|---|---|---|
| **Sistema de Seguimiento de Inversiones (SSI)**, https://ofi5.mef.gob.pe/ssi/ | Costo total, **devengado acumulado**, saldo por ejecutar, primer y último devengado, **devengado mensualizado por año**, PIA/PIM/certificado/compromiso por año, enlace a INFOBRAS | Público (se busca por CUI o código SNIP); los operadores entran con usuario | No: una consulta por CUI (página web). Automatizarla = scraping: revisar `robots.txt` y términos antes |
| **Consulta Amigable** (MEF, Transparencia Económica) | PIA, PIM, devengado y girado por año; se puede bajar hasta el nivel de proyecto | Público | Parcial: exporta tablas, pero navegando nivel por nivel |
| **Portal de datos abiertos del MEF** (datosabiertos.mef.gob.pe) | Por verificar: archivos anuales de ejecución del gasto que **podrían** traer la columna de producto/proyecto (CUI) y el devengado mensual | Público | **Por verificar.** Si existe, es la mejor opción: un CSV por año, sin navegador |

Fuentes de la información de la tabla: manuales y capacitaciones del MEF sobre el SSI (https://www.mef.gob.pe/contenidos/inv_publica/docs/capacitaciones/Capacitacion_2021_08_25.pdf y https://mef.gob.pe/contenidos/inv_publica/docs/Instructivo_BI/2025/Seguimiento_2_Manual_SSI.pdf). Hay tesis que ya cruzan INFOBRAS, Consulta Amigable y el SSI.

## Qué falta comprobar (checklist del cuaderno)

- [ ] Abrir datosabiertos.mef.gob.pe y buscar el conjunto de datos de ejecución del gasto: ¿trae una columna de proyecto (CUI)? ¿devengado mensual o anual? ¿desde qué año?
- [ ] Leer `robots.txt` y los términos de uso de ofi5.mef.gob.pe y de apps5.mineco.gob.pe (Consulta Amigable) **antes** de automatizar.
- [ ] Probar a mano en el SSI con 5 CUI de `fichas_infobras` (por ejemplo 2301257, 2389067, 2380222, 2193048, 2251248) y anotar si aparecen y si el devengado acumulado coincide con `monto_ejecucion_acumulado` de INFOBRAS.

## Cómo serviría

- Comparar el **devengado acumulado (MEF)** con el **monto de ejecución acumulado (INFOBRAS)** y con el costo actualizado de la Contraloría.
- Ver si una obra "paralizada" sigue devengando (gasto sin avance físico) o si dejó de recibir presupuesto.

## Riesgos

- El devengado del MEF es **financiero**; el avance de INFOBRAS es **físico**. No deben coincidir necesariamente.
- Si solo existe el SSI (una página por CUI), son ~430 consultas más: requiere el mismo cuidado que INFOBRAS (pausas, un solo navegador, y avisar antes).
