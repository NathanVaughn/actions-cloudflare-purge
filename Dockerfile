FROM alpine:3.10.2

RUN apk add --no-cache bash curl

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]