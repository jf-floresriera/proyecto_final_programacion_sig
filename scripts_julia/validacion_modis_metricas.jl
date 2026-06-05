# Cálculo de métricas de validación MODIS en Julia.
# Entrada: CSV con columnas y_true e y_pred, o adaptar nombres a LAI_MODIS/LAI_GF, FPAR_MODIS/FVC_GF.

using CSV
using DataFrames
using Statistics
using GLM

function regression_metrics(df::DataFrame, true_col::Symbol, pred_col::Symbol)
    clean = dropmissing(df[:, [true_col, pred_col]])
    y = Float64.(clean[:, true_col])
    ŷ = Float64.(clean[:, pred_col])
    n = length(y)
    residuals = ŷ .- y
    mse = mean(residuals .^ 2)
    rmse = sqrt(mse)
    mae = mean(abs.(residuals))
    bias = mean(residuals)
    r = cor(y, ŷ)
    r2 = 1 - sum(residuals .^ 2) / sum((y .- mean(y)) .^ 2)
    reg_df = DataFrame(y_true=y, y_pred=ŷ)
    model = lm(@formula(y_pred ~ y_true), reg_df)
    slope = coef(model)[2]
    intercept = coef(model)[1]
    return DataFrame(n=n, MSE=mse, RMSE=rmse, MAE=mae, Bias=bias,
                     R2=r2, Slope=slope, Intercept=intercept, Pearson_r=r)
end

# Ejemplo de uso:
# lai = CSV.read("data/validacion_MODIS_LAI_vs_GF_2023.csv", DataFrame)
# println(regression_metrics(lai, :LAI_MODIS, :LAI_GF))
# fvc = CSV.read("data/validacion_MODIS_FPAR_vs_FVC_GF_2023.csv", DataFrame)
# println(regression_metrics(fvc, :FPAR_MODIS, :FVC_GF))
