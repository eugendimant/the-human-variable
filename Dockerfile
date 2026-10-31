# The Human Variable: game, live classroom and tutor in one container (standard-library Python).
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOST=0.0.0.0 PORT=8080 THV_DATA_DIR=/data THV_TRUST_PROXY=1
WORKDIR /app
COPY index.html classroom.html start_classroom.py ./
COPY server ./server
COPY src/bank.json ./src/bank.json
RUN useradd -m thv && mkdir -p /data && chown thv /data
USER thv
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request,os;urllib.request.urlopen(f'http://127.0.0.1:{os.environ[\"PORT\"]}/api/health',timeout=2)"
CMD ["python", "-m", "server.app"]
