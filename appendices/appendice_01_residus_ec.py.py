import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

df = pd.read_excel("E-Ticaret_MMM_v2.xlsx")
df.columns = [c.strip() for c in df.columns]

FONT = "DejaVu Serif"

VARS_EC = [
    "M : Google", "M : Meta", "M : Influenceur", "M : Indice de dépenses",
    "M : Retard t-1", "M : Retard t-7", "D : Retard t-1",
    "Choc : Taux de change", "Choc : Crise logistique",
    "Facteur saisonnier", "Effet du dimanche",
    "Dépenses des concurrents", "Part de voix (%)", "Taux de conversion (%)",
]
DEP = "D : Commandes (canal)"

valid = [v for v in VARS_EC if v in df.columns]
sub   = df[[DEP] + valid].dropna()
Y     = sub[DEP].values
X     = np.column_stack([np.ones(len(Y)), sub[valid].values])
n, k  = X.shape
params, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
fitted = X @ params
resid  = Y - fitted
R_std  = (resid - resid.mean()) / resid.std()

sse    = resid @ resid
sst    = ((Y - Y.mean())**2).sum()
r2     = 1 - sse / sst
r2_adj = 1 - (1 - r2) * (n-1) / (n-k)
jb_stat, jb_p = scipy_stats.jarque_bera(resid)
dw_val = (np.diff(resid)**2).sum() / (resid @ resid)
sk     = scipy_stats.skew(resid)
ku     = scipy_stats.kurtosis(resid)

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.patch.set_facecolor("#FAFAFA")
C = "#1F3864"

def style_ax(ax):
    ax.set_facecolor("#F7F9FC")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)

# ── Panneau 1 : résidus vs valeurs ajustées ───────────────────────────────────
ax = axes[0, 0]
style_ax(ax)
ax.scatter(fitted, resid, color=C, alpha=0.25, s=8, edgecolors="none")
ax.axhline(0, color="#C00000", lw=1.5, linestyle="--")
ax.set_xlabel("Valeurs ajustées", fontsize=9, fontfamily=FONT)
ax.set_ylabel("Résidus", fontsize=9, fontfamily=FONT)
ax.set_title("Résidus vs Valeurs ajustées",
             fontsize=10.5, fontweight="bold",
             fontfamily=FONT, color="#1F3864", pad=8)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.text(0.02, 0.97,
        f"R² = {r2:.4f}\nR² ajusté = {r2_adj:.4f}",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=8.5, fontfamily=FONT, color="#333",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CCCCCC", alpha=0.9))

# ── Panneau 2 : QQ-plot ───────────────────────────────────────────────────────
ax = axes[0, 1]
style_ax(ax)
qq = scipy_stats.probplot(R_std, dist="norm")
ax.scatter(qq[0][0], qq[0][1], color=C, alpha=0.35, s=8, edgecolors="none")
x_line = np.array([qq[0][0].min(), qq[0][0].max()])
ax.plot(x_line, qq[1][1] + qq[1][0] * x_line,
        color="#C00000", lw=1.8, linestyle="--",
        label="Droite théorique normale")
ax.set_xlabel("Quantiles théoriques", fontsize=9, fontfamily=FONT)
ax.set_ylabel("Quantiles observés",   fontsize=9, fontfamily=FONT)
ax.set_title("Graphique quantile-quantile (QQ-plot)",
             fontsize=10.5, fontweight="bold",
             fontfamily=FONT, color="#1F3864", pad=8)
ax.legend(fontsize=8, prop={"family": FONT},
          framealpha=0.9, edgecolor="#CCCCCC")

# ── Panneau 3 : histogramme des résidus standardisés ─────────────────────────
ax = axes[1, 0]
style_ax(ax)
n_bins = min(50, int(np.sqrt(len(resid))))
ax.hist(R_std, bins=n_bins, color=C, alpha=0.55,
        edgecolor="white", linewidth=0.5, density=True,
        label="Distribution observée")
x_r = np.linspace(R_std.min(), R_std.max(), 300)
ax.plot(x_r, scipy_stats.norm.pdf(x_r),
        color="#C00000", lw=2.0, linestyle="--",
        label="Loi normale théorique")
ax.set_xlabel("Résidus standardisés", fontsize=9, fontfamily=FONT)
ax.set_ylabel("Densité", fontsize=9, fontfamily=FONT)
ax.set_title("Distribution des résidus standardisés",
             fontsize=10.5, fontweight="bold",
             fontfamily=FONT, color="#1F3864", pad=8)
ax.text(0.97, 0.97,
        f"Asymétrie   = {sk:.3f}\n"
        f"Aplatissement = {ku:.3f}\n"
        f"Jarque-Bera  = {jb_stat:.2f}\n"
        f"p-valeur JB  = {jb_p:.4f}\n"
        f"Durbin-Watson = {dw_val:.3f}",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=8, fontfamily=FONT, color="#333",
        bbox=dict(boxstyle="round,pad=0.4", fc="white",
                  ec="#CCCCCC", alpha=0.92))
ax.legend(fontsize=8, prop={"family": FONT},
          framealpha=0.9, edgecolor="#CCCCCC")

# ── Panneau 4 : autocorrélogramme (ACF) ──────────────────────────────────────
ax = axes[1, 1]
style_ax(ax)
max_lag = min(40, n // 4)
acf_vals = [1.0]
for lag in range(1, max_lag + 1):
    acf_vals.append(np.corrcoef(resid[:-lag], resid[lag:])[0, 1])
lags = np.arange(len(acf_vals))
ax.bar(lags, acf_vals, color=C, alpha=0.65,
       edgecolor="white", linewidth=0.5, width=0.7)
ci = 1.96 / np.sqrt(n)
ax.axhline( ci, color="#C00000", lw=1.2, linestyle="--",
            alpha=0.8, label=f"IC 95% (±{ci:.3f})")
ax.axhline(-ci, color="#C00000", lw=1.2, linestyle="--", alpha=0.8)
ax.axhline(0,   color="#555555", lw=0.8)
ax.set_xlabel("Décalage (lag)", fontsize=9, fontfamily=FONT)
ax.set_ylabel("Autocorrélation", fontsize=9, fontfamily=FONT)
ax.set_title("Autocorrélogramme des résidus (ACF)",
             fontsize=10.5, fontweight="bold",
             fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylim(-1.05, 1.05)
ax.legend(fontsize=8, prop={"family": FONT},
          framealpha=0.9, edgecolor="#CCCCCC")

fig.suptitle(
    "Appendice C — Diagnostics des résidus MCO — E-Commerce",
    fontsize=12, fontweight="bold", fontfamily=FONT,
    color="#1F3864", y=1.01
)
fig.text(0.5, -0.01,
         "Note : Test de Jarque-Bera : H₀ = normalité des résidus. "
         "Durbin-Watson : valeur proche de 2 = absence d'autocorrélation.\n"
         "Source : Auteur, estimations MCO à partir des données propriétaires E-Commerce (2022–2024).",
         ha="center", fontsize=7.5, fontfamily=FONT,
         color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Appendice_C_Diagnostics_Residus_EC.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
