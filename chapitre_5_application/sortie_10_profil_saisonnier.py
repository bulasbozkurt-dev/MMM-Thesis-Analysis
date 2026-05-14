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

MOIS_FR = ["Jan.", "Fév.", "Mars", "Avr.", "Mai", "Juin",
           "Juil.", "Août", "Sept.", "Oct.", "Nov.", "Déc."]

ec_mois = df_ec.groupby(df_ec["Date"].dt.month)["D : Total quotidien"].mean()
fg_mois = df_fg.groupby(df_fg["Date"].dt.month)["D : Volume des ventes"].mean()

ec_trim = df_ec.groupby(" Trimestre" if " Trimestre" in df_ec.columns
                         else df_ec["Date"].dt.quarter)["D : Total quotidien"].mean()
fg_trim = df_fg.groupby(df_fg[" Trimestre"].values if " Trimestre" in df_fg.columns
                         else df_fg["Date"].dt.quarter)["D : Volume des ventes"].mean()

if " Trimestre" in df_fg.columns:
    fg_trim = df_fg.groupby(" Trimestre")["D : Volume des ventes"].mean()
else:
    fg_trim = df_fg.groupby(df_fg["Date"].dt.quarter)["D : Volume des ventes"].mean()

if " Trimestre" in df_ec.columns:
    ec_trim = df_ec.groupby(" Trimestre")["D : Total quotidien"].mean()
else:
    ec_trim = df_ec.groupby(df_ec["Date"].dt.quarter)["D : Total quotidien"].mean()

FONT  = "DejaVu Serif"
C_EC  = "#1F3864"
C_FG  = "#1E6B3C"
C_BAR = "#B45309"

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.patch.set_facecolor("#FAFAFA")

def style_ax(ax):
    ax.set_facecolor("#F7F9FC")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)

# ── E-Commerce mensuel ────────────────────────────────────────────────────────
ax = axes[0, 0]
style_ax(ax)
mois_idx = ec_mois.index.tolist()
vals = ec_mois.values
couleurs = [C_EC if v >= np.mean(vals) else "#7FA8D4" for v in vals]
bars = ax.bar([MOIS_FR[m-1] for m in mois_idx], vals,
              color=couleurs, edgecolor="white", linewidth=0.8, width=0.7)
ax.axhline(np.mean(vals), color=C_BAR, lw=1.5, linestyle="--",
           label=f"Moyenne = {np.mean(vals):,.0f}")
ax.set_title("E-Commerce — Profil mensuel de la demande",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Commandes moyennes / jour", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h * 1.01,
            f"{h:,.0f}", ha="center", va="bottom", fontsize=7, fontfamily=FONT, color="#333")

# ── FMCG mensuel ──────────────────────────────────────────────────────────────
ax = axes[0, 1]
style_ax(ax)
mois_idx_fg = fg_mois.index.tolist()
vals_fg = fg_mois.values
couleurs_fg = [C_FG if v >= np.mean(vals_fg) else "#82C49E" for v in vals_fg]
bars_fg = ax.bar([MOIS_FR[m-1] for m in mois_idx_fg], vals_fg,
                 color=couleurs_fg, edgecolor="white", linewidth=0.8, width=0.7)
ax.axhline(np.mean(vals_fg), color=C_BAR, lw=1.5, linestyle="--",
           label=f"Moyenne = {np.mean(vals_fg):,.0f}")
ax.set_title("FMCG — Profil mensuel de la demande",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Volume moyen des ventes / semaine", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")
for bar in bars_fg:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h * 1.01,
            f"{h:,.0f}", ha="center", va="bottom", fontsize=7, fontfamily=FONT, color="#333")

# ── E-Commerce trimestriel ────────────────────────────────────────────────────
ax = axes[1, 0]
style_ax(ax)
trim_labels = [f"T{int(t)}" for t in ec_trim.index]
vals_t = ec_trim.values
ax.bar(trim_labels, vals_t, color=C_EC, alpha=0.75,
       edgecolor="white", linewidth=0.8, width=0.5)
ax.axhline(np.mean(vals_t), color=C_BAR, lw=1.5, linestyle="--",
           label=f"Moyenne = {np.mean(vals_t):,.0f}")
ax.set_title("E-Commerce — Profil trimestriel de la demande",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Commandes moyennes / jour", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")
for i, v in enumerate(vals_t):
    ax.text(i, v * 1.01, f"{v:,.0f}", ha="center", va="bottom",
            fontsize=9, fontfamily=FONT, fontweight="bold", color="#1F3864")

# ── FMCG trimestriel ──────────────────────────────────────────────────────────
ax = axes[1, 1]
style_ax(ax)
trim_labels_fg = [f"T{int(t)}" for t in fg_trim.index]
vals_t_fg = fg_trim.values
ax.bar(trim_labels_fg, vals_t_fg, color=C_FG, alpha=0.75,
       edgecolor="white", linewidth=0.8, width=0.5)
ax.axhline(np.mean(vals_t_fg), color=C_BAR, lw=1.5, linestyle="--",
           label=f"Moyenne = {np.mean(vals_t_fg):,.0f}")
ax.set_title("FMCG — Profil trimestriel de la demande",
             fontsize=10, fontweight="bold", fontfamily=FONT, color="#1F3864", pad=8)
ax.set_ylabel("Volume moyen des ventes / semaine", fontsize=8.5, fontfamily=FONT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(fontsize=8, prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")
for i, v in enumerate(vals_t_fg):
    ax.text(i, v * 1.01, f"{v:,.0f}", ha="center", va="bottom",
            fontsize=9, fontfamily=FONT, fontweight="bold", color="#1E6B3C")

fig.suptitle("Figure 4 — Profil saisonnier de la demande",
             fontsize=13, fontweight="bold", fontfamily=FONT,
             color="#1F3864", y=1.01)

fig.text(0.5, -0.01,
         "Source : Auteur, à partir des données propriétaires E-Commerce et FMCG (2022–2024). "
         "Couleur foncée = valeur supérieure à la moyenne.",
         ha="center", fontsize=7.5, fontfamily=FONT, color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Figure_10_Profil_Saisonnier_Demande.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
