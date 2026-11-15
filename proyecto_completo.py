"""Proyecto completo, de inicio a fin, en un solo script (solo codigo, sin explicaciones).

Es el mismo flujo de la Parte B del cuaderno notebooks/proyecto_completo.ipynb (que si trae las explicaciones): descarga, tablas de ESCALE y ENLA,
datos personales, proyecto PDF, NLP de las causas, producto final, CSV unico del dashboard, diccionario y auditorias.
El codigo de cada modulo esta en src/ (config.py, utils.py, nlp_causas.py, producto_final.py, ...).

  python proyecto_completo.py        (o en VS Code: «Run Cell» en cada bloque «# %%»)

Este archivo lo genera generar_cuaderno.py desde el cuaderno: no se edita a mano.
"""
import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ_PROYECTO / "src"))

# %% 0. Opciones
from types import SimpleNamespace

import auditoria_calidad
import catalogo_escale
import config
import datos_personales
import diccionario
import escale_ampliado
import inventario_datos
import main
import main_pdf
import pipeline_completo
import producto_final

# ---------------- opciones ----------------
DESCARGAR = False          # True: consulta ESCALE, ENLA, Contraloría y MEF (Chrome visible + internet, ~15 min). False: usa data/raw tal como está
INCLUIR_INFOBRAS = False   # True: ADEMAS vuelve a leer INFOBRAS. Cambia el listado (hay obras que dejaron de estar paralizadas) y mueve los números
FORZAR = False             # True: rehace todo aunque ya esté hecho (muy lento)

FUENTES = list(pipeline_completo.FUENTES_POR_DEFECTO) + (["infobras"] if INCLUIR_INFOBRAS else [])
ARGS = SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES)
print("Carpeta del proyecto:", config.RAIZ.name)
print("Descargar:", DESCARGAR, "| fuentes:", FUENTES)

# %% 1. Descarga de las fuentes
if DESCARGAR:
    main.descargar(ARGS)
else:
    print("DESCARGAR = False: no se consulta ningún portal; se usa lo que hay en data/raw")

# %% 2. Tablas de ESCALE y ENLA
main.extraer(SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES))
catalogo_escale.construir()
escale_ampliado.construir()

# %% 3. Datos personales
datos_personales.limpiar()

# %% 4. Proyecto PDF (fases 1 a 4) y anexos Excel
main_pdf.ejecutar(4, FORZAR)

# %% 5. Producto final: NLP de las causas, tablas y CSV único
tablas, validacion = producto_final.construir()

# %% 6. Diccionario, datos personales e inventario
diccionario.escribir_diccionario()
datos_personales.auditoria_o_falla()
inventario_datos.construir()

# %% 7. Auditoría de calidad del CSV único
auditoria_calidad.auditoria_o_falla()
