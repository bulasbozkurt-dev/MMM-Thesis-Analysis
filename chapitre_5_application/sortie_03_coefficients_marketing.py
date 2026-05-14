import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import statsmodels.api as sm

df_ec = pd.read_excel("E-Ticaret_MMM_v2.xlsx")
df_fg = pd.read_excel("FMCG_MMM_v2.xlsx")
df_ec.columns = [c.strip() for c in df_ec.columns]
df_fg.columns = [c.strip() for c in df_fg.columns]

FONT = "DejaVu Serif"

VARS_MARK_EC = [
    "M : Google", "M : Meta", "M : Influenceur", "M : Indice de dépenses",
    "M : Retard t-1", "M : Retard t-7",
]
VARS_MARK_FG = [
    "M : Dépenses marketing totales", "M : Pondéré",
    "M : Retard 1 semaine", "M : Retard 4 semaines",
]

ALL_VARS_EC = VARS_MARK_EC + [
    "D : Retard t-1", "Choc : Taux de change", "Choc : Crise logistique",
    "Facteur saisonnier", "Effet du dimanche",
    "Dépenses des concurrents", "Part de voix (%)", "Taux de conversion (%)",
]
ALL_VARS_FG = VARS_MARK_FG + [
    "D : Retard 1 semaine", "Choc : Taux de change", "Choc : Impact du séisme",
    "Facteur saisonnier",
    "Dépenses marketing des concurrents", "Part de voix (%)", "Part de marché (%)",
    "Rupture de stock (%)", "Stock (jours)", "Efficacité marketing",
]

def estimer_sm(df, dep, vars_list):
    valid = [v for v in vars_list if v in df.columns]
    sub   = df[[dep] + valid].dropna()
    Y     = sub[dep]
    X     = sm.add_constant(sub[valid], has_constant="add")
    mod   = sm.OLS(Y, X).fit()
    ci    = mod.conf_int()
    return {
        "params":  mod.params.to_dict(),
        "pvalues": mod.pvalues.to_dict(),
        "ci_low":  ci[0].to_dict(),
        "ci_high": ci[1].to_dict(),
    }

res_ec = estimer_sm(df_ec, "D : Commandes (canal)", ALL_VARS_EC)
res_fg = estimer_sm(df_fg, "D : Volume des ventes",  ALL_VARS_FG)

LABELS_EC = {
    "M : Google":             "Google",
    "M : Meta":               "Meta",
    "M : Influenceur":        "Influenceur",
    "M : Indice de dépenses": "Indice dép.",
    "M : Retard t-1":         "Retard t−1",
    "M : Retard t-7":         "Retard t−7",
}
LABELS_FG = {
    "M : Dépenses marketing totales": "Dép. totales",
    "M : Pondéré":                    "Pondéré",
    "M : Retard 1 semaine":           "Retard 1 sem.",
    "M : Retard 4 semaines":          "Retard 4 sem.",
}

def couleur_barre(coef, pval):
    sig = pval < 0.05
    if coef > 0:
        return "#1E6B3C" if sig else "#82C49E"
    return "#C00000" if sig else "#F4AAAA"

def tracer_coefs(ax, res, vars_list, labels_map, titre, xlim=None):
    ax.set_facecolor("#F7F9FC")
    coefs = [res["params"][v]  for v in vars_list if v in res["params"]]
    pvals = [res["pvalues"][v] for v in vars_list if v in res["pvalues"]]
    ci_lo = [res["ci_low"][v]  for v in vars_list if v in res["ci_low"]]
    ci_hi = [res["ci_high"][v] for v in vars_list if v in res["ci_high"]]
    noms  = [labels_map.get(v, v) for v in vars_list if v in res["params"]]

    idx      = np.arange(len(noms))
    couleurs = [couleur_barre(c, p) for c, p in zip(coefs, pvals)]

    ax.barh(idx, coefs, color=couleurs, edgecolor="white",
            linewidth=0.8, height=0.6, zorder=3)

    for i, (c, lo, hi) in enumerate(zip(coefs, ci_lo, ci_hi)):
        if xlim:
            lo_plot = max(lo, xlim[0])
            hi_plot = min(hi, xlim[1])
        else:
            lo_plot, hi_plot = lo, hi
        ax.plot([lo_plot, hi_plot], [i, i], color="#333333",
                lw=1.5, solid_capstyle="round", zorder=4)
        ax.plot([lo_plot, lo_plot], [i-0.12, i+0.12],
                color="#333333", lw=1.2, zorder=4)
        ax.plot([hi_plot, hi_plot], [i-0.12, i+0.12],
                color="#333333", lw=1.2, zorder=4)

    for i, (c, p) in enumerate(zip(coefs, pvals)):
        sig_label = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
        if sig_label:
            ref = xlim[1] * 0.03 if xlim else abs(max(coefs, default=1)) * 0.05
            x_pos = c + ref if c >= 0 else c - ref
            if xlim:
                x_pos = min(max(x_pos, xlim[0] + ref), xlim[1] - ref)
            ha = "left" if c >= 0 else "right"
            ax.text(x_pos, i, sig_label, ha=ha, va="center",
                    fontsize=9, color="#333333",
                    fontfamily=FONT, fontweight="bold")

    ax.axvline(0, color="#555555", lw=1.0, zorder=2)
    if xlim:
        ax.set_xlim(xlim)
    ax.set_yticks(idx)
    ax.set_yticklabels(noms, fontsize=9, fontfamily=FONT)
    ax.set_xlabel("Coefficient MCO (avec IC à 95%)", fontsize=9, fontfamily=FONT)
    ax.set_title(titre, fontsize=10.5, fontweight="bold",
                 fontfamily=FONT, color="#1F3864", pad=8)
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels():
        lbl.set_fontfamily(FONT)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4, color="#AAAAAA", zorder=1)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#FAFAFA")

tracer_coefs(axes[0], res_ec, VARS_MARK_EC, LABELS_EC,
             "E-Commerce — Coefficients\ndes variables marketing",
             xlim=(-2.5, 4.0))

tracer_coefs(axes[1], res_fg, VARS_MARK_FG, LABELS_FG,
             "FMCG — Coefficients\ndes variables marketing")

axes[0].annotate("Note : IC tronqués pour\nIndice dép. (multicolinéarité)",
                 xy=(0.02, 0.02), xycoords="axes fraction",
                 fontsize=7, fontfamily=FONT, color="#888888", style="italic")

legende = [
    mpatches.Patch(facecolor="#1E6B3C", label="Positif significatif (p < 0,05)"),
    mpatches.Patch(facecolor="#82C49E", label="Positif non significatif"),
    mpatches.Patch(facecolor="#C00000", label="Négatif significatif (p < 0,05)"),
    mpatches.Patch(facecolor="#F4AAAA", label="Négatif non significatif"),
]
fig.legend(handles=legende, loc="lower center", ncol=4,
           bbox_to_anchor=(0.5, -0.05), fontsize=8.5,
           prop={"family": FONT}, framealpha=0.9, edgecolor="#CCCCCC")

fig.suptitle("Figure 5.1 — Coefficients MCO des variables marketing",
             fontsize=13, fontweight="bold", fontfamily=FONT,
             color="#1F3864", y=1.02)

fig.text(0.5, -0.10,
         "Note : Les barres d'erreur représentent l'intervalle de confiance à 95%. "
         "*** p < 0,01 ; ** p < 0,05 ; * p < 0,10.\n"
         "Source : Auteur, estimations MCO (statsmodels) à partir des données synthétiques (2022–2024).",
         ha="center", fontsize=7.5, fontfamily=FONT,
         color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Figure_13_Coefficients_Variables_Marketing.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
