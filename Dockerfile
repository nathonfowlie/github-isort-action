FROM python:latest

COPY files /

RUN python3 -m pip install pipx && \
    python3 -m pipx ensurepath

RUN pipx ensurepath && \
    pipx install isort

RUN chown -R root:root /app

ENTRYPOINT ["/app/entrypoint.sh"]