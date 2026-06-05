"""Validación externa MODIS vs productos GPR gap-filled.

Entradas esperadas:
  data/validacion_MODIS_LAI_vs_GF_2023.csv con columnas LAI_MODIS, LAI_GF
  data/validacion_MODIS_FPAR_vs_FVC_GF_2023.csv con columnas FPAR_MODIS, FVC_GF

Este script calcula MSE, RMSE, MAE, bias, R², pendiente, intercepto y Pearson r,
y genera un panel de dispersión con línea 1:1 y recta de regresión.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr, linregress

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "figuras_finales" / "03_validacion_modis"
OUT.mkdir(parents=True, exist_ok=True)


def metrics(y_true, y_pred):
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    y_true = np.asarray(y_true)[mask]
    y_pred = np.asarray(y_pred)[mask]
    reg = linregress(y_true, y_pred)
    return {
        "n": len(y_true),
        "MSE": mean_squared_error(y_true, y_pred),
        "RMSE": mean_squared_error(y_true, y_pred, squared=False),
        "MAE": mean_absolute_error(y_true, y_pred),
        "Bias": float(np.mean(y_pred - y_true)),
        "R2": r2_score(y_true, y_pred),
        "Slope": reg.slope,
        "Intercept": reg.intercept,
        "Pearson_r": pearsonr(y_true, y_pred)[0],
    }


def plot_panel(lai_df, fvc_df):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), constrained_layout=True)

    panels = [
        (axes[0], lai_df["LAI_MODIS"], lai_df["LAI_GF"], "LAI MODIS", "LAI GF", "LAI"),
        (axes[1], fvc_df["FPAR_MODIS"], fvc_df["FVC_GF"], "FPAR MODIS", "FVC GF", "FVC-FPAR"),
    ]

    rows = []
    for ax, x, y, xlabel, ylabel, name in panels:
        m = metrics(x.to_numpy(), y.to_numpy())
        rows.append({"Variable": name, **m})
        ax.scatter(x, y, s=10, alpha=0.45)
        lim_min = np.nanmin([x.min(), y.min()])
        lim_max = np.nanmax([x.max(), y.max()])
        ax.plot([lim_min, lim_max], [lim_min, lim_max], linestyle="--", linewidth=1, label="1:1")
        xx = np.linspace(lim_min, lim_max, 100)
        ax.plot(xx, m["Slope"] * xx + m["Intercept"], linewidth=1.2, label="Regresión")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(name)
        ax.legend()
        ax.text(0.03, 0.97, f"n={m['n']}\nRMSE={m['RMSE']:.3f}\nBias={m['Bias']:.3f}\nR²={m['R2']:.2f}\nr={m['Pearson_r']:.2f}",
                transform=ax.transAxes, va="top", ha="left")

    fig.savefig(OUT / "fig_modis_lai_fvc_scatter.png", dpi=300)
    pd.DataFrame(rows).to_csv(OUT / "metricas_validacion_modis.csv", index=False)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    lai = pd.read_csv(DATA / "validacion_MODIS_LAI_vs_GF_2023.csv")
    fvc = pd.read_csv(DATA / "validacion_MODIS_FPAR_vs_FVC_GF_2023.csv")
    summary = plot_panel(lai, fvc)
    print(summary.to_string(index=False))
