// Validación externa con MODIS MCD15A3H v6.1 para LAI y FVC/FPAR
// ------------------------------------------------------------------
// Propósito: construir pares espacio-temporales entre los mapas gap-filled
// derivados de Sentinel-2/GPR y el producto MODIS MCD15A3H.
// IMPORTANTE: ajustar las rutas de assets a los nombres reales de su proyecto.

// 1. Parámetros generales ----------------------------------------------------
var START = '2023-01-01';
var END   = '2023-12-31';
var N_POINTS = 500;
var WINDOW_DAYS = 2;
var SCALE_MODIS = 500;

// 2. Área de estudio ---------------------------------------------------------
// Reemplace esta ruta por el AOI usado en el informe regional 2023.
var aoi = ee.FeatureCollection('users/USUARIO/AOI_PUERTO_GAITAN_UPRA_2023');

// 3. Colecciones Sentinel-2/GPR gap-filled ----------------------------------
// Deben contener una banda comparable con LAI o FVC y conservar system:time_start.
var gfLai = ee.ImageCollection('users/USUARIO/GF_LAI_2023')
  .filterDate(START, END)
  .filterBounds(aoi);

var gfFvc = ee.ImageCollection('users/USUARIO/GF_FVC_2023')
  .filterDate(START, END)
  .filterBounds(aoi);

// 4. Producto MODIS MCD15A3H -------------------------------------------------
// Lai: factor 0.1; Fpar: factor 0.01 según la documentación del producto.
var modis = ee.ImageCollection('MODIS/061/MCD15A3H')
  .filterDate(START, END)
  .filterBounds(aoi)
  .map(function(img) {
    var lai = img.select('Lai').multiply(0.1).rename('LAI_MODIS');
    var fpar = img.select('Fpar').multiply(0.01).rename('FPAR_MODIS');
    return lai.addBands(fpar).copyProperties(img, ['system:time_start']);
  });

// 5. Puntos fijos de validación ---------------------------------------------
var points = ee.FeatureCollection.randomPoints({
  region: aoi.geometry(),
  points: N_POINTS,
  seed: 2026,
  maxError: 10
});

// 6. Función para encontrar MODIS más cercano --------------------------------
function nearestModis(targetDate) {
  targetDate = ee.Date(targetDate);
  var start = targetDate.advance(-WINDOW_DAYS, 'day');
  var end = targetDate.advance(WINDOW_DAYS, 'day');
  var filtered = modis.filterDate(start, end);
  var withDiff = filtered.map(function(img) {
    var diff = ee.Number(img.get('system:time_start')).subtract(targetDate.millis()).abs();
    return img.set('time_diff', diff);
  });
  return ee.Image(withDiff.sort('time_diff').first());
}

// 7. Construcción de pares LAI ----------------------------------------------
function sampleLai(img) {
  img = ee.Image(img);
  var date = ee.Date(img.get('system:time_start'));
  var mod = nearestModis(date);
  var pair = img.select([0]).rename('LAI_GF')
    .addBands(mod.select('LAI_MODIS'))
    .set('date', date.format('YYYY-MM-dd'));
  return pair.sampleRegions({
    collection: points,
    scale: SCALE_MODIS,
    geometries: true
  }).map(function(f) { return f.set('date', date.format('YYYY-MM-dd')); });
}

// 8. Construcción de pares FVC-FPAR -----------------------------------------
function sampleFvc(img) {
  img = ee.Image(img);
  var date = ee.Date(img.get('system:time_start'));
  var mod = nearestModis(date);
  var pair = img.select([0]).rename('FVC_GF')
    .addBands(mod.select('FPAR_MODIS'))
    .set('date', date.format('YYYY-MM-dd'));
  return pair.sampleRegions({
    collection: points,
    scale: SCALE_MODIS,
    geometries: true
  }).map(function(f) { return f.set('date', date.format('YYYY-MM-dd')); });
}

var samplesLai = gfLai.map(sampleLai).flatten();
var samplesFvc = gfFvc.map(sampleFvc).flatten();

// 9. Exportación -------------------------------------------------------------
Export.table.toDrive({
  collection: samplesLai,
  description: 'validacion_MODIS_LAI_vs_GF_2023',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: samplesFvc,
  description: 'validacion_MODIS_FPAR_vs_FVC_GF_2023',
  fileFormat: 'CSV'
});
