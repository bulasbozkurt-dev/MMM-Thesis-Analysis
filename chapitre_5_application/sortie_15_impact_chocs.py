import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

df_ec = pd.read_excel("E-Ticaret_MMM_v2.xlsx")
df_fg = pd.read_excel("FMCG_MMM_v2.xlsx")
df_ec.columns = [c.strip() for c in df_ec.columns]
df_fg.columns = [c.strip() for c in df_fg.columns]

df_ec["Date"] = pd.to_datetime(df_ec["Date"])
df_fg["Date"] = pd.to_datetime(df_fg["Date"])

FONT  = "DejaVu Serif"
C_EC  = "#1F3864"
C_FG  = "#1E6B3C"
C_CH1 = "#C00000"
C_CH2 = "#B45309"
C_CH3 = "#7B2D8B"

def estimer_coef_choc(df, dep, choc_var, autres_vars):
    valid = [v for v in autres_vars + [choc_var] if v in df.columns]
    sub   = df[[dep] + valid].dropna()
    Y     = sub[dep].values
    X     = np.column_stack([np.ones(len(Y)), sub[valid].values])
    params, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
    n, k  = X.shape
    fitted = X @ params
    resid  = Y - fitted
    sigma2 = (resid @ resid) / (n - k)
    cov    = sigma2 * np.linalg.inv(X.T @ X)
    bse    = np.sqrt(np.diag(cov))
    index  = ["const"] + valid
    coef_map = dict(zip(index, params))
    bse_map  = dict(zip(index, bse))
    t_crit   = scipy_stats.t.ppf(0.975, df=n-k)
    pval     = dict(zip(index, 2 * scipy_stats.t.sf(
        np.abs(params / bse), df=n-k)))
    ci_lo    = dict(zip(index, params - t_crit * bse))
    ci_hi    = dict(zip(index, params + t_crit * bse))
    return coef_map, bse_map, pval, ci_lo, ci_hi

CTRL_EC = [
    "M : Google", "M : Meta", "M : Influenceur", "M : Indice de dépenses",
    "M : Retard t-1", "M : Retard t-7", "D : Retard t-1",
    "Facteur saisonnier", "Effet du dimanche",
    "Dépenses des concurrents", "Part de voix (%)", "Taux de conversion (%)",
]
CTRL_FG = [
    "M : Dépenses marketing totales", "M : Pondéré",
    "M : Retard 1 semaine", "M : Retard 4 semaines", "D : Retard 1 semaine",
    "Facteur saisonnier",
    "Dépenses marketing des concurrents", "Part de voix (%)", "Part de marché (%)",
    "Rupture de stock (%)", "Stock (jours)", "Efficacité marketing",
]

CHOCS_EC = {
    "Choc : Taux de change":   ("Choc : Taux\nde change",   C_CH1),
    "Choc : Crise logistique": ("Choc : Crise\nlogistique",  C_CH2),
}
CHOCS_FG = {
    "Choc : Taux de change":  ("Choc : Taux\nde change",  C_CH1),
    "Choc : Impact du séisme":("Choc : Impact\ndu séisme", C_CH3),
}

def collecter_chocs(df, dep, chocs_dict, ctrl_vars):
    resultats = {}
    for var, (label, couleur) in chocs_dict.items():
        if var not in df.columns:
            continue
        cm, bm, pv, clo, chi = estimer_coef_choc(df, dep, var, ctrl_vars)
        resultats[var] = {
            "label":   label,
            "couleur": couleur,
            "coef":    cm.get(var, np.nan),
            "bse":     bm.get(var, np.nan),
            "pval":    pv.get(var, np.nan),
            "ci_lo":   clo.get(var, np.nan),
            "ci_hi":   chi.get(var, np.nan),
        }
    return resultats

res_chocs_ec = collecter_chocs(df_ec, "D : Commandes (canal)", CHOCS_EC, CTRL_EC)
res_chocs_fg = collecter_chocs(df_fg, "D : Volume des ventes",  CHOCS_FG, CTRL_FG)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor("#FAFAFA")

def style_ax(ax):
    ax.set_facecolor("#F7F9FC")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)

def sig_label(p):
    if p < 0.01:  return "***"
    if p < 0.05:  return "**"
    if p < 0.10:  return "*"
    return "n.s."

# ── Panneau 1 : coefficients des chocs (barres) ───────────────────────────────
def panneau_coefs(ax, res_dict, titre, dep_label):
    style_ax(ax)
    noms    = [v["label"]   for v in res_dict.values()]
    coefs   = [v["coef"]    for v in res_dict.values()]
    ci_los  = [v["ci_lo"]   for v in res_dict.values()]
    ci_his  = [v["ci_hi"]   for v in res_dict.values()]
    pvals   = [v["pval"]    for v in res_dict.values()]
    couleurs= [v["couleur"] for v in res_dict.values()]

    idx  = np.arange(len(noms))
    bars = ax.barh(idx, coefs, color=couleurs, edgecolor="white",
                   linewidth=0.8, height=0.45, zorder=3, alpha=0.85)
    for i, (c, lo, hi) in enumerate(zip(coefs, ci_los, ci_his)):
        ax.plot([lo, hi], [i, i], color="#333333", lw=1.8,
                solid_capstyle="round", zorder=4)
        ax.plot([lo, lo], [i-0.1, i+0.1], color="#333333", lw=1.2, zorder=4)
        ax.plot([hi, hi], [i-0.1, i+0.1], color="#333333", lw=1.2, zorder=4)
    for i, (c, p) in enumerate(zip(coefs, pvals)):
        sig = sig_label(p)
        offset = abs(max(coefs, default=1)) * 0.05 if max(coefs, default=1) != 0 else 0.05
        x_pos  = c + offset if c >= 0 else c - offset
        ha     = "left" if c >= 0 else "right"
        ax.text(x_pos, i, sig, ha=ha, va="center", fontsize=10,
                fontfamily=FONT, fontweight="bold", color="#333333")
    ax.axvline(0, color="#555555", lw=1.0, zorder=2)
    ax.set_yticks(idx)
    ax.set_yticklabels(noms, fontsize=9, fontfamily=FONT)
    ax.set_xlabel(f"Coefficient MCO (impact sur {dep_label})", fontsize=8.5, fontfamily=FONT)
    ax.set_title(titre, fontsize=10, fontweight="bold",
                 fontfamily=FONT, color="#1F3864", pad=7)
    ax.grid(axis="x", linestyle="--", alpha=0.4, color="#AAAAAA", zorder=1)

panneau_coefs(axes[0, 0], res_chocs_ec,
              "E-Commerce — Coefficients MCO des variables de choc",
              "commandes")
panneau_coefs(axes[1, 0], res_chocs_fg,
              "FMCG — Coefficients MCO des variables de choc",
              "volume des ventes")

# ── Panneau 2 : évolution temporelle avec zones de choc ──────────────────────
def panneau_serie_choc(ax, df, dep, chocs_dict, titre, dep_label, couleur_dep):
    style_ax(ax)
    serie = df[[dep, "Date"]].dropna()
    serie = serie.sort_values("Date")
    ax.plot(serie["Date"], serie[dep], color=couleur_dep,
            lw=1.3, alpha=0.75, label=dep_label)

    couleurs_choc = [C_CH1, C_CH2, C_CH3]
    for i, (var, (label, coul)) in enumerate(chocs_dict.items()):
        if var not in df.columns:
            continue
        sub_choc = df[["Date", dep, var]].dropna()
        sub_choc = sub_choc[sub_choc[var] > 0].sort_values("Date")
        if len(sub_choc) == 0:
            continue
        ymin = serie[dep].min()
        ymax = serie[dep].max()
        for _, row_c in sub_choc.iterrows():
            ax.axvspan(row_c["Date"] - pd.Timedelta(days=1),
                       row_c["Date"] + pd.Timedelta(days=1),
                       alpha=0.18, color=coul, zorder=1)
        proxy = mpatches.Patch(color=coul, alpha=0.4, label=label.replace("\n", " "))
        ax.plot([], [], color=coul, linewidth=4, alpha=0.4,
                label=label.replace("\n", " "))

    ax.set_title(titre, fontsize=10, fontweight="bold",
                 fontfamily=FONT, color="#1F3864", pad=7)
    ax.set_ylabel(dep_label, fontsize=8.5, fontfamily=FONT)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.legend(fontsize=7.5, prop={"family": FONT}, framealpha=0.9,
              edgecolor="#CCCCCC", loc="upper left", ncol=1)

panneau_serie_choc(
    axes[0, 1], df_ec, "D : Commandes (canal)", CHOCS_EC,
    "E-Commerce — Périodes de choc et demande",
    "Commandes", C_EC
)
panneau_serie_choc(
    axes[1, 1], df_fg, "D : Volume des ventes", CHOCS_FG,
    "FMCG — Périodes de choc et demande",
    "Volume des ventes", C_FG
)

fig.suptitle("Figure 8 — Impact des chocs sur la demande",
             fontsize=13, fontweight="bold", fontfamily=FONT,
             color="#1F3864", y=1.01)

fig.text(0.5, -0.01,
         "Note : *** p < 0,01 ; ** p < 0,05 ; * p < 0,10 ; n.s. = non significatif. "
         "Les zones colorées indiquent les périodes d'activation du choc.\n"
         "Source : Auteur, estimations MCO à partir des données propriétaires (2022–2024).",
         ha="center", fontsize=7.5, fontfamily=FONT, color="#777777", style="italic")

plt.tight_layout(pad=2.5)
output_path = "Figure_15_Impact_Chocs.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
