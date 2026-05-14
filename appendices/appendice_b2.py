import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

df = pd.read_excel("FMCG_MMM_v2.xlsx")
df.columns = [c.strip() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"])

FONT    = "DejaVu Serif"
REGIONS = sorted(df["Région"].dropna().unique())
COLORS  = ["#1F3864", "#1E6B3C", "#C00000", "#B45309",
           "#7B2D8B", "#0D7377", "#8B4513", "#2F4F4F"]
MOIS_FR = ["Jan.", "Fév.", "Mars", "Avr.", "Mai", "Juin",
           "Juil.", "Août", "Sept.", "Oct.", "Nov.", "Déc."]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#FAFAFA")

# ── Panneau 1 : évolution hebdomadaire par région ─────────────────────────────
ax = axes[0]
ax.set_facecolor("#F7F9FC")

for i, region in enumerate(REGIONS):
    sub = df[df["Région"] == region].sort_values("Date")
    heb = sub.groupby(sub["Date"].dt.to_period("W"))[
        "Part de marché (%)"
    ].mean().reset_index()
    heb["Date"] = heb["Date"].dt.to_timestamp()
    ax.plot(heb["Date"], heb["Part de marché (%)"],
            color=COLORS[i % len(COLORS)], lw=1.8,
            label=region, marker=".", markersize=2)

ax.set_title("Évolution hebdomadaire de la\npart de marché par région",
             fontsize=10.5, fontweight="bold",
             fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Part de marché (%)", fontsize=9, fontfamily=FONT)
ax.set_xlabel("Période (hebdomadaire)", fontsize=9, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"{x:.1f}%"))
ax.tick_params(labelsize=8)
for lbl in ax.get_xticklabels() + ax.get_yticklabels():
    lbl.set_fontfamily(FONT)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(fontsize=8.5, prop={"family": FONT},
          framealpha=0.9, edgecolor="#CCCCCC",
          title="Région", title_fontsize=8.5)
ax.grid(axis="y", linestyle="--", alpha=0.4, color="#AAAAAA")

# ── Panneau 2 : profil mensuel moyen par région (barres groupées) ─────────────
ax = axes[1]
ax.set_facecolor("#F7F9FC")

mois_data = {}
for region in REGIONS:
    sub = df[df["Région"] == region]
    grp = sub.groupby(sub["Date"].dt.month)["Part de marché (%)"].mean()
    mois_data[region] = grp

mois_idx  = sorted(set().union(*[d.index for d in mois_data.values()]))
x         = np.arange(len(mois_idx))
n_reg     = len(REGIONS)
width     = 0.8 / n_reg
offsets   = np.linspace(-(n_reg-1)/2, (n_reg-1)/2, n_reg) * width

for i, region in enumerate(REGIONS):
    vals = [mois_data[region].get(m, np.nan) for m in mois_idx]
    bars = ax.bar(x + offsets[i], vals, width=width,
                  color=COLORS[i % len(COLORS)], label=region,
                  edgecolor="white", linewidth=0.5, alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels([MOIS_FR[m-1] for m in mois_idx], fontsize=8)
for lbl in ax.get_xticklabels() + ax.get_yticklabels():
    lbl.set_fontfamily(FONT)
ax.set_title("Profil mensuel moyen de la\npart de marché par région",
             fontsize=10.5, fontweight="bold",
             fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Part de marché moyenne (%)", fontsize=9, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"{x:.1f}%"))
ax.tick_params(labelsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(fontsize=8.5, prop={"family": FONT},
          framealpha=0.9, edgecolor="#CCCCCC",
          title="Région", title_fontsize=8.5)
ax.grid(axis="y", linestyle="--", alpha=0.4, color="#AAAAAA")

# ── Statistiques par région ───────────────────────────────────────────────────
for i, region in enumerate(REGIONS):
    s = df[df["Région"] == region]["Part de marché (%)"].dropna()
    axes[0].text(0.02, 0.97 - i * 0.09,
                 f"{region} : μ={s.mean():.2f}%  σ={s.std():.2f}%",
                 transform=axes[0].transAxes, ha="left", va="top",
                 fontsize=7.2, fontfamily=FONT,
                 color=COLORS[i % len(COLORS)],
                 bbox=dict(boxstyle="round,pad=0.2", fc="white",
                           ec="none", alpha=0.85))

fig.suptitle(
    "Appendice B2 — Part de marché par région (FMCG)",
    fontsize=12, fontweight="bold", fontfamily=FONT,
    color="#1F3864", y=1.01
)
fig.text(0.5, -0.02,
         "Source : Auteur, à partir des données propriétaires FMCG (2022–2024).",
         ha="center", fontsize=7.5, fontfamily=FONT,
         color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Appendice_B2_Part_Marche_Par_Region.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
