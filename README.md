# Informe final robusto - Programación en SIG

Este paquete contiene una versión ampliada del informe Quarto que integra:

- Informe 1: fase regional 2023 en Puerto Gaitán, Meta.
- Informe 2: fase Finca La Esperanza 2024.
- Nueva fase de validación externa con MODIS MCD15A3H.
- Código suplementario en GEE/JavaScript, Python y Julia.
- Generador automático de anexos de código.

## Uso recomendado

1. Copiar todo el contenido de este paquete en la raíz del repositorio:

```bash
sentinel2-maize-gaussian-processes/
```

2. Copiar las figuras finales en la estructura indicada en `GUIA_ORGANIZACION_FIGURAS.md`.

3. Generar el anexo de código:

```bash
python tools/generar_anexos_codigo.py
```

4. Renderizar:

```bash
quarto render informe_final_programacion_sig_robusto.qmd --to html
quarto render informe_final_programacion_sig_robusto.qmd --to pdf
```

## Archivos nuevos

- `informe_final_programacion_sig_robusto.qmd`
- `tools/generar_anexos_codigo.py`
- `code_modis/validacion_modis_gee.js`
- `code_modis/validacion_modis_python.py`
- `scripts_julia/gpr_temporal_kernel_check.jl`
- `scripts_julia/validacion_modis_metricas.jl`
- `Project.toml`
- `GUIA_ORGANIZACION_FIGURAS.md`
