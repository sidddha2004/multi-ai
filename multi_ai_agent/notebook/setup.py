import os
import sys
import pathlib

from dotenv import load_dotenv

NOTEBOOKS_DIR = pathlib.Path(__file__).parent
REPO_ROOT = NOTEBOOKS_DIR.parent
DJANGO_PROJECT_ROOT = REPO_ROOT

DJANGO_SETTINGS_MODULE = "multi_ai_agent.settings"


def init(verbose=True):
    os.chdir(DJANGO_PROJECT_ROOT)
    sys.path.insert(0, str(DJANGO_PROJECT_ROOT))

    if verbose:
        print("Working directory:", DJANGO_PROJECT_ROOT)

    load_dotenv(DJANGO_PROJECT_ROOT / ".env")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    import django
    django.setup()

    if verbose:
        print("Django initialized successfully")