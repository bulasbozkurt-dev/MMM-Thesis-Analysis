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

FONT  = "DejaVu Serif"
C1, C2, C3, C4 = "#1F3864", "#1E6B3C", "#B45309", "#7B2D8B"

# ── E-Commerce : canaux marketing ─────────────────────────────────────────────
canaux_ec = {
    "Google":      "M : Google",
    "Meta":        "M : Meta",
    "Influenceur": "M : Influenceur",
}
totaux_ec = {k: df_ec[v].sum() for k, v in canaux_ec.items()}
total_ec  = sum(totaux_ec.values())
pcts_ec   = {k: v / total_ec * 100 for k, v in totaux_ec.items()}

# ── E-Commerce : évolution mensuelle par canal ────────────────────────────────
ec_men = df_ec.copy()
ec_men["Mois"] = ec_men["Date"].dt.to_period("M").dt.to_timestamp()
ec_canal_mois = ec_men.groupby("Mois")[list(canaux_ec.values())].mean()
ec_canal_mois.columns = list(canaux_ec.keys())

# ── FMCG : dépenses totales vs pondérées ─────────────────────────────────────
fg_vars = {
    "Dépenses totales":  "M : Dépenses marketing totales",
    "Dépenses pondérées":"M : Pondéré",
}
totaux_fg = {k: df_fg[v].sum() for k, v in fg_vars.items()}

# ── FMCG : évolution hebdomadaire ─────────────────────────────────────────────
fg_hebdo = df_fg.copy()
fg_hebdo["Semaine"] = fg_hebdo["Date"].dt.to_period("W").dt.to_timestamp()
fg_mark_hebdo = fg_hebdo.groupby("Semaine")[list(fg_vars.values())].mean()
fg_mark_hebdo.columns = list(fg_vars.keys())

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.patch.set_facecolor("#FAFAFA")

def style_ax(ax):
    ax.set_facecolor("#F7F9FC")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)

# ── Panneau 1 : camembert E-Commerce ─────────────────────────────────────────
ax = axes[0, 0]
ax.set_facecolor("#F7F9FC")
couleurs_pie = [C1, C2, C3]
wedges, texts, autotexts = ax.pie(
    list(pcts_ec.values()),
    labels=list(pcts_ec.keys()),
    colors=couleurs_pie,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.75,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    textprops={"fontfamily": FONT, "fontsize": 9},
)
for at in autotexts:
    at.set_fontsize(8.5)
    at.set_fontfamily(FONT)
    at.set_color("white")
    at.set_fontweight("bold")
ax.set_title("E-Commerce — Répartition des dépenses\nmarketing par canal",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.text(0, -1.35,
        f"Total = {total_ec:,.0f} (indice cumulé)",
        ha="center", fontsize=8, fontfamily=FONT, color="#555", style="italic")

# ── Panneau 2 : évolution mensuelle E-Commerce ───────────────────────────────
ax = axes[0, 1]
style_ax(ax)
couleurs_ec = [C1, C2, C3]
for i, (canal, col) in enumerate(zip(ec_canal_mois.columns, couleurs_ec)):
    ax.plot(ec_canal_mois.index, ec_canal_mois[canal],
            color=col, lw=1.8, label=canal, marker="o", markersize=3)
ax.set_title("E-Commerce — Évolution mensuelle\ndes dépenses par canal",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Dépenses moyennes (indice)", fontsize=8.5, fontfamily=FONT)
ax.set_xlabel("Période (mensuelle)", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.2f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9,
          edgecolor="#CCCCCC", loc="upper left")

# ── Panneau 3 : barres FMCG ───────────────────────────────────────────────────
ax = axes[1, 0]
style_ax(ax)
labels_fg = list(totaux_fg.keys())
vals_fg   = list(totaux_fg.values())
bars = ax.bar(labels_fg, vals_fg,
              color=[C1, C2], edgecolor="white", linewidth=0.8, width=0.45)
ax.set_title("FMCG — Dépenses marketing totales\nvs pondérées (cumul)",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Dépenses cumulées (₺)", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h * 1.01,
            f"{h:,.0f} ₺", ha="center", va="bottom",
            fontsize=8.5, fontfamily=FONT, fontweight="bold", color="#333")

# ── Panneau 4 : évolution hebdomadaire FMCG ──────────────────────────────────
ax = axes[1, 1]
style_ax(ax)
for i, (label, col) in enumerate(zip(fg_mark_hebdo.columns, [C1, C2])):
    ax.plot(fg_mark_hebdo.index, fg_mark_hebdo[label],
            color=col, lw=1.8, label=label,
            linestyle="-" if i == 0 else "--", marker=".", markersize=2)
ax.set_title("FMCG — Évolution hebdomadaire des\ndépenses marketing",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Dépenses moyennes (₺)", fontsize=8.5, fontfamily=FONT)
ax.set_xlabel("Période (hebdomadaire)", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9,
          edgecolor="#CCCCCC", loc="upper left")

fig.suptitle("Figure 5 — Composition des dépenses marketing",
             fontsize=13, fontweight="bold", fontfamily=FONT,
             color="#1F3864", y=1.01)

fig.text(0.5, -0.01,
         "Source : Auteur, à partir des données propriétaires E-Commerce et FMCG (2022–2024).",
         ha="center", fontsize=7.5, fontfamily=FONT, color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Figure_11_Composition_Depenses_Marketing.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
