import argparse
import json
import pprint
import os
import sys
from urllib import request, parse


def main():
    # parse the arguments
    parser = argparse.ArgumentParser()

    # load values from environment first, by default
    parser.add_argument("--cf-zone", nargs="?", type=str)
    parser.add_argument("--cf-auth", nargs="?", type=str)

    # caching objects
    parser.add_argument("--urls", nargs="*", type=str)
    parser.add_argument("--tags", nargs="*", type=str)
    parser.add_argument("--hosts", nargs="*", type=str)
    parser.add_argument("--prefixes", nargs="*", type=str)

    args = parser.parse_args(sys.argv[1])

    # if no argument given, pull from environment
    if not args.cf_zone:
        args.cf_zone = os.getenv("CLOUDFLARE_ZONE")
        
    if not args.cf_auth:
        args.cf_auth = os.getenv("CLOUDFLARE_AUTH_KEY")

    # see if anything was set
    if not args.cf_zone:
        parser.error("Cloudflare Zone required")

    if not args.cf_auth:
        parser.error("Cloudflare Auth required")

    # prepare the request data

    data = {}

    if args.urls:
        data["files"] = args.urls

    if args.tags:
        data["tags"] = args.tags

    if args.hosts:
        data["hosts"] = args.hosts

    if args.prefixes:
        data["prefixes"] = args.prefixes

    if not args.urls and not args.tags and not args.hosts and not args.prefixes:
        data["purge_everything"] = True

    # create the request
    url = f"https://api.cloudflare.com/client/v4/zones/args.cf_zone/purge_cache"
    headers = {"Authorization": f"Bearer {args.cf_auth}"}
    encoded_data = parse.urlencode(data).encode()

    # send it
    print(f"Making POST request to {url} with {data}")

    req = request.Request(url, data=encoded_data, headers=headers)
    resp = request.urlopen(req)

    # process response
    resp_data = json.loads(resp.read())

    print(pprint.pprint(resp_data))

    if resp_data["success"] != True:
        raise Exception("Success NOT True")


if __name__ == "__main__":
    main()