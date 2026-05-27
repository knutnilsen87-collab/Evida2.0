# Advokat AI — Provider Interfaces v1

## Purpose

Provider-specific code must not leak through the application.

AI, OCR, storage, auth and email integrations must be behind interfaces so Codex can implement mock/local providers first and production providers later.

---

# 1. AI provider interface

```python
class AIProvider(Protocol):
    async def generate_structured(
        self,
        *,
        task: str,
        context: dict,
        response_schema: dict,
        safety_policy: dict,
        timeout_seconds: int,
    ) -> dict:
        ...
```

Implementations:
- `MockAIProvider` for tests/local
- `ConfiguredAIProvider` placeholder using environment variables
- production provider adapter later

Rules:
- no direct AI calls from frontend
- no provider keys in code
- no customer data used for training by default
- provider failures must return deterministic fallback where possible

---

# 2. OCR provider interface

```python
class OCRProvider(Protocol):
    async def extract_text(
        self,
        *,
        document_id: str,
        page_number: int,
        page_image_uri: str,
        language_hint: str | None = "no",
    ) -> OCRResult:
        ...
```

`OCRResult`:
- text
- confidence
- warnings
- bounding_boxes optional
- provider_metadata

Implementations:
- `MockOCRProvider`
- `LocalOCRProvider` optional
- `ConfiguredOCRProvider`

---

# 3. Storage provider interface

```python
class ObjectStorage(Protocol):
    async def create_upload_url(...)
    async def put_object(...)
    async def get_object(...)
    async def create_download_url(...)
    async def object_exists(...)
```

Local:
- MinIO or filesystem emulator

Production:
- EU/EEA S3-compatible storage

---

# 4. Auth provider interface

```python
class AuthProvider(Protocol):
    async def get_current_user(token: str) -> AuthenticatedUser:
        ...
```

Local:
- dev token provider

Production:
- OIDC provider

---

# 5. Virus/malware scan interface

```python
class MalwareScanner(Protocol):
    async def scan_object(storage_uri: str) -> ScanResult:
        ...
```

Local:
- mock pass scanner

Production:
- configured scanner

---

# 6. Legal source connector interface

Manual `LegalSource` is required first.

External connectors optional behind:

```python
class LegalSourceProvider(Protocol):
    async def search(...)
    async def fetch(...)
    async def verify_reference(...)
```

No external legal source connector is required for Pilot Candidate unless owner provides provider details.

---

# 7. Provider configuration

Environment variables:

```env
AI_PROVIDER=mock
OCR_PROVIDER=mock
STORAGE_PROVIDER=minio
AUTH_PROVIDER=local
MALWARE_SCANNER=mock
DATA_REGION=EU
CUSTOMER_DATA_TRAINING_ALLOWED=false
```

---

# 8. Provider audit

Provider calls involving case data must produce audit or observability records:
- provider type
- operation
- case_id
- user_id if applicable
- success/failure
- latency
- no full sensitive payload in logs by default
