# Fork: `categoryid` field for bills

This branch (`feat/categoryid`) adds an optional `categoryid` field (Integer, nullable) to
IHateMoney's `Bill` model, form, and web UI. Stock IHateMoney has no category field for bills at
all — this has been an [open upstream request since 2011](https://github.com/spiral-project/ihatemoney/issues/55),
with two failed attempts ([#557](https://github.com/spiral-project/ihatemoney/pull/557),
[#923](https://github.com/spiral-project/ihatemoney/pull/923)), and the project is in maintenance
mode — so this lives as a fork rather than a PR.

**What changed** (`ihatemoney/models.py`, `ihatemoney/forms.py`,
`ihatemoney/templates/{forms,list_bills}.html`, a new Alembic migration, plus the existing test
suite updated for the new field): a `Bill.category_id` column, serialized as JSON key
`categoryid` (no underscore — matches what MoneyBuster/Cospend clients already send on the wire),
editable via a dropdown in the web UI's bill form and shown as a column in the bill list.
Negative IDs are Nextcloud Cospend's fixed global categories (grocery, rent, transport, ...);
`null` means unclassified. Full rationale, wire-format verification (against MoneyBuster's own
source), and test results are in this repo's own `README.md` history — see the original patch
notes at
[modularidea/obsidian-ihm-tracker/server-patch/README.md](https://github.com/modularidea/obsidian-ihm-tracker/blob/main/server-patch/README.md).

Built for and used by **[IHM Tracker](https://github.com/modularidea/obsidian-ihm-tracker)**, an
Obsidian plugin for IHateMoney — the plugin works fully without this fork (its own vault-file
category sync is the default path); this fork is an optional upgrade for people who self-host
IHateMoney and want the category visible to *other* IHM clients too (web UI, MoneyBuster,
Cospend), not just the plugin.

Base commit: `e66a7672e8e5c41549bf53c4a824c72c43ab9079` (upstream `main`, "Back to development:
7.2.2"). Upstream's own test suite is unmodified in behavior (146 passed, 5 skipped, same as
before the patch).

## Running locally with Docker

```bash
git clone --branch feat/categoryid https://github.com/modularidea/ihatemoney-cat.git
cd ihatemoney-cat
docker compose -f docker-compose.fork.yml up --build
```

Builds this checkout (patched code included) instead of pulling the official
`ihatemoney/ihatemoney` image, and starts it on `http://localhost:8000`. `docker-compose.fork.yml`
uses the same environment variables as upstream's own `docker-compose.yml` example — see
[the config docs](https://ihatemoney.readthedocs.io/en/latest/configuration.html) for all of
them. It's a local-dev example (`SECRET_KEY`/`ADMIN_PASSWORD` are placeholders) — set your own
values before exposing it beyond `localhost`.
