"""Proyecto completo, de inicio a fin, en un solo script (solo codigo, sin explicaciones).

Es el mismo flujo del cuaderno notebooks/proyecto_completo.ipynb (que si trae las explicaciones): descarga, tablas de ESCALE y ENLA,
datos personales, proyecto PDF, NLP de las causas, producto final, CSV unico del dashboard, diccionario y auditorias.
El codigo de cada modulo esta en src/ (config.py, utils.py, nlp_causas.py, producto_final.py, ...).

  python proyecto_completo.py        (o en VS Code: «Run Cell» en cada bloque «# %%»)

Este archivo lo genera generar_cuaderno.py desde el cuaderno: no se edita a mano.
"""
import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ_PROYECTO / "src"))


def ver(valor):
    """Muestra un resultado como lo haria el cuaderno (tablas completas hasta 40 filas); no imprime None."""
    if valor is None:
        return
    if hasattr(valor, "columns"):
        print(valor.to_string(max_rows=40, max_cols=30))
    elif hasattr(valor, "to_string"):
        print(valor.to_string(max_rows=40))
    else:
        print(valor)

# %% 0. Opciones
from types import SimpleNamespace

import pandas as pd

import auditoria_calidad
import catalogo_escale
import config
import datos_personales
import diccionario
import escale_ampliado
import inventario_datos
import main
import main_pdf
import nlp_causas
import pipeline_completo
import producto_final
import texto_nlp
import utils

pd.set_option("display.width", 200, "display.max_columns", 40, "display.max_colwidth", 70)

# ---------------- opciones ----------------
DESCARGAR = False          # True: consulta ESCALE, ENLA, Contraloría y MEF (Chrome visible + internet, ~15 min). False: usa data/raw tal como está
INCLUIR_INFOBRAS = False   # True: ADEMAS vuelve a leer INFOBRAS. Cambia el listado (hay obras que dejaron de estar paralizadas) y mueve los números
FORZAR = False             # True: rehace todo aunque ya esté hecho (muy lento)
TODO_DE_UNA_VEZ = False    # True: al final corre pipeline_completo.ejecutar() de nuevo (equivale a «python src/pipeline_completo.py»)

FUENTES = list(pipeline_completo.FUENTES_POR_DEFECTO) + (["infobras"] if INCLUIR_INFOBRAS else [])
ARGS = SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES)
print("Carpeta del proyecto:", config.RAIZ.name)
print("Descargar:", DESCARGAR, "| fuentes:", FUENTES)

# %% 1. Descarga de las fuentes
if DESCARGAR:
    main.descargar(ARGS)
else:
    print("DESCARGAR = False: no se consulta ningún portal. Lo que hay en data/raw:")
ver(inventario_datos.inventario_raw())

# %% 2. Tablas de ESCALE y ENLA
main.extraer(SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES))
catalogo = catalogo_escale.construir()
ampliado = escale_ampliado.construir()
ver(ampliado.head(3))

# %% 2. Tablas de ESCALE y ENLA
for nombre in ("escale_infraestructura", "escale_distrito_ampliado", "enla_regiones", "enla_niveles_logro"):
    t = pd.read_csv(config.PROCESSED / f"{nombre}.csv", dtype={"ubigeo": str}, encoding="utf-8-sig")
    print(f"{nombre}: {t.shape[0]} filas x {t.shape[1]} columnas | años: {sorted(int(a) for a in t.anio.unique())}")
niveles = pd.read_csv(config.PROCESSED / "enla_niveles_logro.csv", encoding="utf-8-sig")
ver(niveles.groupby(["anio", "evaluacion", "grado"]).size().rename("regiones x 2 áreas").reset_index())

# %% 3. Datos personales
ejemplos = ["SUPERVISOR DE OBRA: ING. JUAN PEREZ QUISPE RESIDENTE DE OBRA: MARIA LOPEZ RAMOS",
            "aprobada por el supervisor de obra, Ing. Walter Martos, cumple los requisitos",
            "NO SE TIENE ASIGNACIÓN PRESUPUESTAL PARA PROSEGUIR CON LA EJECUCIÓN",
            "con supervisión del Consorcio Supervisor Villa María"]
print(pd.DataFrame({"antes": ejemplos, "despues": [utils.omitir_nombres(e) for e in ejemplos]}).to_string())
ver(datos_personales.limpiar())

# %% 4. Proyecto PDF (fases 1 a 4)
ver(main_pdf.ejecutar(4, FORZAR))

# %% 4. Proyecto PDF (fases 1 a 4)
inv = pd.read_csv(config.INVENTARIO_PDF, dtype=str, encoding="utf-8-sig")
cat = pd.read_csv(config.CATALOGO_TABLAS, dtype=str, keep_default_na=False, encoding="utf-8-sig")
print(len(inv), "PDF |", len(cat), "tablas detectadas,", int((cat.estado == "guardada").sum()), "guardadas")
ver(inv.groupby(["fuente", "tipo_texto"]).agg(documentos=("archivo", "count"), paginas=("paginas", lambda s: s.astype(int).sum())))

# %% 4. Proyecto PDF (fases 1 a 4)
v = pd.read_csv(config.DOCS / "validacion_pdf.csv", encoding="utf-8-sig")
x = pd.read_csv(config.DOCS / "validacion_excel.csv", encoding="utf-8-sig")
a = pd.read_csv(config.DOCS / "validacion_anexos_excel.csv", encoding="utf-8-sig")
print(f"PDF: {len(v)} comprobaciones, {(~v.ok).sum()} falla (error del propio informe de jun-2023)")
print(f"PDF vs Excel de la Contraloría: {len(x)} comparaciones, {(~x.ok_10pct).sum()} fuera del 10 % (set-2023 y set-2025: errores del PDF)")
print(f"Panel y tablas de los anexos Excel: {len(a)} comprobaciones, {(~a.ok).sum()} no pasan (explicadas en docs/hallazgos_pdf.md)")
ver(pd.read_csv(config.DOCS / "validacion_infobras.csv", encoding="utf-8-sig"))

# %% 4.1 Texto narrativo de los informes (citas y términos)
terminos = pd.read_csv(config.PROCESSED / "frecuencia_terminos.csv", encoding="utf-8-sig")
print("Años:", sorted(int(a) for a in terminos.anio.unique()))
ver(terminos[(terminos.anio == terminos.anio.max()) & (terminos.tipo == "par")].head(8))

# %% 5. NLP de las causas de paralización
reglas = pd.DataFrame([(g, len(p), config.CAUSAS_MACRO[g], "estado" if g in config.CAUSAS_ESTADO else "causa") for g, p in config.CAUSAS_REGLAS.items()],
                      columns=["grupo", "patrones", "macro_categoria", "clase"])
ver(reglas)

# %% 5. NLP de las causas de paralización
pruebas = ["FALTA DE ASIGNACIÓN PRESUPUESTAL PARA CULMINAR LA OBRA",
           "Paralizada por lluvias intensas y deslizamiento del talud",
           "Las condiciones climatológicas permiten su ejecución sin ningún problema",
           "Se resolvió el contrato por incumplimiento y se inició el proceso arbitral",
           "NO EXISTE RESTRICCIONES A LA FECHA.",
           "El avance físico se determinó respecto al costo del Expediente Técnico"]
filas = []
for t in pruebas:
    r = nlp_causas.analizar([("texto", t, 1.0)])
    filas.append({"texto": t, "puntajes": nlp_causas.puntuar(nlp_causas.normalizar(t)), "principal": r["principal"], "secundarias": r["secundarias"]})
ver(pd.DataFrame(filas))

# %% 5. NLP de las causas de paralización
# Las 13 causales oficiales de la Contraloría deben caer en el grupo esperado (prueba de las reglas)
fallas = [(c, esperado, texto_nlp.clasificar_causa(c)) for c, esperado in texto_nlp.PRUEBA_REGLAS.items() if texto_nlp.clasificar_causa(c) != esperado]
print(f"{len(texto_nlp.PRUEBA_REGLAS) - len(fallas)} de {len(texto_nlp.PRUEBA_REGLAS)} causales oficiales caen en su grupo.", "Fallan:" if fallas else "", fallas or "")

# %% 5.1 Modelo de apoyo: entrenamiento y evaluación
par = pd.read_csv(config.PROCESSED / "infobras_paralizaciones.csv", dtype=str, keep_default_na=False, encoding="utf-8-sig")
mef = pd.read_csv(config.PROCESSED / "mef_f12b_obras.csv", dtype=str, keep_default_na=False, encoding="utf-8-sig")
textos_comentarios = [t for lista in nlp_causas.textos_de_infobras(par).values() for t, _ in lista]
modelo, metricas = nlp_causas.entrenar(textos_comentarios + list(mef.ult_problema))
print("Textos de entrenamiento: comentarios de INFOBRAS", len(textos_comentarios), "| problemáticas del MEF", int((mef.ult_problema != "").sum()))
ver(metricas)

# %% 6. Producto final y CSV único del dashboard
tablas, validacion = producto_final.construir()
print(f"{len(validacion)} comprobaciones, {(~validacion.ok).sum()} fallan")
ver(validacion[["tabla", "comprobacion", "valor", "esperado", "ok"]])

# %% 6.1 Resultado del NLP sobre las 429 obras
obras = tablas["obras_maestra"]
distribucion = pd.DataFrame({"obras": obras.causa_grupo_final.value_counts(), "paralizadas_hoy": obras[obras.paralizada_hoy].causa_grupo_final.value_counts()}).fillna(0).astype(int)
distribucion["macro_categoria"] = distribucion.index.map(config.CAUSAS_MACRO)
ver(distribucion.sort_values("obras", ascending=False))

# %% 6.1 Resultado del NLP sobre las 429 obras
macro = obras.groupby("causa_macro").agg(obras=("codigo_infobras", "count"), paralizadas_hoy=("paralizada_hoy", "sum"))
macro["% de obras"] = (100 * macro.obras / macro.obras.sum()).round(1)
print("Ninguna macro-categoría supera el 50 %:", macro["% de obras"].max() <= 50)
ver(macro.sort_values("obras", ascending=False))

# %% 6.1 Resultado del NLP sobre las 429 obras
print("Fuente que más aportó:", obras.causa_fuente.value_counts().to_dict())
print("Confianza:", obras.causa_confianza.replace("", "sin causa").value_counts().to_dict())
print("Método:", obras.causa_metodo.value_counts().to_dict())
# acuerdo entre fuentes: obras que tienen causa clara en dos fuentes a la vez
claras = lambda s: ~s.isin(["otros", "sin_informacion", "sin_restricciones", "obra_concluida_o_en_marcha"])
ambas = obras[claras(obras.causa_grupo_infobras) & claras(obras.causa_grupo_contraloria)]
print(f"Comentarios de INFOBRAS vs causal oficial: {len(ambas)} obras con causa clara en ambas; coinciden {100 * (ambas.causa_grupo_infobras == ambas.causa_grupo_contraloria).mean():.0f} %")

# %% 6.2 El CSV único
dashboard = pd.read_csv(config.FINAL / "dashboard_obras.csv", dtype={"cod_departamento": str, "ubigeo": str, "codigo_infobras": str, "cui": str, "escale_codlocal": str}, encoding="utf-8-sig")
print(dashboard.shape[0], "filas x", dashboard.shape[1], "columnas")
ver(dashboard.groupby("tipo_registro").agg(filas=("tipo_registro", "size"), n_obras=("n_obras", "sum"), desde=("fecha_corte", "min"), hasta=("fecha_corte", "max")))

# %% 6.2 El CSV único
# Ejemplos de cómo se filtra: obras paralizadas hoy por macro-categoría de causa, y evolución de Educación en el país
hoy = dashboard[(dashboard.tipo_registro == "obra_infobras") & (dashboard.paralizada_hoy == True)]
print(hoy.groupby("causa_macro").n_obras_paralizadas.sum().sort_values(ascending=False).to_dict())
ver(dashboard[dashboard.tipo_registro == "pais_educacion_corte"][["fecha_corte", "n_obras", "pct_obras", "educacion_corregida"]].tail(6))

# %% 6.2 El CSV único
# Avisos de calidad de las obras de INFOBRAS (la columna alertas_calidad no corrige nada: marca lo dudoso)
ob = dashboard[dashboard.tipo_registro == "obra_infobras"]
ver(ob.alertas_calidad.fillna("(sin alertas)").str.split("|").explode().value_counts().rename("obras"))

# %% 7. Diccionario, auditorías e inventario
dic = diccionario.escribir_diccionario()
print(dic.tabla.nunique(), "tablas,", len(dic), "columnas descritas")
hallazgos = datos_personales.auditoria_o_falla()
print("Auditoría de datos personales:", len(hallazgos), "hallazgos")
tablas_inv, raw_inv, necesidades = inventario_datos.construir()
ver(tablas_inv.drop(columns="archivo"))

# %% 7. Diccionario, auditorías e inventario
calidad = auditoria_calidad.auditoria_o_falla()
print("Errores:", int((calidad.nivel == "ERROR").sum()), "| avisos:", int((calidad.nivel == "aviso").sum()))
ver(calidad)

# %% 7. Diccionario, auditorías e inventario
ver(necesidades)

# %% Todo de una vez
if TODO_DE_UNA_VEZ:
    fallidos = pipeline_completo.ejecutar(FUENTES, sin_descarga=not DESCARGAR, forzar=FORZAR)
    print("Pasos fallidos:", fallidos or "ninguno")
else:
    print("TODO_DE_UNA_VEZ = False: ya se ejecutaron los pasos uno por uno arriba.")
