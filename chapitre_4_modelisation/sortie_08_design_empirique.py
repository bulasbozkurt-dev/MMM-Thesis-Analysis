import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")
fig.patch.set_facecolor("#FAFAFA")

# ── Couleurs ──────────────────────────────────────────────────────────────────
C_DEP   = "#1F3864"   # variable dépendante
C_MARK  = "#1E6B3C"   # variables marketing
C_RETARD= "#7B2D8B"   # retards
C_CHOC  = "#C00000"   # chocs
C_FIX   = "#B45309"   # effets fixes
C_CTRL  = "#1565A8"   # contrôle
C_ERR   = "#555555"   # erreur
C_ARROW = "#333333"

def boite(ax, x, y, w, h, texte, couleur, taille=9, bold=False, radius=0.3):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=f"round,pad=0.05,rounding_size={radius}",
                         linewidth=1.2, edgecolor=couleur,
                         facecolor=couleur + "22")
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x, y, texte, ha="center", va="center",
            fontsize=taille, fontweight=weight, color=couleur,
            fontfamily="DejaVu Serif", wrap=True,
            multialignment="center")

def fleche(ax, x1, y1, x2, y2, couleur=C_ARROW, style="-|>", lw=1.5):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=couleur,
                                lw=lw, connectionstyle="arc3,rad=0.0"))

def label_fleche(ax, x, y, texte, couleur=C_ARROW):
    ax.text(x, y, texte, ha="center", va="center",
            fontsize=7.5, color=couleur, style="italic",
            fontfamily="DejaVu Serif",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

# ── Titre ─────────────────────────────────────────────────────────────────────
ax.text(8, 9.6, "Figure 1 — Design empirique du modèle MCO",
        ha="center", va="center", fontsize=13, fontweight="bold",
        fontfamily="DejaVu Serif", color="#1F3864")
ax.text(8, 9.2, "Modèle de Mix Marketing (MMM) — E-Commerce & FMCG",
        ha="center", va="center", fontsize=9.5, fontfamily="DejaVu Serif",
        color="#555555", style="italic")

# ── Variable dépendante (centre droit) ────────────────────────────────────────
boite(ax, 11.5, 5.0, 2.8, 1.2,
      "Variable dépendante\n(D : Commandes / Volume\ndes ventes)",
      C_DEP, taille=8.5, bold=True)

# ── Variables marketing ────────────────────────────────────────────────────────
mark_labels = [
    "M : Google",
    "M : Meta",
    "M : Influenceur",
    "M : Indice de\ndépenses",
    "M : Pondéré\n(FMCG)",
]
ys_mark = [8.2, 7.0, 5.8, 4.6, 3.4]
for label, y in zip(mark_labels, ys_mark):
    boite(ax, 2.8, y, 2.6, 0.75, label, C_MARK, taille=8)
    fleche(ax, 4.1, y, 10.95, 5.0, couleur=C_MARK)

# ── Retards ────────────────────────────────────────────────────────────────────
retard_labels = ["M : Retard t−1\n(E-Commerce)", "M : Retard t−7\n(E-Commerce)",
                 "D : Retard t−1"]
ys_ret = [8.2, 7.3, 6.4]
for label, y in zip(retard_labels, ys_ret):
    boite(ax, 6.5, y, 2.4, 0.65, label, C_RETARD, taille=7.8)
    fleche(ax, 7.7, y, 10.95, 5.1, couleur=C_RETARD, lw=1.2)

# ── Chocs ──────────────────────────────────────────────────────────────────────
choc_labels = ["Choc : Taux de change", "Choc : Crise logistique\n(E-Commerce)",
               "Choc : Impact du\nséisme (FMCG)"]
ys_choc = [2.4, 1.5, 0.7]
for label, y in zip(choc_labels, ys_choc):
    boite(ax, 6.5, y, 2.8, 0.65, label, C_CHOC, taille=7.8)
    fleche(ax, 7.9, y, 10.95, 4.9, couleur=C_CHOC, lw=1.2)

# ── Effets fixes ───────────────────────────────────────────────────────────────
fix_labels = ["Facteur saisonnier", "Effet du dimanche\n/ Week-end"]
ys_fix = [3.2, 2.3]
for label, y in zip(fix_labels, ys_fix):
    boite(ax, 2.8, y, 2.5, 0.65, label, C_FIX, taille=7.8)
    fleche(ax, 4.05, y, 10.95, 4.95, couleur=C_FIX, lw=1.2)

# ── Variables de contrôle ──────────────────────────────────────────────────────
ctrl_labels = ["Dépenses des\nconcurrents", "Part de voix (%)"]
ys_ctrl = [1.4, 0.6]
for label, y in zip(ctrl_labels, ys_ctrl):
    boite(ax, 2.8, y, 2.5, 0.65, label, C_CTRL, taille=7.8)
    fleche(ax, 4.05, y, 10.95, 4.85, couleur=C_CTRL, lw=1.2)

# ── Terme d'erreur ─────────────────────────────────────────────────────────────
boite(ax, 11.5, 2.8, 2.2, 0.65, "ε : Terme d'erreur", C_ERR, taille=8)
fleche(ax, 11.5, 3.13, 11.5, 4.38, couleur=C_ERR, lw=1.2)

# ── Équation MCO ──────────────────────────────────────────────────────────────
eq_box = FancyBboxPatch((4.5, 4.5), 5.8, 1.0,
                        boxstyle="round,pad=0.1,rounding_size=0.2",
                        linewidth=1.5, edgecolor="#1F3864",
                        facecolor="#EBF0F8")
ax.add_patch(eq_box)
ax.text(7.4, 5.05,
        r"$D_t = \alpha + \sum_k \beta_k M_{k,t} + \sum_j \gamma_j F_{j,t} + \sum_m \delta_m S_{m,t} + \sum_l \lambda_l C_{l,t} + \varepsilon_t$",
        ha="center", va="center", fontsize=9.5, color="#1F3864",
        fontfamily="DejaVu Serif")
fleche(ax, 10.4, 5.05, 10.95, 5.05, couleur=C_DEP, lw=2.0)

# ── Légende ────────────────────────────────────────────────────────────────────
legend_items = [
    (C_MARK,  "Variables marketing (M :)"),
    (C_RETARD,"Variables de retard (t−k)"),
    (C_CHOC,  "Variables de choc (δ)"),
    (C_FIX,   "Effets fixes / Saisonnalité (γ)"),
    (C_CTRL,  "Variables de contrôle (λ)"),
    (C_DEP,   "Variable dépendante (D)"),
    (C_ERR,   "Terme d'erreur (ε)"),
]
patches = [mpatches.Patch(facecolor=c + "33", edgecolor=c, linewidth=1.2, label=l)
           for c, l in legend_items]
ax.legend(handles=patches, loc="lower center", ncol=4,
          bbox_to_anchor=(0.5, -0.04), fontsize=7.5,
          frameon=True, framealpha=0.9, edgecolor="#CCCCCC",
          prop={"family": "DejaVu Serif", "size": 7.5})

ax.text(8, 0.12,
        "Source : Auteur. MCO = Moindres Carrés Ordinaires. "
        "Spécification commune aux jeux de données E-Commerce et FMCG.",
        ha="center", va="center", fontsize=7.5, color="#777777",
        fontfamily="DejaVu Serif", style="italic")

plt.tight_layout(pad=0.5)
output_path = "Figure_04_Design_Empirique_Modele.png"
plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Fichier sauvegardé : {output_path}")
