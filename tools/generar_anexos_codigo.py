from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "anexos_codigo"
OUT.mkdir(exist_ok=True)

FILES = [
    ("Google Earth Engine - Paso 1: predicción espectral GPR", "code/1_Paso_GEE_Adaptado.js", "javascript"),
    ("Google Earth Engine - Paso 2: gap-filling temporal GPR", "code/2_Paso_GEE_Adaptado.js", "javascript"),
    ("Google Earth Engine - Paso 3: métricas LSP", "code/3_Paso_GEE_Adaptado.js", "javascript"),
    ("Python - descarga de productos desde GEE", "code/a_descargar_GEE.py", "python"),
    ("Python - control de calidad de imágenes", "code/b_calidad.py", "python"),
    ("Python - validación cruzada GPR vs gap-filled", "code/c_validacion.py", "python"),
    ("Python - generación de figuras finales", "code/d_graficas_articulo5.py", "python"),
    ("Google Earth Engine - validación externa con MODIS MCD15A3H", "code_modis/validacion_modis_gee.js", "javascript"),
    ("Python - métricas y gráficos de validación MODIS", "code_modis/validacion_modis_python.py", "python"),
    ("Julia - verificación numérica del kernel GPR temporal", "scripts_julia/gpr_temporal_kernel_check.jl", "julia"),
    ("Julia - métricas de validación MODIS", "scripts_julia/validacion_modis_metricas.jl", "julia"),
]

content = [
    "# Anexo C. Código completo del proyecto\n",
    "Este anexo se genera automáticamente a partir de los scripts reales presentes en el repositorio. ",
    "Los bloques se muestran con `eval: false`, por lo que el informe los documenta para revisión y trazabilidad sin ejecutarlos durante el renderizado.\n",
]

for title, rel, lang in FILES:
    path = ROOT / rel
    content.append(f"\n## {title}\n")
    content.append(f"Archivo esperado: `{rel}`\n")
    if path.exists():
        code = path.read_text(encoding="utf-8", errors="replace")
        content.append(f"```{{{lang}}}\n#| eval: false\n#| echo: true\n")
        content.append(code.rstrip() + "\n")
        content.append("```\n")
    else:
        content.append(
            f"> **Pendiente:** no se encontró `{rel}` al generar este anexo. "
            "Verifique que el archivo exista en la raíz del repositorio antes de renderizar la versión final.\n"
        )

(OUT / "anexo_codigo_completo.qmd").write_text("\n".join(content), encoding="utf-8")
print(f"Anexo generado en: {OUT / 'anexo_codigo_completo.qmd'}")
