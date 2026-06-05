#!/usr/bin/env python3
"""
Genera un anexo de código en formato QMD.

La versión v2 deja los scripts largos dentro de bloques <details> para que,
en HTML, cada archivo aparezca plegado/desplegable. Esto evita que el cuerpo
del informe quede excesivamente largo, pero conserva el código integrado como
material suplementario.

Uso:
    python tools/generar_anexos_codigo_v2.py
"""

from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "anexos_codigo" / "anexo_codigo_completo.qmd"

FILES = [
    ("Google Earth Engine / JavaScript", "code/1_Paso_GEE_Adaptado.js", "javascript"),
    ("Google Earth Engine / JavaScript", "code/2_Paso_GEE_Adaptado.js", "javascript"),
    ("Google Earth Engine / JavaScript", "code/3_Paso_GEE_Adaptado.js", "javascript"),
    ("Python", "code/a_descargar_GEE.py", "python"),
    ("Python", "code/b_calidad.py", "python"),
    ("Python", "code/c_validacion.py", "python"),
    ("Python", "code/d_graficas_articulo5.py", "python"),
    ("Google Earth Engine / JavaScript", "code_modis/validacion_modis_gee.js", "javascript"),
    ("Python", "code_modis/validacion_modis_python.py", "python"),
    ("Julia", "scripts_julia/gpr_temporal_kernel_check.jl", "julia"),
    ("Julia", "scripts_julia/validacion_modis_metricas.jl", "julia"),
]

def read_file(path: Path) -> str:
    if not path.exists():
        return f"# PENDIENTE: no se encontró el archivo {path.as_posix()}\n"
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    blocks = []
    blocks.append("# Anexo C. Código completo integrado\n")
    blocks.append(
        "Este anexo integra los scripts principales del proyecto. "
        "En la salida HTML cada archivo aparece dentro de un bloque desplegable; "
        "en Word/PDF puede visualizarse como código suplementario al final del documento.\n"
    )

    for label, rel, lang in FILES:
        path = ROOT / rel
        code = read_file(path)
        title = f"{label}: {rel}"
        blocks.append(f"\n## {rel}\n")
        blocks.append(f"<details>\n<summary>{html.escape(title)}</summary>\n\n")
        blocks.append(f"```{lang}\n{code.rstrip()}\n```\n\n")
        blocks.append("</details>\n")

    OUT.write_text("\n".join(blocks), encoding="utf-8")
    print(f"Anexo generado en: {OUT}")

if __name__ == "__main__":
    main()
