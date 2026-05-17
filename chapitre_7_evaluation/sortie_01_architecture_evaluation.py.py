"""
Figure 7.1 - Architecture de l'evaluation generale du projet

Genere une figure recapitulative presentant les cinq dimensions
d'evaluation du projet autour d'un noeud central.

Sorties :
    - figure_7_1_architecture_evaluation.pdf
    - figure_7_1_architecture_evaluation.png

Dependances :
    - matplotlib

Utilisation :
    python figure_7_1_architecture_evaluation.py
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = "chapter7_figures_advanced"
FIG_BASENAME = "figure_7_1_architecture_evaluation"


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def add_box(ax, x, y, w, h, title, desc, title_size=10.5, desc_size=8.2):
    """Ajoute une boite arrondie avec un titre et une description."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08,rounding_size=0.04",
        linewidth=1.2,
        edgecolor="black",
        facecolor="white",
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h * 0.63,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
    )
    ax.text(
        x + w / 2,
        y + h * 0.33,
        desc,
        ha="center",
        va="center",
        fontsize=desc_size,
    )


def add_arrow(ax, start, end):
    """Ajoute une fleche entre deux points."""
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="->",
        mutation_scale=12,
        linewidth=1.1,
        color="black",
        shrinkA=4,
        shrinkB=4,
    )
    ax.add_patch(arrow)


# ---------------------------------------------------------------------------
# Construction de la figure
# ---------------------------------------------------------------------------

def build_figure():
    """Construit et retourne la figure matplotlib."""
    fig, ax = plt.subplots(figsize=(13.5, 7.2))
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    # Titre
    ax.text(
        6.75,
        6.65,
        "Architecture de l'evaluation generale du projet",
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold",
    )

    # Dimensions des boites
    w_top, h_top = 3.15, 1.00
    w_bottom, h_bottom = 3.35, 1.05
    w_center, h_center = 2.85, 0.95

    # Boites superieures
    add_box(
        ax, 0.70, 5.25, w_top, h_top,
        "Objectifs initiaux",
        "Adequation entre\nproblematique, perimetre\net objectifs du projet",
    )
    add_box(
        ax, 5.15, 5.50, w_top, h_top,
        "Deroulement du projet",
        "Progression academique,\nconstruction methodologique\net coherence du travail",
    )
    add_box(
        ax, 9.60, 5.25, w_top, h_top,
        "Contraintes realistes",
        "Donnees, confidentialite,\nfaisabilite et limites\nmethodologiques",
    )

    # Boite centrale
    add_box(
        ax, 5.35, 3.35, w_center, h_center,
        "Evaluation generale\ndu projet",
        "",
        title_size=11,
        desc_size=8,
    )

    # Boites inferieures
    add_box(
        ax, 1.65, 1.30, w_bottom, h_bottom,
        "Apports en genie industriel",
        "Vision systemique,\nperformance et aide\na la decision",
    )
    add_box(
        ax, 8.55, 1.30, w_bottom, h_bottom,
        "Portee et impact potentiel",
        "Contribution scientifique,\ntechnologique et\nsocio-economique",
    )

    # Fleches vers la boite centrale
    add_arrow(ax, (3.85, 5.55), (5.35, 4.00))
    add_arrow(ax, (6.75, 5.50), (6.75, 4.30))
    add_arrow(ax, (9.60, 5.55), (8.20, 4.00))
    add_arrow(ax, (4.95, 1.85), (5.75, 3.35))
    add_arrow(ax, (8.55, 1.85), (7.80, 3.35))

    plt.tight_layout(pad=0.4)
    return fig


# ---------------------------------------------------------------------------
# Point d'entree
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fig = build_figure()

    pdf_path = os.path.join(OUTPUT_DIR, f"{FIG_BASENAME}.pdf")
    png_path = os.path.join(OUTPUT_DIR, f"{FIG_BASENAME}.png")

    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved PDF: {pdf_path}")
    print(f"Saved PNG: {png_path}")


if __name__ == "__main__":
    main()
