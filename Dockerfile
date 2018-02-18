FROM alpine:3.7 AS builder

RUN \
  apk update && \
  apk add \
    python3=3.6.3-r9 postgresql-dev=10.2-r0 gcc=6.4.0-r5 \
    python3-dev=3.6.3-r9 libc-dev=0.7.1-r0 libffi-dev=3.2.1-r4

RUN pip3 install gunicorn==19.7.1

COPY src/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# ---

FROM alpine:3.7

RUN mkdir -p /app/src
WORKDIR /app/src/

RUN \
  apk update && \
  apk add python3=3.6.3-r9 postgresql-client=10.1-r1

ENV MJOE_ENV_FILE /run/secrets/env

COPY --from=builder /usr/lib/python3.6/ /usr/lib/python3.6/
COPY --from=builder /usr/bin/gunicorn /usr/bin/gunicorn

COPY docker/start /app/start
COPY src/ /app/src/

CMD ["/app/start"]
