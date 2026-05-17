"""
Figure 7.2 - Matrice qualitative des contraintes realistes prises en compte

Genere une matrice qualitative croisant six familles de contraintes
(economiques, operationnelles, methodologiques, ethiques, durabilite,
organisationnelles) avec quatre dimensions d'analyse (identification,
integration, limite liee aux donnees, perspective future).

Sorties :
    - figure_7_2_matrice_contraintes.pdf
    - figure_7_2_matrice_contraintes.png

Dependances :
    - matplotlib

Utilisation :
    python figure_7_2_matrice_contraintes.py
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = "chapter7_figures_advanced"
FIG_BASENAME = "figure_7_2_matrice_contraintes"

ROWS = [
    "Economiques",
    "Operationnelles",
    "Methodologiques",
    "Ethiques et confidentialite",
    "Durabilite",
    "Organisationnelles",
]

COLS = [
    "Identification",
    "Integration",
    "Limite liee aux donnees",
    "Perspective future",
]

VALUES = [
    ["Fort",  "Fort",  "Moyen",  "Moyen"],
    ["Fort",  "Fort",  "Moyen",  "Fort"],
    ["Fort",  "Fort",  "Fort",   "Fort"],
    ["Fort",  "Fort",  "Faible", "Moyen"],
    ["Moyen", "Moyen", "Moyen",  "Fort"],
    ["Moyen", "Moyen", "Moyen",  "Moyen"],
]

COLOR_MAP = {
    "Fort":   "#B7D7A8",
    "Moyen":  "#F6E3A1",
    "Faible": "#E6B8AF",
}


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def add_cell(ax, x, y, w, h, text, facecolor,
             fontsize=12, fontweight="bold", linewidth=1.0):
    """Ajoute une cellule rectangulaire contenant du texte centre."""
    ax.add_patch(
        Rectangle(
            (x, y), w, h,
            facecolor=facecolor,
            edgecolor="black",
            linewidth=linewidth,
        )
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=fontweight,
        wrap=True,
    )


# ---------------------------------------------------------------------------
# Construction de la figure
# ---------------------------------------------------------------------------

def build_figure():
    """Construit et retourne la figure matplotlib."""
    fig, ax = plt.subplots(figsize=(16, 8.5))
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.8, 7.3)
    ax.axis("off")

    # Titre
    ax.text(
        2.5, 7.05,
        "Matrice qualitative des contraintes realistes prises en compte",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
    )

    # Largeurs de colonnes
    col_widths = [1.25, 0.9, 0.9, 1.15, 0.9]
    x_positions = [0]
    for w in col_widths[:-1]:
        x_positions.append(x_positions[-1] + w)

    headers = ["Contrainte"] + COLS

    # Ligne d'en-tete
    for j, header in enumerate(headers):
        add_cell(
            ax,
            x_positions[j], 6,
            col_widths[j], 0.8,
            header,
            facecolor="#D9EAF7",
            fontsize=11,
            linewidth=1.2,
        )

    # Corps du tableau
    for i, row in enumerate(ROWS):
        y = 5 - i

        # Libelle de ligne
        add_cell(
            ax,
            x_positions[0], y,
            col_widths[0], 1,
            row,
            facecolor="#F2F2F2",
            fontsize=11,
        )

        # Cellules de valeurs
        for j, value in enumerate(VALUES[i]):
            add_cell(
                ax,
                x_positions[j + 1], y,
                col_widths[j + 1], 1,
                value,
                facecolor=COLOR_MAP[value],
                fontsize=12,
            )

    # Legende
    legend_y = -0.20
    ax.text(
        0, legend_y,
        "Lecture qualitative :",
        ha="left",
        va="center",
        fontsize=11,
        fontweight="bold",
    )

    legend_items = [
        ("Fort",   COLOR_MAP["Fort"]),
        ("Moyen",  COLOR_MAP["Moyen"]),
        ("Faible", COLOR_MAP["Faible"]),
    ]

    for k, (label, color) in enumerate(legend_items):
        x = 1.35 + k * 0.85
        ax.add_patch(
            Rectangle(
                (x, legend_y - 0.12),
                0.22, 0.22,
                facecolor=color,
                edgecolor="black",
                linewidth=0.8,
            )
        )
        ax.text(
            x + 0.30,
            legend_y,
            label,
            ha="left",
            va="center",
            fontsize=10.5,
        )

    # Note
    ax.text(
        0, -0.55,
        "Note : cette matrice constitue une synthese qualitative "
        "et n'introduit aucun nouveau resultat statistique.",
        ha="left",
        va="center",
        fontsize=10,
    )

    plt.tight_layout(pad=0.5)
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
