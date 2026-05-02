# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

`ci-cd-demo` is a deliberately tiny Vue 3 + FastAPI + Nginx app whose real goal is the **CI/CD pipeline around it**: local dev → CI checks → image build → GHCR push → SSH deploy → health probe. Treat the application code as scaffolding; the workflows, Dockerfiles, and compose files are the product.

## Critical environment constraint

The primary dev machine is **Windows 11 without Docker installed**. Do NOT instruct the user to run `docker`, `docker compose`, or `docker build` locally unless they have explicitly said Docker is available. Container build/run validation happens in one of:

- An Ubuntu VM Docker Host
- GitHub Actions
- The production server

When you write a verification step that uses Docker, label which environment it runs in.

## Common commands

Backend (run inside `backend/`, requires `uv`):
- `uv sync --frozen --no-dev` — install deps
- `uv run uvicorn app.main:app --reload` — run dev server on `:8000`
- `uv run python -c "from app.main import app; print(app.title)"` — the same import smoke check CI performs

Frontend (run inside `frontend/`, requires Node 22):
- `npm ci` — install
- `npm run dev` — Vite dev server on `:5173`
- `npm run build` — `vue-tsc -b && vite build` (this is the CI gate)

Docker Host validation (NOT for Win11 dev machine):
- `docker compose up --build` — full stack on `http://127.0.0.1:8080`
- `docker compose -f compose.prod.yml pull && docker compose -f compose.prod.yml up -d` — production-style run using GHCR images

Health checks (against either compose):
- `curl http://127.0.0.1:8080/health` → `{"status":"ok"}`
- `curl http://127.0.0.1:8080/api/hello` → `{"message":"hello from backend"}`

## Architecture: how the request flows

There is one public entry point (`:8080`, served by the frontend container's Nginx) and one backend container reachable only on the internal compose network:

1. Browser hits `http://host:8080/` → frontend container's Nginx serves the built Vue SPA from `/usr/share/nginx/html`.
2. SPA calls relative paths (`fetch("/api/hello")`) — no CORS in production because everything is same-origin.
3. Nginx routes `/api/` and `/health` to `http://backend:8000` (the compose service name).
4. FastAPI (`backend/app/main.py`) returns Pydantic-modeled JSON.

The Nginx config lives at `nginx/nginx.conf` and is **bind-mounted into the frontend container at runtime** in both `docker-compose.yml` and `compose.prod.yml`. It is not baked into the image. Editing `nginx.conf` requires a container restart but no rebuild.

CORS middleware in `backend/app/main.py` only whitelists `localhost:5173` for the Vite dev workflow; in containers the SPA is same-origin via Nginx and CORS does not apply.

## Two compose files, by design

- `docker-compose.yml` — Docker Host validation. Both services use `build:`. Source-of-truth for "does the code build and run."
- `compose.prod.yml` — Server deployment. Both services use `image:` pointing at GHCR (`ghcr.io/mrzhang7777777/ci-cd-demo-{backend,frontend}:latest`). **The server never builds**; it only `pull`s and `up -d`s. Do not add `build:` here.

## CI/CD workflows (`.github/workflows/`)

- `ci-backend.yml` — on push/PR to main: `uv sync` + import the FastAPI app.
- `ci-frontend.yml` — on push/PR to main: `npm ci` + `npm run build`.
- `docker-release.yml` — on push to main: matrix-builds backend and frontend images, pushes to GHCR with both `:latest` and `:sha-<short>` tags. **Image names must be all lowercase** — GHCR rejected uppercase owners (`MrZhang...`); the namespace is hardcoded as `mrzhang7777777`.
- `deploy-production.yml` — runs after `docker-release` succeeds (or via `workflow_dispatch`). SSHes to the server using `appleboy/ssh-action`, then `cd $DEPLOY_PATH && git pull && docker compose -f compose.prod.yml pull && up -d` and curls `/health` + `/api/hello`. Required secrets: `SERVER_HOST`, `SERVER_USER`, `SERVER_PORT`, `SERVER_SSH_KEY`, `DEPLOY_PATH`.

## Documentation-first workflow (from AGENTS.md)

This repo enforces "docs before code" for anything structural. Before changing any of the following, update the relevant doc in `docs/ai/` first:

- Directory layout
- API contract (`docs/ai/API_SPEC.md`)
- Image build approach
- GitHub Actions flow (`docs/ai/CI_CD_PLAN.md`)
- Deployment approach (`docs/ai/DEPLOYMENT.md`)
- Environment variable names

When docs conflict, the priority order is:
1. `docs/ai/DECISIONS.md`
2. `docs/ai/ARCHITECTURE.md`
3. `docs/ai/API_SPEC.md`
4. `docs/ai/DEPLOYMENT.md`
5. `docs/ai/CI_CD_PLAN.md`
6. `docs/ai/TASKS.md`
7. `README.md`

## Scope guardrails

The target server is a 2-core / 2 GB cloud VM. Keep things small:

- No Kubernetes, no auth/DB/cache layer, no heavy observability stack — none are planned.
- No "server pulls source and builds" pattern. The server only consumes prebuilt GHCR images.
- Don't add dependencies not declared in `docs/ai/TECH_STACK.md` without a doc update first.
- One task per commit; tasks are tracked in `docs/ai/TASKS.md` (T010–T016 are the current sequence; T016 = automated SSH deploy is the active focus per `readme1.md`).
