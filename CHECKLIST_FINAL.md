# Checklist antes de entregar

- [ ] Copiar el `.qmd` en la raíz del repositorio.
- [ ] Copiar las figuras originales a `figuras_finales/` usando la guía de nombres.
- [ ] Revisar que el texto no diga que se ejecutó Julia para todo el pipeline, sino como verificación complementaria.
- [ ] Confirmar que las métricas MODIS son las definitivas y que la figura `fig_modis_lai_fvc_scatter.png` esté en su carpeta.
- [ ] Ejecutar `python tools/generar_anexos_codigo.py`.
- [ ] Renderizar HTML y PDF dentro del Docker.
- [ ] Subir `.qmd`, HTML, PDF, scripts, `environment.yml`, `Project.toml` y figuras al repositorio público.

## Verificación adicional: plugin QGIS

- [ ] Verificar que el informe mencione el plugin en metodología.
- [ ] Verificar que el informe incluya el plugin como resultado instrumental.
- [ ] Verificar que la discusión explique el aporte del plugin como desarrollo de software geoespacial.
- [ ] Incluir la figura de interfaz del plugin en `figuras_finales/03_plugin_qgis/` o ajustar la ruta en el `.qmd`.
- [ ] Si se entrega el código del plugin, incorporarlo como submódulo o carpeta complementaria `plugin_qgis/GEE_GPR_Phenology/`.
