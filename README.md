# middesk-api

Run everything from `src/middesk_api`:

```bash
cd src/middesk_api

uv run fastapi dev main.py              # API → http://127.0.0.1:8000/docs
uv run python ingest.py sample.csv      # load CSV into app.db
sqlite3 app.db                          # inspect DB
```
