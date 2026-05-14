import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

df_ec = pd.read_excel("E-Ticaret_MMM_v2.xlsx")
df_fg = pd.read_excel("FMCG_MMM_v2.xlsx")
df_ec.columns = [c.strip() for c in df_ec.columns]
df_fg.columns = [c.strip() for c in df_fg.columns]

df_ec["Date"] = pd.to_datetime(df_ec["Date"])
df_fg["Date"] = pd.to_datetime(df_fg["Date"])

FONT = "DejaVu Serif"

def estimer_fitted(df, dep, vars_list):
    valid = [v for v in vars_list if v in df.columns]
    sub   = df[[dep] + valid + (["Date"] if "Date" in df.columns else [])].dropna()
    Y     = sub[dep].values
    X     = np.column_stack([np.ones(len(Y)), sub[valid].values])
    params, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
    fitted = X @ params
    resid  = Y - fitted
    sst    = ((Y - Y.mean())**2).sum()
    sse    = (resid**2).sum()
    r2     = 1 - sse / sst
    n, k   = X.shape
    r2_adj = 1 - (1 - r2) * (n - 1) / (n - k)
    return Y, fitted, resid, sub["Date"].values if "Date" in sub.columns else np.arange(len(Y)), r2, r2_adj

VARS_EC = [
    "M : Google", "M : Meta", "M : Influenceur", "M : Indice de dépenses",
    "M : Retard t-1", "M : Retard t-7", "D : Retard t-1",
    "Choc : Taux de change", "Choc : Crise logistique",
    "Facteur saisonnier", "Effet du dimanche",
    "Dépenses des concurrents", "Part de voix (%)", "Taux de conversion (%)",
]
VARS_FG = [
    "M : Dépenses marketing totales", "M : Pondéré",
    "M : Retard 1 semaine", "M : Retard 4 semaines", "D : Retard 1 semaine",
    "Choc : Taux de change", "Choc : Impact du séisme",
    "Facteur saisonnier",
    "Dépenses marketing des concurrents", "Part de voix (%)", "Part de marché (%)",
    "Rupture de stock (%)", "Stock (jours)", "Efficacité marketing",
]

Y_ec, F_ec, R_ec, dates_ec, r2_ec, r2a_ec = estimer_fitted(df_ec, "D : Commandes (canal)", VARS_EC)
Y_fg, F_fg, R_fg, dates_fg, r2_fg, r2a_fg = estimer_fitted(df_fg, "D : Volume des ventes",  VARS_FG)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor("#FAFAFA")

C_OBS  = "#1F3864"
C_FIT  = "#C00000"
C_RES  = "#B45309"
C_ZERO = "#555555"

def style_ax(ax):
    ax.set_facecolor("#F7F9FC")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)

# ── Panneau 1 : E-Commerce — série temporelle ─────────────────────────────────
ax = axes[0, 0]
style_ax(ax)
ax.plot(dates_ec, Y_ec, color=C_OBS, lw=1.2, alpha=0.7, label="Valeurs observées")
ax.plot(dates_ec, F_ec, color=C_FIT, lw=1.5, linestyle="--", label="Valeurs ajustées")
ax.set_title("E-Commerce — Valeurs observées vs ajustées\n(série temporelle)",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=6)
ax.set_ylabel("Commandes", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.text(0.02, 0.97, f"R² = {r2_ec:.4f}\nR² ajusté = {r2a_ec:.4f}",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
        fontfamily=FONT, color="#333",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CCCCCC", alpha=0.9))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9,
          edgecolor="#CCCCCC", loc="upper right")

# ── Panneau 2 : E-Commerce — nuage de points ──────────────────────────────────
ax = axes[0, 1]
style_ax(ax)
ax.scatter(Y_ec, F_ec, color=C_OBS, alpha=0.25, s=8, edgecolors="none")
lims = [min(Y_ec.min(), F_ec.min()), max(Y_ec.max(), F_ec.max())]
ax.plot(lims, lims, color=C_FIT, lw=1.5, linestyle="--", label="Droite parfaite (45°)")
slope, intercept, r, p, _ = scipy_stats.linregress(Y_ec, F_ec)
x_line = np.linspace(lims[0], lims[1], 100)
ax.plot(x_line, intercept + slope * x_line, color=C_RES, lw=1.2,
        linestyle="-", alpha=0.7, label=f"Tendance (r = {r:.3f})")
ax.set_title("E-Commerce — Nuage : observées vs ajustées",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=6)
ax.set_xlabel("Valeurs observées", fontsize=8.5, fontfamily=FONT)
ax.set_ylabel("Valeurs ajustées",  fontsize=8.5, fontfamily=FONT)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")

# ── Panneau 3 : FMCG — série temporelle ──────────────────────────────────────
ax = axes[1, 0]
style_ax(ax)
ax.plot(dates_fg, Y_fg, color="#1E6B3C", lw=1.2, alpha=0.7, label="Valeurs observées")
ax.plot(dates_fg, F_fg, color=C_FIT, lw=1.5, linestyle="--", label="Valeurs ajustées")
ax.set_title("FMCG — Valeurs observées vs ajustées\n(série temporelle)",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=6)
ax.set_ylabel("Volume des ventes", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.text(0.02, 0.97, f"R² = {r2_fg:.4f}\nR² ajusté = {r2a_fg:.4f}",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
        fontfamily=FONT, color="#333",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CCCCCC", alpha=0.9))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9,
          edgecolor="#CCCCCC", loc="upper right")

# ── Panneau 4 : FMCG — nuage de points ───────────────────────────────────────
ax = axes[1, 1]
style_ax(ax)
ax.scatter(Y_fg, F_fg, color="#1E6B3C", alpha=0.25, s=8, edgecolors="none")
lims_fg = [min(Y_fg.min(), F_fg.min()), max(Y_fg.max(), F_fg.max())]
ax.plot(lims_fg, lims_fg, color=C_FIT, lw=1.5, linestyle="--", label="Droite parfaite (45°)")
slope2, intercept2, r2, p2, _ = scipy_stats.linregress(Y_fg, F_fg)
x2 = np.linspace(lims_fg[0], lims_fg[1], 100)
ax.plot(x2, intercept2 + slope2 * x2, color=C_RES, lw=1.2,
        linestyle="-", alpha=0.7, label=f"Tendance (r = {r2:.3f})")
ax.set_title("FMCG — Nuage : observées vs ajustées",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=6)
ax.set_xlabel("Valeurs observées", fontsize=8.5, fontfamily=FONT)
ax.set_ylabel("Valeurs ajustées",  fontsize=8.5, fontfamily=FONT)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")

fig.suptitle("Figure 7 — Valeurs observées vs valeurs ajustées du modèle MCO",
             fontsize=13, fontweight="bold", fontfamily=FONT,
             color="#1F3864", y=1.01)

fig.text(0.5, -0.01,
         "Source : Auteur, estimations MCO. "
         "La droite en pointillé rouge représente l'ajustement parfait (observé = ajusté).",
         ha="center", fontsize=7.5, fontfamily=FONT, color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Figure_14_Observees_vs_Ajustees.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
