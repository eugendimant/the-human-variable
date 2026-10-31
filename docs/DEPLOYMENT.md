# Deployment

The game is a single HTML file. The live classroom and the tutor need a server process that keeps shared state. A Streamlit iframe alone cannot provide that: it renders the page, but it does not expose the classroom API to students' phones. This document covers three ways to deploy, from the simplest to the most capable. Nothing here has been published; every step needs your accounts and your approval.

## Option A: static game only (GitHub Pages)

Use this for self-study, with no live class and no AI tutor.

1. Push the repository to GitHub.
2. Go to Settings, then Pages, and choose Deploy from branch, `main`, `/ (root)`.
3. Students open `https://<user>.github.io/<repo>/`.

`index.html` runs fully offline. Progress stays in each student's browser. The tutor answers from the lab's checked summaries.

The offline file contains every answer, because it must reveal results without a server. That suits self-study. For graded or live classes, use Option B or C: the server strips answers from the page and releases evidence only after each call is locked, and holds it during a live class until the instructor reveals it.

## Option B: one container (recommended for teaching)

The container runs the game, live classroom and tutor together, using only the Python standard library.

```bash
docker build -t human-variable .
docker run -p 8080:8080 -v thv-data:/data \
  -e THV_INSTRUCTOR_PASSCODE='choose-one' \
  -e GEMINI_API_KEY='optional' \
  human-variable
```

| Host | Steps | Persistence |
|---|---|---|
| Render | New Blueprint and select the repo. `render.yaml` defines a web service with a 1 GB disk at `/data`. Set the secrets in the dashboard. | Disk survives restarts (paid instance) |
| Fly.io | `fly launch --no-deploy`, then `fly volumes create thv_data --size 1`, then `fly secrets set THV_INSTRUCTOR_PASSCODE=... GEMINI_API_KEY=...`, then `fly deploy` (`fly.toml` is included) | Volume survives restarts |
| Railway or any container host | Deploy the Dockerfile, mount a volume at `/data` and set the variables | Depends on the volume |

Students open `https://your-host/` and tap **Join a class**, or scan the QR code on the instructor screen. The instructor opens `https://your-host/classroom`.

**Capacity.** One process with SQLite in WAL mode. Participants poll every 2 seconds, and polls are served from an in-memory versioned cache. A test with 50 simulated phones polling and submitting at once gave a p95 latency of 2 ms (`tests/test_http.py`). A small instance is enough for 50 to 120 students. Run one instance only: SQLite is a single-writer store and the cache lives in memory.

**Security in place:**
- HTTPS comes from the host.
- Instructor keys and participant tokens are random and stored only as SHA-256 hashes.
- Responses carry a Content Security Policy, nosniff and no-referrer.
- Request bodies are capped at 8 KB.
- Rate limits apply per browser plus a ceiling per IP, so a class behind one campus NAT is not throttled.
- Session creation can require `THV_INSTRUCTOR_PASSCODE`.
- Participants are numbers, with no names.
- Session data is deleted when the instructor ends the session, or after `THV_RETENTION_HOURS` (default 48).
- CSV export uses formula escaping.

**Environment variables.**

| Variable | Default | Purpose |
|---|---|---|
| `HOST`, `PORT` | `127.0.0.1`, `8502` (the Dockerfile uses `0.0.0.0`, `8080`) | Bind address |
| `THV_DATA_DIR` | `server/data` | SQLite files |
| `THV_INSTRUCTOR_PASSCODE` | empty | Required to create sessions when set |
| `THV_RETENTION_HOURS` | `48` | Automatic deletion of session data |
| `THV_MAX_PARTICIPANTS` | `120` | Per session |
| `THV_TRUST_PROXY` | empty (`1` in Docker) | Read client IP from `X-Forwarded-For` |
| `THV_FRAME_ANCESTORS` | `'self'` | Who may embed the site in an iframe |
| `GEMINI_API_KEY` or `GOOGLE_API_KEY` | empty | Enables the AI tutor. See `TUTOR.md` |

## Option C: Streamlit Community Cloud

1. Push to GitHub. On share.streamlit.io, create an app with main file `streamlit_app.py`.
2. In the app's Secrets, add the secrets you need:

```toml
THV_INSTRUCTOR_PASSCODE = "choose-one"
GEMINI_API_KEY = "optional"
```

Pages:
- **Play:** the full game, embedded full-window.
- **Join a class** and **Run a class:** native Streamlit pages that read and write the same classroom store in-process.
- **Ask the tutor:** the grounded tutor.

**Limits to know:**
- Community Cloud runs one process. Live classes work because every browser session shares it.
- The disk is ephemeral. Classroom data is lost when the app sleeps, restarts or redeploys. Download the CSV at the end of each class.
- Each student holds a websocket session. Streamlit reruns cost more than the container's polling API, so for 40 to 50 students Option B is the safer choice.
- Students join through the **Join a class** page with the code. The embedded game hides its join button because it cannot reach the API from inside Streamlit's frame.
- **Play** embeds the self-study file, which carries its answers. When `THV_INSTRUCTOR_PASSCODE` is set (a deployment for classes), Play shows a pointer to **Join a class** instead, unless you set `THV_STREAMLIT_SOLO=1`. During a live class Play is paused either way.

## Local classroom (one laptop, same network)

Run `python start_classroom.py`. It binds `127.0.0.1` by default. To let phones on the same Wi-Fi join, run `HOST=0.0.0.0 python start_classroom.py` and share `http://<laptop-ip>:8502/`. This is plain HTTP, so use it only on a trusted network.
