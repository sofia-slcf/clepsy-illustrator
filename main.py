"""Agent illustrateur CléPsy — génère des images conformes à la charte graphique.

Usage :
    export MISTRAL_API_KEY="..."
    python main.py "Le rituel du coucher en 4 étapes" --type schema
    python main.py "Un enfant qui range ses écrans" --type fiche --out images/

Types disponibles : fiche, schema, infographie, icone
"""

import argparse
import asyncio
import os
import sys

from mistralai import Mistral
from mistralai.client.models import ToolFileChunk

from charter import build_image_prompt, system_instructions

MODEL = "mistral-medium-latest"
AGENT_NAME = "CléPsy Illustrator"


async def generer(sujet: str, type_visuel: str, dossier_sortie: str) -> list[str]:
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    agent = client.beta.agents.create(
        model=MODEL,
        name=AGENT_NAME,
        description=(
            "Agent de génération d'illustrations pour la documentation CléPsy, "
            "strictement conforme à la charte graphique."
        ),
        instructions=system_instructions(),
        tools=[{"type": "image_generation"}],
        completion_args={"temperature": 0.3, "top_p": 0.95},
    )

    response = client.beta.conversations.start(
        agent_id=agent.id,
        inputs=build_image_prompt(sujet, type_visuel),
    )

    fichiers: list[str] = []
    os.makedirs(dossier_sortie, exist_ok=True)
    for i, chunk in enumerate(response.outputs[-1].content):
        if isinstance(chunk, ToolFileChunk):
            donnees = client.files.download(file_id=chunk.file_id).read()
            chemin = os.path.join(
                dossier_sortie,
                f"clepsy_{type_visuel}_{i}_{chunk.file_id[:8]}.{chunk.file_type}",
            )
            with open(chemin, "wb") as f:
                f.write(donnees)
            fichiers.append(chemin)
            print(f"Image enregistrée : {chemin}")

    if not fichiers:
        print("Aucune image générée. Réponse de l'agent :")
        print(response.outputs[-1].content)
    return fichiers


def main() -> int:
    parser = argparse.ArgumentParser(description="Illustrations CléPsy conformes à la charte")
    parser.add_argument("sujet", help="Sujet de l'illustration (en français)")
    parser.add_argument(
        "--type",
        dest="type_visuel",
        default="fiche",
        choices=["fiche", "schema", "infographie", "icone"],
        help="Type de visuel (défaut : fiche)",
    )
    parser.add_argument("--out", default="images", help="Dossier de sortie (défaut : images/)")
    args = parser.parse_args()

    if not os.environ.get("MISTRAL_API_KEY"):
        print("Erreur : définissez MISTRAL_API_KEY.", file=sys.stderr)
        return 1

    asyncio.run(generer(args.sujet, args.type_visuel, args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
