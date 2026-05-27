# Evida2.0

Evida2.0 er organisert som et ryddig monorepo direkte fra prosjektroten.

## Struktur

- `apps/web` - webflate og saksrom
- `services/api` - FastAPI for saker, dokumenter, kilder, audit, export gate og assistant
- `services/worker` - dokumentpipeline, OCR/mock, chunking og hashing
- `packages/*` - delte kontrakter og hjelpepakker
- `infra` - lokal database/queue/storage og migrasjoner
- `tests` - kontrakt- og assistant golden-tester
- `docs/specs` - produkt-, design-, teknisk-, QA- og leveransedokumentasjon
- `scripts` - start, smoke-build og kontrollscripts

## Start programmet

Dobbeltklikk:

```text
Start_Advokat_AI.bat
```

Startfilen kjører alltid fra denne repo-roten. Hvis repoet er koblet til git, prøver den å hente siste kode før den starter lokale dev-servere.

## Verifisering

```bash
npm run verify
```

Dette kjører:

- UI-copy check
- backend- og worker-tester
- kontrakttester
- assistant golden-tester
- web smoke-build

## API

Lokal API-server:

```bash
cd services/api
python -m uvicorn advokat_ai.main:app --host 127.0.0.1 --port 8000 --reload
```

Health:

```text
http://127.0.0.1:8000/health
```
