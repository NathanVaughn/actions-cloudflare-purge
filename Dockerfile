FROM alpine:3.13.4

RUN apk add --no-cache bash curl

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]