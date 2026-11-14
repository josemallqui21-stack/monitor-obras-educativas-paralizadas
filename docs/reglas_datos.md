# Reglas de datos

Estado: Fase 3 (extracción). Todo sale de `src/extraccion.py`; los datos crudos de `data/raw` no se modifican.

## 1. ESCALE: `data/processed/escale_infraestructura.csv`

Una fila por distrito (ubigeo de 6 dígitos) y año, 2022 a 2025: 7.546 filas (1.882, 1.886, 1.888 y 1.890 distritos por año).
Faltan los distritos sin ningún local público que respondiera el censo.

| Columna | Definición |
|---|---|
| `anio`, `ubigeo`, `departamento`, `provincia`, `distrito` | `CODGEO` y nombres de `Loc_Lineal_1` (el más frecuente por ubigeo). Los nombres vienen en mayúsculas y sin tildes, como en el origen |
| `n_locales_publicos` | Locales públicos, activos y que respondieron el censo |
| `n_locales_sin_dato` | De esos, los que no permiten saber si tienen los 3 servicios (columna agregada; no estaba en el pedido) |
| `pct_3_servicios` | % de locales con agua, desagüe y electricidad de red pública, **sobre los locales con dato** |
| `pct_sin_3_servicios` | 100 menos `pct_3_servicios` |
| `pct_rural` | % de locales rurales entre los públicos del distrito |
| `n_locales_con_dato_edif` | Locales públicos con al menos una edificación en uso que respondió la pregunta de riesgo (base de los dos indicadores siguientes) |
| `pct_riesgo_estructural` | % de esos locales con al menos una edificación en uso que declara **riesgo de colapso o riesgo estructural** |
| `pct_estructura_mal_estado` | % de esos locales con al menos una edificación en uso con **muros, columnas, vigas o estructura de techos en mal estado** |

### Nombres de departamento, provincia y distrito
La fuente no escribe igual los nombres en todos los años: 2023 trae nombres cortados (por ejemplo "MADRE DE DIO") y con la Ñ dañada, y algunos distritos
vienen con texto doblemente codificado ("CONSTITUCIÃ\x93N"). Por eso la tabla final **armoniza los nombres por ubigeo**: se repara el texto
doblemente codificado y cada código conserva el mismo nombre en todos los años (el más largo entre los que no tienen caracteres dañados).
Resultado: 0 códigos con más de un nombre y ningún carácter raro. Los nombres vienen en mayúsculas sin tildes, salvo los pocos que la fuente trae con tilde (CONSTITUCIÓN, EL TALLÁN).

### Universo
1. Locales presentes en `Loc_Lineal_1` (respondieron la ficha del censo).
2. **Público:** el local tiene al menos un servicio educativo con `GESTION` 1 (pública de gestión directa) o 2 (pública de
   gestión privada) en el padrón del mismo año. Coincide exacto con `GES_LOC = A` del Padlocal 2025 y con `GESTION` de
   las tablas lineales de 2022 y 2025. Los 27 a 35 locales mixtos (público y privado) cuentan como públicos.
3. **Activo:** el local aparece en el padrón del año. En 2025 el padrón trae `ESTADO` y el 100 % de los registros es "Activo";
   en 2022 a 2024 no hay columna de estado, y se **asume** que el padrón lista solo servicios activos.
4. Locales del censo que no están en el padrón (no se pueden clasificar) quedan fuera: 0 en 2022, 91 en 2023, 5 en 2024, 39 en 2025.
   Un local sin ubigeo en el archivo (uno en 2023 y uno en 2024) recibe el de otro local con el mismo departamento, provincia y
   distrito; si no existe, se excluye (el de 2023 no se pudo recuperar y no era público).
5. **Rural:** `AREA_CENSO` del padrón (1 urbana, 2 rural); coincide 100 % con `AREA_LOC` del Padlocal 2025.

### Servicios de red pública (código 1 en los tres, según el diccionario LE de cada año)

| Año | Archivo | Agua | Desagüe | Electricidad | Marca de "predominante" |
|---|---|---|---|---|---|
| 2022 | `Local_Servicios_Basicos` (tabla larga) | C202 | C206 | C207 | `TIPO = X` |
| 2023 | `Loc_P200_ServBa` (tabla larga) | C202 | C206 | C207 | `TIPO = X` |
| 2024 | `Loc_P200_ServBa` (tabla larga) | C202 | C212 | C216 | `PREDOMINA = X` |
| 2025 | columnas de `Loc_Lineal_1` | `P321` | `P3212` | `P3217` | no aplica |

- **Sin dato** (nunca se cuenta como "no tiene"): no hay fila predominante, el valor está vacío o es "-", o hay más de una fila predominante
  (ambiguo; en 2024 son 45, 37 y 10 locales en agua, desagüe y luz).
- Se usa lógica de tres valores: si a un local ya le falta un servicio con certeza, cuenta como "sin los 3 servicios" aunque otro dato falte.
- En 2025 la electricidad de red pública incluye el código 1 (empresa distribuidora) y el 2 (terceros), porque el diccionario
  de ese año llama "Red pública" a ambos. Efecto: 0,18 puntos porcentuales sobre el total nacional.
- `P311_*` (servicios del centro poblado) no se usa.

### Estado de la infraestructura: no existe `pct_reparacion_total`
En los datos **no hay una categoría "reparación total"**. Los campos "Necesitan reparación" del diccionario son de equipos
(extintores, recursos tecnológicos). Lo más cercano está en la tabla de edificaciones (una fila por edificación), que se descarga
junto con los demás archivos (`Local_Sec400` en 2022, `Loc_P401_Edific` en 2023 y 2024, `Loc_P53_Edific` en 2025):

| Dato | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Edificación en uso (solo se cuentan estas) | `P401_3` (SI/NO) | `P401_3` (1/2) | `P401_3` (1/2) | `P53_3` (1/2) |
| Riesgo de colapso o riesgo estructural | `P401_20` | `P401_19` | `P401_20` | `P53_20` |
| Estado de muros, columnas, vigas y techos | `P401_11_1C`, `_2C`, `_3C`, `_4C` | `P401_10_12`, `_22`, `_32`, `_42` | `P401_11_12`, `_22`, `_32`, `_42` | `P53_11_12`, `_22`, `_32`, `_42` |

Escala de estado: 01 Bueno, 02 Regular, 03 Mal estado (2025: BU, RE, MA). Los códigos 04, 05 y NA ("no tiene" o "no aplica") no cuentan
como mal estado. Un local cuenta como "en riesgo" o "en mal estado" si **alguna** de sus edificaciones en uso cumple la condición.
Son medidas del estado estructural, **no** una estimación de cuántos locales necesitan reparación total.

### Comparabilidad entre años (leer antes de comparar)
- **2023 tiene un hueco:** 4.669 locales públicos (8,5 %) no tienen ninguna fila de servicios en la base publicada, aunque su ficha lineal
  está completa. Quedan como "sin dato" y el porcentaje se calcula con los demás. Es probable que sesgue la cifra de 2023.
- **2024 cambió la pregunta** (nuevos códigos de cuadro y una marca `PREDOMINA` distinta).
- **2025 cambió de estructura** (columnas en la tabla lineal).
- Serie nacional ponderada de `pct_3_servicios`: 28,50 (2022), 27,00 (2023), 31,42 (2024), 32,77 (2025). La caída de 2023 puede ser un efecto del hueco.
  El `pct_rural` es estable (77,3 a 77,6 %).
- **`pct_riesgo_estructural` de 2024 no es comparable.** A nivel nacional baja a 15,0 % (25,2 / 25,5 / 15,0 / 25,9 en 2022-2025). No es un error de lectura:
  en 2024 la respuesta de riesgo se declara menos en todos los grupos. Entre las edificaciones con algún elemento en mal estado la declaran
  el 36 % (50 a 58 % en los demás años) y entre las que no tienen ninguno el 5 % (7 a 9 %).
- `pct_estructura_mal_estado` sube todos los años a nivel nacional (25,3 / 28,1 / 30,0 / 34,3 %). Puede ser un deterioro real o un cambio en cómo se responde; no se pudo distinguir.
- El hueco de 2023 es específico de la tabla de servicios: 3.228 de los 4.874 locales sin dato de servicios sí tienen datos de edificaciones.
- Para años nuevos sin configuración explícita se usa el formato de columnas de 2025 y se avisa en el log.

## 2. ENLA: `data/processed/enla_regiones.csv`

182 filas: 7 combinaciones de año, evaluación y grado, con **26 regiones** cada una. Columnas: `region`, `anio`, `grado`, `evaluacion`
(columna agregada, ver abajo), `lectura_satisfactorio`, `matematica_satisfactorio`.

| Año | Evaluación | Grados incluidos |
|---|---|---|
| 2022 | MUESTRAL (EM 2022) | 4.° primaria, 2.° secundaria |
| 2023 | MUESTRAL (ENLA 2023) | 4.° primaria, 2.° secundaria |
| 2024 | **CENSAL** (ENLA 2024) | 4.° primaria |
| 2025 | MUESTRAL (ENLA 2025) | 4.° primaria, 2.° secundaria |

### Fuente y método
- Fuente: **SICRECE, acceso público** (perfil público; rol "Estudiante de pregrado", autorizado por el usuario; sin credenciales).
  El scraper elige en pantalla tipo de evaluación, año, nivel y grado, marca Lectura, Matemática, ámbito DRE y "TODOS", y pulsa Buscar.
  Los números solo se dibujan en un gráfico `<canvas>` y en un PDF que es una imagen, así que se guarda en `data/raw/enla/{año}/` el **JSON que la propia
  página recibe** al buscar (`reporteGrafico_Publico_EMAmbitos_Nacional_DRE` para la muestral y `reporteGrafico_Publico_ECE_DRE` para la censal).
  No se llama a la API por cuenta propia ni se usa OCR.
- **Verificación:** los 104 valores de 2022 (26 regiones × 2 áreas × 2 grados) se compararon con las tablas en texto del reporte nacional EM 2022:
  coinciden todos (diferencia máxima 0,05).
- `lectura_satisfactorio` y `matematica_satisfactorio` son el % de estudiantes en nivel **Satisfactorio** de cada DRE. En cada región se valida que los
  cuatro niveles de logro sumen 100 (±0,6) y que haya 26 regiones.
- **Regla de Lima:** SICRECE usa una DRE por región: Lima Metropolitana, Lima Provincias y Callao aparte, tal como pide el proyecto. No se localizó la
  definición oficial de "Lima Metropolitana"; se asume que es la provincia de Lima.

### Advertencias
- **`evaluacion` distingue MUESTRAL de CENSAL.** En 2024 el 4.° de primaria solo existe como evaluación censal (todas las escuelas), mientras que los demás
  años son muestrales. Las cifras no son estrictamente comparables entre una y otra.
- **No hay columnas `lectura_rural` ni `matematica_rural`.** Al elegir el ámbito DRE, SICRECE desactiva los filtros de área geográfica (urbana/rural), gestión y característica:
  solo existen a nivel nacional.
- Otros resultados disponibles en SICRECE que no se piden: 2.° de primaria, 6.° de primaria (2024, muestral), 5.° de secundaria (2025), Ciencias Sociales y ámbito UGEL o distrito (censal).
- Los PDF de la UMC (reportes técnicos, presentaciones) se descargan como documentación, pero no se usan para esta tabla. En la presentación de 2023 las tablas regionales
  son imágenes, y las de los reportes técnicos de 2023 y 2024 son de cobertura de muestra, no de resultados.
