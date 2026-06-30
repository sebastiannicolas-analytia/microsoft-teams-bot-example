"""
Bot genérico de Microsoft Teams.

Responde "hola" a cualquier mensaje. No usa ninguna IA.
Construido con el SDK oficial https://github.com/microsoft/teams.py
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from microsoft_teams.api import MessageActivity
from microsoft_teams.apps import ActivityContext, App

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# El .env usa el prefijo TEAMS_, así que pasamos las credenciales explícitamente.
app = App(
    client_id=os.getenv("TEAMS_CLIENT_ID"),
    client_secret=os.getenv("TEAMS_CLIENT_SECRET"),
    tenant_id=os.getenv("TEAMS_TENANT_ID"),
)


@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]) -> None:
    """Responde 'hola' a cualquier mensaje entrante."""
    logger.info("Mensaje recibido: %s", ctx.activity.text)
    await ctx.reply("hola")


if __name__ == "__main__":
    asyncio.run(app.start())
