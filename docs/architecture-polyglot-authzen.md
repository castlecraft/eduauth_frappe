# Architecture Specification: Polyglot AuthZEN via Frappe Control Plane & Topaz PDP

## Overview

In an institutional polyglot environment, satellite microservices (FastAPI, Go, Spring Boot, Node.js) frequently spawn alongside the central Frappe instance. 

To prevent junior developer churn and avoid bottlenecking core Frappe maintainers:
1. **Frappe** serves as the **Authoring & Validation Control Plane**:
   - Manages and syncs core organizational entities (`department`, `committee`, `institution`, `user`).
   - Registers external resource DDL schemas and stitches the unified Topaz `manifest.yaml`.
   - Exposes a strict, validated REST API for satellite apps to assign relations without polluting Frappe's database with external instance rows.
2. **Topaz** serves as the **High-Performance PDP (Policy Decision Point)**:
   - Stores all validated graph edges.
   - Evaluates sub-millisecond authorization queries directly for satellite app runtimes.

```
                         ┌──────────────────────────────────────────────┐
                         │             FRAPPE CONTROL PLANE             │
                         │                                              │
                         │  1. Author & Sync Core DDL (Manifest)        │
                         │  2. Author & Sync Core Entities (Depts, etc) │
                         │  3. Whitelisted Validation API for Satellite │
                         │     Relation Assignments                     │
                         └──────────────────────┬───────────────────────┘
                                                │ Validated Tuples / Manifest
                                                ▼
┌──────────────────────────────────────┐  ┌───────────┐
│       SATELLITE APP / JUNIOR DEV     │  │   TOPAZ   │
│     (FastAPI / Go / Spring Boot)     │  │    PDP    │
│                                      │  │           │
│  - Reads Core Entities from Shell/API│  │           │
│  - Calls Frappe to ASSIGN Relation   ├──┴───────────┤
│  - Calls Topaz DIRECTLY for          │              │
│    `is_allowed` (Check) ────────────▶│  Fast Check  │
└──────────────────────────────────────┘  └───────────┘
```

---

## 🏛️ System Architecture: Frappe Control Plane (`topaz_frappe`)

### 1. Resource & Relation DDL Registration via `Topaz External Resource` DocType
- **DocType `Topaz External Resource`**
  - Standardized administrative DocType in `topaz_frappe` serving as the single source of truth for all external satellite resources:
    - `resource_type` (Select, Unique, e.g. `candidate`, `expense_claim`, `book_reservation`): Base shipped as empty Select or placeholder; consuming apps populate options via `Property Setter` fixtures.
    - `service_name` (Select, e.g. `recruitment-fastapi`, `finance-springboot`): Consuming apps populate options via `Property Setter` fixtures.
    - `owner_team` (Select, e.g. `HR Tech`, `Finance`, `Student Affairs`): Consuming apps populate options via `Property Setter` fixtures.
    - `manifest_fragment` (Code, language `yaml`): The Topaz type specification snippet:
      ```yaml
      candidate:
        relations:
          interview_committee: committee
          lead: user
          interviewer: user
        permissions:
          can_interview: interview_committee->is_member | interviewer | lead
          can_view: can_interview
      ```
    - `enabled` (Check, default `1`)
  - **Validation & Safety Rules on Save:**
    - Parse `manifest_fragment` with PyYAML on `validate()`.
    - Dry-run validation against Topaz PDP: Verify syntax and schema integrity (Topaz validates relation targets and permissions graph). If Topaz rejects the fragment, abort transaction with a user-friendly error.
- **Manifest Stitcher Engine**
  - Build `topaz_frappe.core.manifest.stitch_manifest()`:
    - Reads base core manifest (`institution`, `department`, `committee`, `user`).
    - Queries all active `Topaz External Resource` records from Frappe DB.
    - Merges their `manifest_fragment` blocks under `types:`.
    - Validates target relations (e.g. `committee` exists in core types).
    - Uploads the unified manifest to Topaz (`POST /api/v3/directory/manifest`). Topaz performs the authoritative validation of the compiled schema.
  - Automatically re-stitch and reload manifest on `on_update` / `on_trash` of `Topaz External Resource`.
  - Provide bench command: `bench --site <site> topaz-stitch-manifest`.

### 2. Whitelisted Dynamic Assignment API Endpoint
- **`topaz_frappe.api.assign_relation`**
  - Whitelisted RPC endpoint for satellite apps to link external local IDs to core subjects:
    ```python
    @frappe.whitelist()
    def assign_relation(
        object_type: str,
        object_id: str,
        relation: str,
        subject_type: str,
        subject_id: str,
    ) -> dict:
        """Validate against Topaz External Resource & core entities, then write tuple to Topaz."""
    ```
  - **Validation Steps:**
    1. Query `Topaz External Resource` where `resource_type = object_type` and `enabled = 1`. If missing, reject: `"Unregistered resource type '{object_type}'"`.
    2. Parse the resource's `manifest_fragment` to confirm `relation` is allowed and maps to `subject_type`. If invalid, reject: `"Relation '{relation}' is not defined for '{object_type}'"`.
    3. Verify `subject_id` exists in Frappe DB (e.g. `committee` -> `Eduauth Committee`, `department` -> `Eduauth Department`, `user` -> `User`). If missing, reject: `"{subject_type} '{subject_id}' does not exist in central directory"`.
    4. Write clean tuple directly to Topaz REST API (`POST /api/v3/directory/relation`).
  - Return clear, human-readable error messages on typos or missing entities.
- **`topaz_frappe.api.remove_relation`**
  - Whitelisted RPC endpoint to safely delete a relation tuple from Topaz when assignments are cancelled or deleted in satellite apps.

### 3. Core Subject Read API
- Standard Frappe REST API / filters allow satellite app frontends (or composite shells) to retrieve dropdown options for valid core entities:
  - `GET /api/resource/Eduauth Committee?fields=["name","committee_name"]`
  - `GET /api/resource/Eduauth Department?fields=["name","department_name"]`

---

## 📖 Direct Topaz Check Reference Documentation

Satellite services do **not** route runtime check requests through Frappe. They evaluate `is_allowed` directly against Topaz's REST/AuthZEN API in < 1ms.

Document copy-pasteable reference helper functions in the documentation:

### Python Reference (FastAPI / Flask)
```python
import os
import requests

TOPAZ_HOST = os.getenv("TOPAZ_HOST", "http://topaz:8383")

def is_allowed(user: str, action: str, resource_type: str, resource_id: str) -> bool:
    """One-line authorization check querying Topaz PDP directly."""
    try:
        response = requests.post(
            f"{TOPAZ_HOST}/api/v3/directory/check",
            json={
                "object_type": resource_type,
                "object_id": resource_id,
                "relation": action,
                "subject_type": "user",
                "subject_id": user,
            },
            timeout=0.5,  # Fail fast
        )
        return response.status_code == 200 and response.json().get("check", False)
    except Exception:
        return False  # Fail closed
```

### Go Reference
```go
package auth

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
	"time"
)

var topazHost = os.Getenv("TOPAZ_HOST") // e.g. "http://topaz:8383"
var httpClient = &http.Client{Timeout: 500 * time.Millisecond}

func IsAllowed(user, action, resourceType, resourceID string) bool {
	payload, _ := json.Marshal(map[string]string{
		"object_type":  resourceType,
		"object_id":    resourceID,
		"relation":     action,
		"subject_type": "user",
		"subject_id":   user,
	})

	resp, err := httpClient.Post(topazHost+"/api/v3/directory/check", "application/json", bytes.NewBuffer(payload))
	if err != nil || resp.StatusCode != http.StatusOK {
		return false
	}
	defer resp.Body.Close()

	var result struct {
		Check bool `json:"check"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return false
	}
	return result.Check
}
```

### Node.js / TypeScript Reference
```typescript
const TOPAZ_HOST = process.env.TOPAZ_HOST || 'http://topaz:8383';

export async function isAllowed(
  user: string,
  action: string,
  resourceType: string,
  resourceId: string
): Promise<boolean> {
  try {
    const res = await fetch(`${TOPAZ_HOST}/api/v3/directory/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        object_type: resourceType,
        object_id: resourceId,
        relation: action,
        subject_type: 'user',
        subject_id: user,
      }),
      signal: AbortSignal.timeout(500),
    });
    if (!res.ok) return false;
    const data = await res.json();
    return !!data.check;
  } catch {
    return false;
  }
}
```

---

## 🚀 Developer Experience for Fast-Turnover Teams

### The 3-Step "Cheat Sheet" for Satellite App Developers
1. **Step 1: Register Resource**  
   In Frappe Desk (or via API / fixture), create a `Topaz External Resource` record with your YAML `manifest_fragment`.
2. **Step 2: Assign via Frappe**  
   When assigning a candidate in your satellite app, call:  
   `POST /api/method/topaz_frappe.api.assign_relation` with the candidate ID, relation, and selected core entity.
3. **Step 3: Guard Endpoints**  
   In your controller routes, check permission directly against Topaz:  
   `if not is_allowed(user=current_user, action="can_interview", resource_type="candidate", resource_id=id): raise Forbidden()`.

### Standardized Error Responses
API validation errors clearly point out developer mistakes:
- `"Committee 'Order_Of_The_Phoenix' does not exist."`
- `"Relation 'interviewer' is not registered on object 'candidate'."`

### Local Sandbox Runbook
- Docker Compose / DevContainer running Frappe + Topaz.
- Pre-seeded fictional entities (`Hogwarts`, `Gryffindor`, `Order_Of_The_Phoenix`) to verify assignments and checks locally.
