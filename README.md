# Eduauth Frappe

`eduauth_frappe` demonstrates how an education ERP / institute management application uses **`topaz_frappe`** to turn Frappe into the authoring and governance control plane for a **[Topaz](https://www.topaz.sh)** (AuthZen / Zanzibar ReBAC) directory.

---

## 🏛️ Architecture & Mental Model

```
       ┌────────────────────────────────────────────────────────┐
       │                   Frappe Desk / API                    │
       │  Authoring UI for Institutes, Departments, Committees, │
       │         Projects, Roles, Groups, and Users             │
       └───────────────────────────┬────────────────────────────┘
                                   │ Document Events (after_commit)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                      topaz_frappe                      │
       │    Reads topaz_registry in hooks.py, computes diffs,   │
       │    and syncs object & relationship tuples via REST v3  │
       └───────────────────────────┬────────────────────────────┘
                                   │ HTTP (POST /object, POST /relation)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                  Topaz Directory Engine                │
       │           Evaluates Zanzibar ReBAC graph &             │
       │          serves AuthZen authorization checks           │
       └───────────────────────────▲────────────────────────────┘
                                   │
              Downstream Microservices (FastAPI, Java, Go)
              Query Topaz directly: POST /api/v3/directory/check
```

* **Frappe is the Authoring Surface**: Frappe users edit standard documents (Institutes, Departments, Committees).
* **Topaz is the Source of Truth for Authorization**: Downstream services query Topaz (not Frappe) to answer authorization decisions in sub-milliseconds.
* **No Domain Controller Boilerplate**: Consuming apps do **not** modify DocType Python controllers or JavaScript views. Everything is declared in `hooks.py`.

---

## 🛠️ What Does an App Need to Add to Use `topaz_frappe`?

To integrate any Frappe app with Topaz, you only need **two things**:

### 1. A Topaz Schema (`manifest.yaml`)
Place your authorization model schema in your app at:
`eduauth_frappe/topaz/manifest.yaml`

This defines your object types, base relations, and computed permissions (such as `lead = head | acting_head` or `can_review = is_member`).

### 2. The `topaz_registry` Hook in `hooks.py`
In your app's `hooks.py`, declare the `topaz_registry` dictionary. Frappe merges this hook across installed apps.

**No changes to DocType Python classes (`.py`), client scripts (`.js`), or custom controllers are needed.**

Example from [`eduauth_frappe/hooks.py`](./eduauth_frappe/hooks.py):

```python
topaz_registry = {
    # 1. Root / Independent entity
    "Eduauth Institute": {
        "object": {"type": "institution", "id_field": "name"},
        "relations": [
            {"kind": "link", "relation": "director", "target_type": "user", "field": "director"},
            {"kind": "link", "relation": "deputy_director", "target_type": "user", "field": "deputy_director"},
            {"kind": "link", "relation": "dean_rnd", "target_type": "user", "field": "dean_rnd"},
            {"kind": "link", "relation": "dean_ap", "target_type": "user", "field": "dean_ap"},
            {"kind": "link", "relation": "dean_admin", "target_type": "user", "field": "dean_admin"},
            {"kind": "link", "relation": "registrar", "target_type": "user", "field": "registrar"},
        ],
    },

    # 2. Hierarchical entity with foreign link and child tables
    "Eduauth Department": {
        "object": {"type": "department", "id_field": "name"},
        "relations": [
            # Edge to parent institution (object -> object)
            {"kind": "link", "relation": "parent_institute", "target_type": "institution", "field": "parent_institute"},
            # Link to User
            {"kind": "link", "relation": "head", "target_type": "user", "field": "head"},
            {"kind": "link", "relation": "acting_head", "target_type": "user", "field": "acting_head"},
            # Link to a Role with subject-set (store_keeper -> role:X#assignee)
            {"kind": "link", "relation": "store_keeper", "target_type": "role", "field": "store_keeper_role", "subject_relation": "assignee"},
            # Child table sets -> subject relations
            {"kind": "child", "table": "faculty_members", "subject_field": "user", "static_relation": "faculty"},
            {"kind": "child", "table": "students", "subject_field": "user", "static_relation": "student"},
            {"kind": "child", "table": "staff_members", "subject_field": "user", "static_relation": "staff"},
            {"kind": "child", "table": "candidates", "subject_field": "user", "static_relation": "candidate"},
        ],
        # (Optional) Opt-in Desk permission mappings:
        "permissions": {
            "read": "is_member",     # List view & read access if user is member
            "write": "lead",          # Edit access if user is HOD/acting head
        },
    },

    # 3. Committee with child table membership
    "Eduauth Committee": {
        "object": {"type": "committee", "id_field": "name"},
        "relations": [
            {"kind": "link", "relation": "chair", "target_type": "user", "field": "chair"},
            {"kind": "child", "table": "members", "subject_field": "user", "static_relation": "member"},
            {"kind": "child", "table": "external_experts", "subject_field": "user", "static_relation": "external_expert"},
        ],
        # (Optional) Opt-in Desk permission mappings:
        # Maps an array/list of relations: access granted if ANY relation matches (OR logic)
        "permissions": {
            "read": ["is_member", "can_access"],
            "write": "can_sign",
        },
    },

    # 4. Standard User DocType registration
    "User": {
        "object": {"type": "user", "id_field": "name"},
        "relations": [],
    },
}
```

---

## 📋 Mapped DocTypes & Schema in `eduauth_frappe`

| DocType | Topaz Object Type | Emitted Base Relations | Computed Permissions in Topaz |
|---|---|---|---|
| **Eduauth Institute** | `institution` | `director`, `deputy_director`, `dean_rnd`, `dean_ap`, `dean_admin`, `registrar` | `is_executive`, `is_central_admin`, `can_escalate_rnd` |
| **Eduauth Department** | `department` | `parent_institute`, `head`, `acting_head`, `faculty`, `student`, `staff`, `candidate`, `store_keeper` | `lead` (`head \| acting_head`), `is_academic`, `is_member`, `can_escalate_rnd` |
| **Eduauth Committee** | `committee` | `chair`, `member`, `external_expert` | `is_member`, `can_review`, `can_sign` |
| **Eduauth Project** | `project` | `host_department`, `lead_investigator`, `co_investigator`, `research_fellow`, `delegate_signatory` | `investigator`, `lead`, `member`, `department_lead`, `can_view` |
| **Eduauth Group** | `group` | `member` (`user \| group#member`) | – |
| **Eduauth Role** | `role` | `assignee` (`user \| group#member`) | `is_assigned` |
| **Eduauth Identity**| `identity` | `identifier` (`user`) | – |
| **User** | `user` | – | – |

---

## 🛠️ Quickstart with DevContainer

Open this folder in VS Code or any devcontainer-compatible environment (**Reopen in Container**). It spins up Frappe, MariaDB, Redis, and Topaz automatically.

Inside the container terminal, run:

```bash
# 1. Quickstart bench and install topaz_frappe + eduauth_frappe using installer.py
./installer.py -j apps.json

# 2. Start the bench server
cd frappe-bench
bench start
```

---

## 🚀 Step-by-Step Topaz & Permissions Setup

### 1. Site Configuration
Enable Topaz on your site and set the directory host:
```bash
bench --site localhost set-config topaz_enabled true
bench --site localhost set-config topaz_host http://topaz:8383
bench --site localhost set-config topaz_subject_type user
```

### 2. Load the App Manifest into Topaz
Upload `eduauth_frappe`'s schema manifest into Topaz:
```bash
bench --site localhost topaz-load-manifest
```

### 3. Check Connectivity & Health
Probe the Topaz connection:
```bash
bench --site localhost topaz-health
```

### 4. Seed Demo Users and Records
On a fresh site with no users or records, run the demo hydration script:
```bash
bench --site localhost execute eduauth_frappe.commands.setup_demo
```
This script automatically:
* Creates demo users: `albus.dumbledore@hogwarts.edu` (`System Manager`), `minerva.mcgonagall@hogwarts.edu` (`Desk User`), and `harry.potter@hogwarts.edu` (`Desk User`).
* Sets all their passwords to `password123`.
* Grants `Desk User` role access on the DocTypes so Frappe delegates Desk permission checks to Topaz.
* Creates `Hogwarts` (Institute), `Gryffindor` (Department), and `Order_Of_The_Phoenix` (Committee).

### 5. Bulk Sync Data to Topaz
Sync the newly seeded database records into Topaz:
```bash
bench --site localhost topaz-sync
```

### 6. Enable Topaz Desk Permissions
Enable Topaz ReBAC enforcement for Frappe Desk views and documents:
```bash
bench --site localhost set-config topaz_desk_permissions true
```

### 7. Test in Browser at `http://localhost:8000`
Open `http://localhost:8000` in your browser and test with different user logins:

1. **Log in as Minerva** (`minerva.mcgonagall@hogwarts.edu` / `password123`):
   * Visit `/app/eduauth-department`: Can view and edit `Gryffindor` (she is Department Head and Faculty).
   * Visit `/app/eduauth-committee`: Can view `Order_Of_The_Phoenix` (she is a Committee Member; evaluated via `["is_member", "can_access"]`).
   * Attempting to edit or sign the Committee will fail (only `chair` has `can_sign`).

2. **Log in as Harry** (`harry.potter@hogwarts.edu` / `password123`):
   * Visit `/app/eduauth-department`: Can view `Gryffindor` (he is a Student in the Department).
   * Attempting to edit `Gryffindor` will fail (he is not Department Head / `lead`).
   * Visit `/app/eduauth-committee`: List is empty (access denied because Harry is not a member of the Committee).

3. **Log in as Albus** (`albus.dumbledore@hogwarts.edu` / `password123`):
   * Full access to `Order_Of_The_Phoenix` as Committee Chair (`can_sign`).

---

### 8. Verify Authorization Probe via CLI
Probe ReBAC permissions directly:
```bash
bench --site localhost topaz-health --object-type institution --object-id Hogwarts --relation director
```

### 9. Prune Dangling Objects
Reconcile Topaz with the Frappe database and remove orphaned objects:
```bash
# Dry run:
bench --site localhost topaz-prune --dry-run

# Execute prune:
bench --site localhost topaz-prune
```

---

## 🔍 Querying Topaz from Downstream Microservices

External applications query Topaz REST API directly without hitting Frappe:

```python
import requests

response = requests.post("http://topaz:8383/api/v3/directory/check", json={
    "object_type": "department",
    "object_id": "Gryffindor",
    "relation": "lead",
    "subject_type": "user",
    "subject_id": "minerva.mcgonagall@hogwarts.edu"
})

print(response.json())
# Output: {'check': True, 'trace': [], 'context': {}}
```
