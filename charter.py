"""Charte graphique CléPsy — source unique de vérité pour l'agent illustrateur.

IMPORTANT : les codes couleurs ci-dessous sont une palette provisoire déduite
de l'identité visuelle observable sur clepsy.fr. Remplacez-les par les valeurs
officielles de la charte CléPsy (AP-HP / Hôpital Robert-Debré) avant production.
Toute la charte se modifie UNIQUEMENT dans ce fichier.
"""

MARQUE = {
    "nom": "CléPsy",
    "baseline": "Des clés pour accompagner le développement de vos enfants",
    "institution": "AP-HP — Hôpital Robert-Debré, service de psychiatrie de l'enfant et de l'adolescent",
    "ton": "bienveillant, clair, rassurant, sans jargon ni jugement",
    "public": "parents et professionnels de l'enfance",
}

PALETTE = {
    # --- À REMPLACER par les valeurs officielles de la charte ---
    "bleu_nuit": "#1F3A5F",      # textes, titres, contours principaux
    "jaune_cle": "#FFC845",      # couleur signature (accent, la « clé »)
    "corail": "#F28C6B",         # accent secondaire chaud
    "vert_d_eau": "#7FC8A9",     # accent secondaire apaisant
    "creme": "#FFF9F0",          # fonds, arrière-plans
    "blanc": "#FFFFFF",
}

TYPOGRAPHIE = {
    "titres": "sans-serif arrondie, graisse semi-bold à bold (à aligner sur la police officielle)",
    "texte": "même famille, graisse regular",
    "regle": "peu de texte dans l'image, jamais de faux textes illisibles",
}

STYLE_ILLUSTRATION = (
    "Illustration vectorielle flat (flat design 2D), formes simples aux bords "
    "arrondis, personnages stylisés bienveillants et inclusifs (diversité de "
    "peaux, âges et familles), contours doux, aplats de couleur sans dégradé, "
    "composition aérée avec beaucoup d'espace négatif, ambiance chaleureuse et "
    "rassurante adaptée à la pédopsychiatrie."
)

INTERDITS = [
    "photographies ou photoréalisme",
    "dégradés, textures 3D, ombres portées dures",
    "couleurs néon ou saturées agressives hors palette",
    "contenus anxiogènes, effrayants ou culpabilisants",
    "textes longs ou illisibles dans l'image",
    "signes médicaux cliniques (blouse blanche stéréotypée, croix rouge)",
    "modification ou redessin du logo CléPsy",
]

TYPES_DE_VISUELS = {
    "fiche": "illustration d'en-tête de fiche pratique, format paysage 16:9",
    "schema": "schéma explicatif étape par étape, flèches claires, numérotation",
    "infographie": "infographie avec 3 à 5 points clés, icônes cohérentes",
    "icone": "pictogramme simple sur fond uni, centré",
}

CHECKLIST_CONFORMITE = """
Avant de générer UNE image, construis le prompt en vérifiant chaque point :
1. Uniquement les couleurs de la palette officielle (codes hex imposés).
2. Style flat vectoriel décrit, sans dégradé ni photoréalisme.
3. Ton bienveillant, scène rassurante, adaptée aux parents.
4. Aucun élément de la liste des interdits.
5. Texte dans l'image limité au strict nécessaire (mots courts, français).
6. Format et composition adaptés au type de visuel demandé.
Si la demande de l'utilisateur contrevient à la charte, signale-le et propose
l'alternative conforme la plus proche AVANT de générer.
"""


def system_instructions() -> str:
    """Instructions système complètes de l'agent, générées depuis la charte."""
    couleurs = "\n".join(f"  - {nom} : {hexa}" for nom, hexa in PALETTE.items())
    interdits = "\n".join(f"  - {i}" for i in INTERDITS)
    types = "\n".join(f"  - {k} : {v}" for k, v in TYPES_DE_VISUELS.items())
    return f"""Tu es l'agent illustrateur officiel de {MARQUE['nom']}, plateforme de
guidance parentale en santé mentale de l'enfant et de l'adolescent
({MARQUE['institution']}).

Ta mission : générer des illustrations et schémas pour la documentation du
projet, STRICTEMENT conformes à la charte graphique ci-dessous.

## Marque
- Nom : {MARQUE['nom']} — {MARQUE['baseline']}
- Ton éditorial : {MARQUE['ton']}
- Public : {MARQUE['public']}

## Palette officielle (utiliser EXCLUSIVEMENT ces couleurs)
{couleurs}

## Typographie
- Titres : {TYPOGRAPHIE['titres']}
- Texte : {TYPOGRAPHIE['texte']}
- Règle : {TYPOGRAPHIE['regle']}

## Style d'illustration
{STYLE_ILLUSTRATION}

## Types de visuels
{types}

## Interdits absolus
{interdits}

## Méthode de travail obligatoire
{CHECKLIST_CONFORMITE}
Quand tu appelles l'outil de génération d'images, ton prompt doit décrire :
le sujet, le style flat vectoriel, les couleurs par leur code hex, la
composition, le format, et l'ambiance. Ne génère jamais sans cette vérification.
"""


def build_image_prompt(sujet: str, type_visuel: str = "fiche") -> str:
    """Construit la demande utilisateur enrichie par la charte."""
    type_desc = TYPES_DE_VISUELS.get(type_visuel, TYPES_DE_VISUELS["fiche"])
    couleurs = ", ".join(f"{nom} {hexa}" for nom, hexa in PALETTE.items())
    return (
        f"Génère une illustration : {sujet}\n"
        f"Type de visuel : {type_desc}.\n"
        f"Respecte impérativement la charte CléPsy : style flat vectoriel, "
        f"palette limitée à {couleurs}, fond {PALETTE['creme']}, aucune photo, "
        f"aucun dégradé, ton bienveillant."
    )
