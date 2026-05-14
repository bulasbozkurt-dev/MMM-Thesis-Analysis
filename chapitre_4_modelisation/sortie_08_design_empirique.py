import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(18, 12))
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis("off")
fig.patch.set_facecolor("#FFFFFF")

FONT = "DejaVu Serif"

C_MARK = "#1E6B3C"
C_RET  = "#7B2D8B"
C_CHOC = "#C00000"
C_FIX  = "#B45309"
C_CTRL = "#1565A8"
C_DEP  = "#1F3864"
C_ERR  = "#555555"

def boite(ax, x, y, w, h, texte, couleur, fontsize=8.5, bold=False):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.08,rounding_size=0.2",
                         linewidth=1.2, edgecolor=couleur,
                         facecolor=couleur + "18")
    ax.add_patch(box)
    ax.text(x, y, texte, ha="center", va="center",
            fontsize=fontsize, fontweight="bold" if bold else "normal",
            color=couleur, fontfamily=FONT, multialignment="center")

def fleche(ax, x1, y1, x2, y2, couleur, lw=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=couleur,
                                lw=lw, connectionstyle="arc3,rad=0.0"))

# ── Titre ─────────────────────────────────────────────────────────────────────
ax.text(9, 11.6, "Modèle de mix marketing — E-commerce et FMCG",
        ha="center", va="center", fontsize=10, fontfamily=FONT,
        color="#555555", style="italic")

# ── Variable dépendante ───────────────────────────────────────────────────────
boite(ax, 15.2, 6.0, 3.0, 1.4,
      "Variable dépendante\nD : Commandes /\nVolume des ventes",
      C_DEP, fontsize=8.5, bold=True)

# ── Terme d'erreur ────────────────────────────────────────────────────────────
boite(ax, 15.2, 3.2, 2.4, 0.7, "ε : Terme d'erreur", C_ERR, fontsize=8)
fleche(ax, 15.2, 3.56, 15.2, 5.28, C_ERR, lw=1.0)

# ── Équation MCO ──────────────────────────────────────────────────────────────
eq_box = FancyBboxPatch((5.5, 5.4), 5.8, 1.2,
                        boxstyle="round,pad=0.1,rounding_size=0.15",
                        linewidth=1.4, edgecolor="#1F3864",
                        facecolor="#EBF0F8")
ax.add_patch(eq_box)
ax.text(8.4, 6.0,
        r"$D_t = \alpha + \sum_k \beta_k M_{k,t} + \sum_j \gamma_j F_{j,t} + \sum_m \delta_m S_{m,t} + \sum_l \lambda_l C_{l,t} + \varepsilon_t$",
        ha="center", va="center", fontsize=9.5, color="#1F3864",
        fontfamily=FONT)
fleche(ax, 11.3, 6.0, 13.65, 6.0, C_DEP, lw=2.0)

# ── Variables marketing ───────────────────────────────────────────────────────
mark_items = [
    (2.2, 10.2, "M : Google"),
    (2.2, 8.9,  "M : Meta"),
    (2.2, 7.6,  "M : Influenceur"),
    (2.2, 6.3,  "M : Indice de\ndépenses"),
    (2.2, 5.0,  "M : Pondéré\n(FMCG)"),
]
for x, y, label in mark_items:
    boite(ax, x, y, 2.8, 0.75, label, C_MARK, fontsize=8)
    fleche(ax, 3.6, y, 5.5, 6.0, C_MARK, lw=1.0)

# ── Variables retardées ───────────────────────────────────────────────────────
ret_items = [
    (7.2, 10.2, "M : Retard t−1\n(E-commerce)"),
    (7.2, 9.0,  "M : Retard t−7\n(E-commerce)"),
    (7.2, 7.8,  "D : Retard t−1"),
]
for x, y, label in ret_items:
    boite(ax, x, y, 2.8, 0.75, label, C_RET, fontsize=8)
    fleche(ax, 8.6, y, 11.3, 6.1, C_RET, lw=1.0)

# ── Effets fixes ──────────────────────────────────────────────────────────────
fix_items = [
    (2.2, 3.7, "Facteur saisonnier"),
    (2.2, 2.8, "Effet week-end"),
]
for x, y, label in fix_items:
    boite(ax, x, y, 2.8, 0.65, label, C_FIX, fontsize=8)
    fleche(ax, 3.6, y, 5.5, 5.9, C_FIX, lw=1.0)

# ── Variables de choc ─────────────────────────────────────────────────────────
choc_items = [
    (7.5, 4.5, "Choc : taux de change"),
    (7.5, 3.3, "Choc : crise logistique\n(E-commerce)"),
    (7.5, 2.0, "Choc : effet du séisme\n(FMCG)"),
]
for x, y, label in choc_items:
    boite(ax, x, y, 3.2, 0.75, label, C_CHOC, fontsize=8)
    fleche(ax, 9.1, y, 11.3, 5.9, C_CHOC, lw=1.0)

# ── Variables de contrôle ─────────────────────────────────────────────────────
ctrl_items = [
    (2.2, 1.7, "Dépenses des\nconcurrents"),
    (2.2, 0.8, "Part de voix (%)"),
]
for x, y, label in ctrl_items:
    boite(ax, x, y, 2.8, 0.65, label, C_CTRL, fontsize=8)
    fleche(ax, 3.6, y, 5.5, 5.8, C_CTRL, lw=1.0)

# ── Légende ───────────────────────────────────────────────────────────────────
legend_items = [
    (C_MARK, "Variables marketing"),
    (C_RET,  "Variables retardées"),
    (C_CHOC, "Variables de choc"),
    (C_FIX,  "Effets fixes / saisonnalité"),
    (C_CTRL, "Variables de contrôle"),
    (C_DEP,  "Variable dépendante"),
    (C_ERR,  "Terme d'erreur"),
]
patches = [mpatches.Patch(facecolor=c + "33", edgecolor=c,
                          linewidth=1.2, label=l)
           for c, l in legend_items]
ax.legend(handles=patches, loc="lower center", ncol=4,
          bbox_to_anchor=(0.5, -0.03), fontsize=8,
          prop={"family": FONT}, frameon=True,
          framealpha=0.9, edgecolor="#CCCCCC")

plt.tight_layout(pad=0.5)
output_path = "Figure_04_Design_Empirique_Modele.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
