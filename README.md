# Izitax Developer — Bot de Teams

Bot genérico de Microsoft Teams que responde **"hola"** a cualquier mensaje.
Sin IA. Construido con el SDK oficial [microsoft/teams.py](https://github.com/microsoft/teams.py).

## Requisitos

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/)
- [devtunnel CLI](https://aka.ms/devtunnel) (para exponer el bot a Teams)

## Configuración

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

```env
TEAMS_CLIENT_SECRET=<your-client-secret>
TEAMS_CLIENT_ID=<your-client-id>
TEAMS_TENANT_ID=<your-tenant-id>
teamsAppId=<your-teams-app-id>
endpoint=https://<your-devtunnel-subdomain>.use.devtunnels.ms/api/messages
```

> `.env` está en `.gitignore` — nunca lo commitees con credenciales reales.

## Ejecutar

```bash
uv sync
uv run python main.py
```

El bot escucha en `http://0.0.0.0:3978` y sirve el endpoint de Bot Framework en
`/api/messages`.

## Exponer a Teams con devtunnel

Teams necesita una URL pública que reenvíe al puerto local `3978`:

```bash
devtunnel user login
devtunnel create teams-bot --allow-anonymous
devtunnel port create teams-bot -p 3978
devtunnel host teams-bot
```

Esto imprime la URL pública (p. ej. `https://<your-subdomain>-3978.use.devtunnels.ms`).
El *messaging endpoint* del bot es esa URL **+ `/api/messages`**.

---

## Para compartir con el dueño de la organización

El developer no administra el registro del bot/app en el tenant. Para que Teams
enrute los mensajes a este bot, el **dueño de la org** debe apuntar el
*messaging endpoint* a la URL pública del devtunnel.

> **Endpoint a configurar (URL completa, con `/api/messages`):**
> ```
> https://<your-subdomain>-3978.use.devtunnels.ms/api/messages
> ```

### Opción A — Actualizar el bot existente (recomendado)

Mantiene el mismo `client_id`/secret; no hay que reinstalar la app en Teams.

```bash
npm install -g @microsoft/teams.cli@preview
teams login

teams app update <your-teams-app-id> \
  --endpoint "https://<your-subdomain>-3978.use.devtunnels.ms/api/messages" -y
```

### Opción B — Crear un bot nuevo

Genera un nuevo `client_id`/secret (hay que actualizar el `.env` y reinstalar la
app en Teams).

```bash
npm install -g @microsoft/teams.cli@preview
teams login

teams app create \
  --name "Izitax Developer" \
  --endpoint "https://<your-subdomain>-3978.use.devtunnels.ms/api/messages"
```

> ⚠️ La URL del devtunnel debe terminar en **`/api/messages`**. Sin esa ruta,
> Teams hace POST a `/` y obtiene `404` (el bot nunca responde).
