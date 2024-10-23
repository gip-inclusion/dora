import os
import random
from pathlib import Path

random.seed()

# Racine du projet Django
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Contrairement aux environements de production et staging,
# les environnement de développement et de test se basent sur les fichiers
# de configuration contenus dans le répertoire 'envs'.
# Dans ce cas, l'environnement est nécessairement local
if os.path.isdir(BASE_DIR / "envs"):
    import environ

    environ.Env.read_env(os.path.join(BASE_DIR / "envs", "dev.env"))
    environ.Env.read_env(os.path.join(BASE_DIR / "envs", "secrets.env"))
