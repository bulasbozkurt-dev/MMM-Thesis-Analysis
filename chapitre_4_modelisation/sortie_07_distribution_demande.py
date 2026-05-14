import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from scipy import stats

df_ec = pd.read_excel("E-Ticaret_MMM_v2.xlsx")
df_fg = pd.read_excel("FMCG_MMM_v2.xlsx")
df_ec.columns = [c.strip() for c in df_ec.columns]
df_fg.columns = [c.strip() for c in df_fg.columns]

s_ec = df_ec["ε : Variation de la demande"].dropna()
s_fg = df_fg["ε : Variation des ventes"].dropna()

FONT  = "DejaVu Serif"
C_EC  = "#1F3864"
C_FG  = "#1E6B3C"
C_NRM = "#C00000"

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#FAFAFA")

def tracer_distribution(ax, serie, couleur, titre, xlabel):
    ax.set_facecolor("#F7F9FC")

    n_bins = min(50, int(np.sqrt(len(serie))))
    counts, bins, patches = ax.hist(
        serie, bins=n_bins, color=couleur, alpha=0.55,
        edgecolor="white", linewidth=0.5, density=True, label="Distribution observée"
    )

    x_min, x_max = serie.min(), serie.max()
    x_range = np.linspace(x_min, x_max, 300)
    mu, sigma = serie.mean(), serie.std()
    y_norm = stats.norm.pdf(x_range, mu, sigma)
    ax.plot(x_range, y_norm, color=C_NRM, lw=2.0,
            linestyle="--", label="Loi normale théorique")

    ax.axvline(mu, color=couleur, lw=1.5, linestyle="-",
               label=f"Moyenne = {mu:.3f}")
    ax.axvline(mu + sigma, color=couleur, lw=1.0, linestyle=":",
               alpha=0.7, label=f"±1 écart-type ({sigma:.3f})")
    ax.axvline(mu - sigma, color=couleur, lw=1.0, linestyle=":", alpha=0.7)

    sk = stats.skew(serie)
    ku = stats.kurtosis(serie)
    stat_jb, p_jb = stats.jarque_bera(serie)

    texte_stats = (
        f"N = {len(serie):,}\n"
        f"Moyenne = {mu:.4f}\n"
        f"Écart-type = {sigma:.4f}\n"
        f"Asymétrie = {sk:.3f}\n"
        f"Aplatissement = {ku:.3f}\n"
        f"Jarque-Bera = {stat_jb:.2f}\n"
        f"p-valeur = {p_jb:.4f}"
    )
    ax.text(0.97, 0.97, texte_stats,
            transform=ax.transAxes, ha="right", va="top",
            fontsize=8, fontfamily=FONT, color="#333333",
            bbox=dict(boxstyle="round,pad=0.4", fc="white",
                      ec="#CCCCCC", alpha=0.92))

    ax.set_title(titre, fontsize=10.5, fontweight="bold",
                 fontfamily=FONT, color="#1F3864", pad=8)
    ax.set_xlabel(xlabel, fontsize=9, fontfamily=FONT, color="#444")
    ax.set_ylabel("Densité", fontsize=9, fontfamily=FONT, color="#444")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, prop={"family": FONT},
              framealpha=0.9, edgecolor="#CCCCCC", loc="upper left")

tracer_distribution(
    axes[0], s_ec, C_EC,
    "E-Commerce — Distribution de ε : Variation de la demande",
    "ε : Variation de la demande (quotidienne)"
)

tracer_distribution(
    axes[1], s_fg, C_FG,
    "FMCG — Distribution de ε : Variation des ventes",
    "ε : Variation des ventes (hebdomadaire)"
)

fig.suptitle(
    "Figure 3 — Distribution de la variabilité de la demande (résidus de variation)",
    fontsize=12.5, fontweight="bold", fontfamily=FONT, color="#1F3864", y=1.02
)

fig.text(
    0.5, -0.02,
    "Source : Auteur. Test de Jarque-Bera : H₀ = normalité de la distribution. "
    "p < 0,05 indique un rejet de la normalité.",
    ha="center", fontsize=7.5, fontfamily=FONT, color="#777777", style="italic"
)

plt.tight_layout(pad=2.5)
output_path = "Figure_07_Distribution_Variabilite_Demande.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
