## Stage 1
FROM python:3.11.4 as builder

WORKDIR /project
ENV POETRY_VERSION=1.3.1
# Install packages
RUN pip install "poetry==$POETRY_VERSION"

# Copy Pipfile and Pipfile.lock
COPY pyproject.toml poetry.lock ./

# Generate requirements.txt using poetry
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

RUN pip install --no-cache --requirement requirements.txt

## Stage 2

FROM python:3.11.4-slim-bookworm

# Copy python packages from previous stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
WORKDIR /project
COPY ditto_deploy ditto_deploy
RUN addgroup --gid 1001 abi && adduser --disabled-password --ingroup abi --uid 1001 abi
USER 1001