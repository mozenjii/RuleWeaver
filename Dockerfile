# The reviewer application, as one container.
#
#   docker build -t ruleweaver .
#   docker run -p 8000:8000 -v ruleweaver-data:/data \
#     -e RULEWEAVER_SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')" \
#     ruleweaver
#
# It refuses to start without an identity provider; see README "The gate". The audit log
# defaults to SQLite on the /data volume. For PostgreSQL, set RULEWEAVER_DATABASE_URL.

FROM python:3.12-slim AS build
WORKDIR /src
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir build==1.3.0 && python -m build --wheel --outdir /dist

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    RULEWEAVER_DATABASE_URL=sqlite:////data/review.db

# The same wheel CI checks, not the source tree, so the image runs what a user installs.
COPY --from=build /dist/ /tmp/dist/
RUN pip install --no-cache-dir "$(ls /tmp/dist/ruleweaver-*.whl)[review,postgres]" \
    && rm -rf /tmp/dist \
    && useradd --create-home --uid 10001 ruleweaver \
    && mkdir /data && chown ruleweaver /data

WORKDIR /app
COPY --chown=ruleweaver examples ./examples
USER ruleweaver
VOLUME /data
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import sys, urllib.request; sys.exit(urllib.request.urlopen('http://127.0.0.1:8000/healthz').status != 200)"

ENTRYPOINT ["ruleweaver"]
CMD ["review", "examples/snap/rules.json", "--host", "0.0.0.0"]
