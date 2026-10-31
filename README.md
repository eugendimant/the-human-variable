# THE HUMAN VARIABLE

Interactive behavioral science decision game. Original concept by Professor Eugen Dimant. No university endorsement implied.

## Fastest way to play

Unzip the package. Open `START_HERE.html`, then click **Play the offline game**. Or open `index.html` directly in Chrome, Edge, Firefox, or Safari. The individual game does not require Python, Streamlit, a server, or an API key.

## Live classroom (instructor and participants)

Install Python 3.10+ if needed. Open a terminal **inside the unzipped `The_Human_Variable` folder**, then run:

```
python start_classroom.py
```

On Windows, `py start_classroom.py` may be needed. Open `http://localhost:8502/classroom` in a browser on the same computer. The instructor creates a session, students enter the code and answer the question. **For students on different devices**, localhost will not work: the server must be deployed to an accessible, appropriately secured host. Do not deploy the prototype publicly without authentication, TLS, and abuse protection.

## Streamlit

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Streamlit embeds the individual game. For the best full-screen experience, use the standalone HTML. Streamlit does not automatically run the classroom backend.

## Development and checks

```
python src/build.py
python -m unittest discover -s tests -v
```

Source content is `src/bank.json`. The individual game stores progress locally. A Gemini tutor is not deployed. Scientific metadata has not been independently verified publication-by-publication.

## Claude continuation
Open `docs/CLAUDE_MASTER_EXECUTION_PROMPT.md` and `docs/TECHNICAL_HANDOVER.md`. Scientific and production readiness are **not certified**. This package intentionally excludes runtime SQLite data and Python caches.
