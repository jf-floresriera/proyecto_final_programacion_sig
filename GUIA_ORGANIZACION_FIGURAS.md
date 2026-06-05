# Guía de organización de figuras para el informe final

Esta estructura evita mezclar las figuras del informe 1, informe 2 y la nueva validación MODIS.

```text
figuras_finales/
├── 00_flujo_general/
│   └── fig01_workflow_gee_python_julia.png
├── 01_regional_2023/
│   ├── fig01_workflow_gee_python_2023.png
│   ├── fig02_area_puerto_gaitan_upra.png
│   ├── fig03_validacion_gpr_gapfilled_2023.png
│   ├── fig04_series_temporales_2023.png
│   ├── fig05_mapas_biofisicos_2023.png
│   └── fig06_metricas_lsp_2023.png
├── 02_finca_2024/
│   ├── fig01_area_finca_la_esperanza.png
│   ├── fig02_validacion_gpr_gapfilled_finca.png
│   ├── fig03_lai_ciclo_a.png
│   ├── fig04_fvc_ciclo_b.png
│   ├── fig05_laicab_ciclo_b.png
│   ├── fig06_perfiles_temporales_2024.png
│   ├── fig07_metricas_lsp_2024.png
│   └── fig08_plugin_qgis.png
├── 03_plugin_qgis/
│   ├── fig08_plugin_qgis.png
│   └── README_plugin.md
└── 04_validacion_modis/
    ├── fig_modis_lai_fvc_scatter.png
    └── metricas_validacion_modis.csv
```

## Recomendaciones

1. Mantener nombres cortos, sin espacios ni tildes.
2. Usar resolución mínima de 300 dpi para figuras finales.
3. No sobrescribir las figuras originales: copiar versiones finales en `figuras_finales/`.
4. En el `.qmd`, reemplazar las rutas sugeridas si los nombres finales cambian.
5. Para evitar errores de renderizado, antes de compilar revisar que todas las rutas existan.
