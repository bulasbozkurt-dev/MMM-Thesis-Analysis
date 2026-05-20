# MMM-Thesis-Analysis

**Galatasaray Üniversitesi — Endüstri Mühendisliği Bölümü**  
**Bitirme Projesi — Mayıs 2026**

---

## Titre du projet

**E-Ticaret ve Hızlı Tüketim Malları Sektörlerinde Pazarlama Yatırımlarının Tedarik Zinciri Performansına Etkisi**

*(Analyse de l'impact des investissements marketing sur la performance de la chaîne d'approvisionnement)*

---

## Auteurs

- Berke Ulaş Bozkurt  
- Uğur Özdoğan  

**Danışmanlar :** Dr. Öğr. Üyesi Esin Mukul Taylan — Dr. Öğr. Üyesi Nazlı Göker Mutlu

---

## Description

Ce dépôt contient l'ensemble des codes Python utilisés pour produire les tableaux, figures et analyses du projet de fin d'études. L'étude analyse les associations entre les investissements marketing, la demande et la performance de la chaîne d'approvisionnement dans deux secteurs distincts : **e-commerce** et **FMCG**.

La méthode d'estimation retenue est la régression linéaire par **Moindres Carrés Ordinaires (MCO)**, inspirée conceptuellement de la logique du **Media Mix Modeling (MMM)**.

---

## Structure du dépôt

```
MMM-Thesis-Analysis/
│
├── données/
│   ├── E-Ticaret_MMM_v2.xlsx        ← Jeu de données e-commerce (quotidien, 1086 obs.)
│   └── FMCG_MMM_v2.xlsx             ← Jeu de données FMCG (hebdomadaire, 1248 obs.)
│
├── chapitre_4_modelisation/         ← Analyse exploratoire + spécification MCO
│   ├── sortie_01_resume_datasets.py          ← Tableau 4.1 — Résumé des jeux de données
│   ├── sortie_02_valeurs_manquantes.py       ← Tableau 4.2/4.3/4.4 — Valeurs manquantes
│   ├── sortie_03_correspondance_variables.py ← Tableau 4.5 — Structure des variables
│   ├── sortie_04_evolution_marketing.py      ← Figure 4.1 — Évolution marketing et demande
│   ├── sortie_05_distribution_demande.py     ← Figure 4.2 — Distribution de la variabilité
│   ├── sortie_06_profil_saisonnier.py        ← Figure 4.3 — Profil saisonnier
│   ├── sortie_07_composition_marketing.py    ← Figure 4.4 — Composition des dépenses
│   └── sortie_08_design_empirique.py         ← Figure 4.5 — Structure empirique du modèle MCO
│
├── chapitre_5_application/          ← Résultats MCO + interprétation
│   ├── sortie_01_resultats_mco.py            ← Tableau 5.1/5.2 — Résultats MCO complets
│   ├── sortie_02_matrice_correlation.py      ← Tableau 5.3/5.4 — Matrices de corrélation
│   ├── sortie_03_coefficients_marketing.py   ← Figure 5.1 — Coefficients des variables marketing
│   ├── sortie_04_observees_ajustees.py       ← Figure 5.2 — Valeurs observées vs ajustées
│   ├── sortie_05_impact_chocs.py             ← Figure 5.3 — Impact des chocs exogènes
│   └── sortie_06_comparaison_ec_fmcg.py      ← Tableau 5.5 — Comparaison E-Commerce vs FMCG
│
└── appendices/                      ← Analyses complémentaires
    ├── appendice_01_residus_ec.py            ← Diagnostics des résidus MCO — E-Commerce
    ├── appendice_02_residus_fg.py            ← Diagnostics des résidus MCO — FMCG
    ├── appendice_03_demande_region.py        ← Demande par région (FMCG)
    ├── appendice_04_part_marche_region.py    ← Part de marché par région (FMCG)
    └── appendice_05_variantes_modeles.py     ← Comparaison des variantes MCO
```

---

## Résultats principaux

| Indicateur | E-Commerce | FMCG |
|---|---|---|
| R² | 0.7679 | 0.8124 |
| R² ajusté | 0.7649 | 0.8102 |
| Statistique F | 257.272 | 362.311 |
| Durbin-Watson | 2.036 | 2.522 |
| N observations | 1025 | 1186 |

---

## Spécification du modèle MCO

```
D_it = α + Σ β_k M_kit + Σ θ_l M_i,t-l + Σ γ_j F_jt + Σ δ_m S_mt + Σ λ_n C_nt + ε_it
```

| Composante | Description |
|---|---|
| D_it | Variable dépendante : commandes (e-commerce) / volume des ventes (FMCG) |
| M_kit | Variables marketing contemporaines |
| M_i,t-l | Variables marketing retardées |
| F_jt | Effets fixes et saisonniers |
| S_mt | Variables de choc exogènes |
| C_nt | Variables de contrôle |
| ε_it | Terme d'erreur |

---

## Prérequis

```python
pip install pandas numpy matplotlib scipy statsmodels openpyxl
```

Ou sous Google Colab (recommandé) : `statsmodels` est déjà installé.

---

## Comment utiliser ce dépôt

**Option 1 — Google Colab (recommandé)**

1. Ouvrir [Google Colab](https://colab.research.google.com)
2. Importer les deux fichiers Excel depuis le dossier `données/`
3. Copier-coller le code de chaque fichier `.py` dans une cellule
4. Exécuter

**Option 2 — Environnement local**

```bash
git clone https://github.com/bulasbozkurt-dev/MMM-Thesis-Analysis.git
cd MMM-Thesis-Analysis
pip install pandas numpy matplotlib scipy statsmodels openpyxl
python chapitre_4_modelisation/sortie_01_resume_datasets.py
```

---

## Note sur les données

Les jeux de données utilisés dans cette étude sont des **séries temporelles synthétiques**. Ils ne correspondent pas à des données internes réelles d'entreprises spécifiques. Ils ont été construits à partir d'ordres de grandeur sectoriels, de paramètres réalistes et de relations économiques plausibles, dans le cadre du projet de fin d'études.

---

## Terminologie

| Abréviation | Signification |
|---|---|
| MCO | Moindres Carrés Ordinaires |
| MMM | Media Mix Modeling |
| FMCG | Fast-Moving Consumer Goods |
| VIF | Facteur d'inflation de la variance |
| DW | Durbin-Watson |
| IC 95% | Intervalle de confiance à 95% |
| OOS | Out-of-stock / Rupture de stock |

---

*Galatasaray Üniversitesi — Mühendislik ve Teknoloji Fakültesi — Endüstri Mühendisliği Bölümü — Mayıs 2026*
