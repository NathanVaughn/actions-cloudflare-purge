FROM alpine:3.13.1

RUN apk add --no-cache bash curl

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]