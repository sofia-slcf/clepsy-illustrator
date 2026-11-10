# CléPsy Illustrator — agent de génération d'illustrations

Agent Mistral qui génère illustrations et schémas pour la documentation CléPsy
(AP-HP — Hôpital Robert-Debré), en respectant strictement la charte graphique.

## Installation

```bash
pip install -r requirements.txt
export MISTRAL_API_KEY="votre-clé"
```

## Utilisation

```bash
python main.py "Le rituel du coucher en 4 étapes" --type schema
python main.py "Reconnaître les signes d'anxiété chez l'enfant" --type infographie
python main.py "Pictogramme sommeil" --type icone --out images/
```

Types de visuels : `fiche` (en-tête 16:9), `schema`, `infographie`, `icone`.

## Personnaliser la charte

Toute la charte vit dans **`charter.py`** : palette (codes hex), style
d'illustration, typographie, interdits, types de visuels. Modifiez ce seul
fichier — les instructions de l'agent sont régénérées automatiquement.

> ⚠️ La palette actuelle est **provisoire** (déduite de l'identité visible sur
> clepsy.fr). Remplacez les codes hex par ceux de la charte officielle CléPsy.

## Fonctionnement

1. `charter.py` génère les instructions système de l'agent (checklist de
   conformité imposée avant chaque génération).
2. L'agent est créé via l'API Agents avec l'outil intégré `image_generation`
   (modèles Black Forest Labs).
3. Les images générées sont téléchargées depuis l'API Files et enregistrées
   dans le dossier de sortie.

## Limites connues

- La génération d'images ne garantit pas au pixel près les codes hex : pour
  les visuels exigeant une conformité stricte (logo, couleurs exactes),
  préférez un post-traitement (re-colorisation des aplats) ou des gabarits
  SVG générés par code.
- L'API `client.beta.agents` (Agents & Conversations) est la voie documentée
  pour l'outil `image_generation` ; elle évolue, consultez
  https://docs.mistral.ai/studio/agents/agent-tools/image_generation
