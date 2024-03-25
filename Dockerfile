FROM alpine:3.10

COPY files /

RUN chown -R root:root /app

ENTRYPOINT ["/app/entrypoint.sh"]