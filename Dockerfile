# cool stuff grabbed from here: https://github.com/gianfa/poetry/blob/d12242c88edf1c8cf6d9aa70677beda212576760/docker-examples/poetry-multistage/Dockerfile

FROM python:3.12-slim AS builder

# --- Install Poetry ---
ARG POETRY_VERSION=1.8

ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

# --- Reproduce the environment ---
# You can comment the following two lines if you prefer to manually install
#   the dependencies from inside the container.
COPY pyproject.toml .
COPY poetry.lock .
COPY count_von_count ./count_von_count
COPY data ./data

# Install the dependencies and clear the cache afterwards.
#   This may save some MBs.
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Now let's build the runtime image from the builder.
#   We'll just copy the env and the PATH reference.
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
# totally shouldnt copy this could mount later for test.
# ideally this is just temp and we stream direct.
ENV TEST_FILE=/app/data/fy25_air_force_working_capital_fund.pdf

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /app/count_von_count /app/count_von_count
COPY --from=builder /app/data /app/data

# download model
RUN python -m spacy download en_core_web_sm

# TODO: we should be fine without a GPU butttt if time permits we can hook it up for zoom zoom.
# thats just quite a pain for other folks machine.

EXPOSE 8000

# TODO: obviously we need to override the entrypoint to run it
ENTRYPOINT ["uvicorn", "count_von_count.main:create_app", "--factory", "--host", "0.0.0.0"]