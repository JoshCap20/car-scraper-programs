"""Load environment variables from a .env file or the process' environment."""

import os
import dotenv

# Load envirnment variables from .env file upon module start.
dotenv.load_dotenv(f"{os.path.dirname(__file__)}/.env", verbose=True)


def getenv(variable: str, default: str = None) -> str:
    value = os.getenv(variable)
    if value is not None:
        return value
    elif default is not None:
        return default
    else:
        raise NameError(f"Error: {variable} Environment Variable not Defined")
