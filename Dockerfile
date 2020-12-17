FROM alpine:3.12.3

RUN apk add --no-cache bash curl

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]