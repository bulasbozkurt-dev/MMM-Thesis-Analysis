import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

df = pd.read_excel("E-Ticaret_MMM_v2.xlsx")
df.columns = [c.strip() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"])

FONT   = "DejaVu Serif"
CANAUX = sorted(df["Canal"].dropna().unique())
COLORS = ["#1F3864", "#1E6B3C", "#C00000", "#B45309",
          "#7B2D8B", "#0D7377", "#8B4513", "#2F4F4F"]

fig, axes = plt.subplots(len(CANAUX), 1,
                         figsize=(14, 3.8 * len(CANAUX)),
                         sharex=False)
if len(CANAUX) == 1:
    axes = [axes]
fig.patch.set_facecolor("#FAFAFA")

for i, canal in enumerate(CANAUX):
    ax  = axes[i]
    sub = df[df["Canal"] == canal].sort_values("Date")
    men = sub.groupby(sub["Date"].dt.to_period("M")).agg(
        demande=("D : Commandes (canal)", "sum"),
        marketing=("M : Indice de dépenses", "mean"),
    ).reset_index()
    men["Date"] = men["Date"].dt.to_timestamp()

    ax.set_facecolor("#F7F9FC")
    ax2 = ax.twinx()

    ax.fill_between(men["Date"], men["demande"],
                    alpha=0.15, color=COLORS[i % len(COLORS)])
    l1, = ax.plot(men["Date"], men["demande"],
                  color=COLORS[i % len(COLORS)], lw=1.8,
                  label="Commandes (canal)")
    l2, = ax2.plot(men["Date"], men["marketing"],
                   color="#B45309", lw=1.5, linestyle="--",
                   label="Indice dépenses marketing")

    corr = men[["demande", "marketing"]].corr().iloc[0, 1]
    ax.text(0.99, 0.97, f"ρ = {corr:.3f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=8.5, fontfamily=FONT, style="italic", color="#555",
            bbox=dict(boxstyle="round,pad=0.3", fc="white",
                      ec="#CCCCCC", alpha=0.9))

    ax.set_title(f"Canal : {canal}",
                 fontsize=10.5, fontweight="bold",
                 fontfamily=FONT, color="#1F3864", pad=6)
    ax.set_ylabel("Commandes / mois", fontsize=8.5, fontfamily=FONT,
                  color=COLORS[i % len(COLORS)])
    ax2.set_ylabel("Indice dépenses mktg", fontsize=8.5, fontfamily=FONT,
                   color="#B45309")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{x:,.0f}"))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{x:,.2f}"))
    ax.tick_params(labelsize=8)
    ax2.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)
    for lbl in ax2.get_yticklabels():
        lbl.set_fontfamily(FONT)
    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax.tick_params(axis="y", colors=COLORS[i % len(COLORS)])
    ax2.tick_params(axis="y", colors="#B45309")
    ax.legend([l1, l2], [l1.get_label(), l2.get_label()],
              fontsize=8, prop={"family": FONT},
              framealpha=0.9, edgecolor="#CCCCCC", loc="upper left")

fig.suptitle(
    "Appendice A1 — Évolution mensuelle de la demande et des dépenses marketing par canal (E-Commerce)",
    fontsize=11, fontweight="bold", fontfamily=FONT, color="#1F3864", y=1.005
)
fig.text(0.5, -0.005,
         "Source : Auteur, à partir des données propriétaires E-Commerce (2022–2024). "
         "ρ = coefficient de corrélation de Pearson.",
         ha="center", fontsize=7.5, fontfamily=FONT,
         color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Appendice_A1_Demande_Par_Canal.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
