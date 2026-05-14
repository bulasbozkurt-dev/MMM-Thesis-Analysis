import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

df_ec = pd.read_excel("E-Ticaret_MMM_v2.xlsx")
df_fg = pd.read_excel("FMCG_MMM_v2.xlsx")
df_ec.columns = [c.strip() for c in df_ec.columns]
df_fg.columns = [c.strip() for c in df_fg.columns]

df_ec["Date"] = pd.to_datetime(df_ec["Date"])
df_fg["Date"] = pd.to_datetime(df_fg["Date"])

ec_mensuel = df_ec.groupby(df_ec["Date"].dt.to_period("M")).agg(
    demande=("D : Total quotidien", "sum"),
    marketing=("M : Indice de dépenses", "mean"),
).reset_index()
ec_mensuel["Date"] = ec_mensuel["Date"].dt.to_timestamp()

fg_hebdo = df_fg.groupby(df_fg["Date"].dt.to_period("W")).agg(
    demande=("D : Volume des ventes", "sum"),
    marketing=("M : Dépenses marketing totales", "sum"),
).reset_index()
fg_hebdo["Date"] = fg_hebdo["Date"].dt.to_timestamp()

C_DEM  = "#1F3864"
C_MARK = "#1E6B3C"
C_AX2  = "#B45309"
FONT   = "DejaVu Serif"

fig, axes = plt.subplots(2, 1, figsize=(14, 9))
fig.patch.set_facecolor("#FAFAFA")

def tracer_evolution(ax, df, col_dem, col_mark, titre, unite_dem, unite_mark, freq_label):
    ax.set_facecolor("#F7F9FC")
    ax2 = ax.twinx()

    ax.fill_between(df["Date"], df[col_dem], alpha=0.15, color=C_DEM)
    l1, = ax.plot(df["Date"], df[col_dem], color=C_DEM, lw=1.8,
                  label=f"Demande ({unite_dem})")

    ax2.fill_between(df["Date"], df[col_mark], alpha=0.12, color=C_MARK)
    l2, = ax2.plot(df["Date"], df[col_mark], color=C_MARK, lw=1.8,
                   linestyle="--", label=f"Dépenses marketing ({unite_mark})")

    ax.set_title(titre, fontsize=11, fontweight="bold",
                 fontfamily=FONT, color="#1F3864", pad=8)
    ax.set_xlabel(f"Période ({freq_label})", fontsize=9, fontfamily=FONT, color="#444")
    ax.set_ylabel(f"Demande ({unite_dem})", fontsize=9, fontfamily=FONT, color=C_DEM)
    ax2.set_ylabel(f"Dépenses marketing ({unite_mark})", fontsize=9,
                   fontfamily=FONT, color=C_MARK)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{x:,.0f}"))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{x:,.2f}" if max(df[col_mark]) < 10 else f"{x:,.0f}"))

    ax.tick_params(axis="both", labelsize=8)
    ax2.tick_params(axis="both", labelsize=8)
    for label in ax.get_xticklabels():
        label.set_fontfamily(FONT)
    for label in ax.get_yticklabels():
        label.set_fontfamily(FONT)
    for label in ax2.get_yticklabels():
        label.set_fontfamily(FONT)

    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax.spines["left"].set_color(C_DEM)
    ax2.spines["right"].set_color(C_MARK)
    ax.tick_params(axis="y", colors=C_DEM)
    ax2.tick_params(axis="y", colors=C_MARK)

    lines = [l1, l2]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc="upper left", fontsize=8.5,
              prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")

    corr = df[[col_dem, col_mark]].corr().iloc[0, 1]
    ax.text(0.99, 0.97, f"ρ = {corr:.3f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=8.5, fontfamily=FONT, style="italic", color="#555555",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CCCCCC", alpha=0.9))

tracer_evolution(
    axes[0], ec_mensuel, "demande", "marketing",
    "E-Commerce — Évolution mensuelle de la demande et des dépenses marketing",
    "commandes/mois", "indice moyen", "mensuelle"
)

tracer_evolution(
    axes[1], fg_hebdo, "demande", "marketing",
    "FMCG — Évolution hebdomadaire de la demande et des dépenses marketing",
    "unités/semaine", "₺", "hebdomadaire"
)

fig.suptitle("Figure 2 — Évolution des dépenses marketing et de la demande",
             fontsize=13, fontweight="bold", fontfamily=FONT,
             color="#1F3864", y=1.01)

fig.text(0.5, -0.01,
         "Source : Auteur, à partir des données propriétaires E-Commerce et FMCG (2022–2024). "
         "ρ = coefficient de corrélation de Pearson entre demande et dépenses marketing.",
         ha="center", fontsize=7.5, fontfamily=FONT,
         color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Figure_06_Evolution_Marketing_Demande.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
