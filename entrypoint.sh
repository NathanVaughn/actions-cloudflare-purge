#!/bin/bash

set -e

function print_error() {
    echo -e "\e[31mERROR: ${1}\e[m"
}

if [ -z "${CLOUDFLARE_ZONE}" ]; then
    print_error "Cloudflare zone not found"
    exit 1
fi

if [ -z "${CLOUDFLARE_EMAIL}" ]; then
    print_error "Cloudflare email address key not found"
    exit 1
fi

if [ -z "${CLOUDFLARE_AUTH_KEY}" ]; then
    print_error "Cloudflare auth key not found"
    exit 1
fi

response = $(
    curl -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE}/purge_cache" \
    -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
    -H "X-Auth-Key: ${CLOUDFLARE_AUTH_KEY}" \
    -H "Content-Type: application/json" \
    --data '{"purge_everything":true}'
)

echo "Response data: $response"