import argparse
import json
import os
import pprint
import sys
from typing import List
from urllib import request


def split_and_flatten_list(items: List[str]) -> List[str]:
    """
    Take a list of strings and return a flat list of strings of the previous
    elements split by spaces.
    """
    # in case input is None, return an empty list
    if items is None:
        return []

    new_list = []

    # split each element by spaces
    for item in items:
        new_list.extend(item.split(" "))

    # filter out empty strings
    return [i for i in new_list if i != ""]


def main() -> None:
    if not os.getenv("NATHANVAUGHN_TESTING"):
        print(f"::debug::{' '.join(sys.argv)}")

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

    args = parser.parse_args()

    # this is weird because while each argument accepts a list, GitHub Actions
    # provides a single value for each argument. So, need to split each element
    # by spaces to make it compatible with both with weird argument stuff
    # and normal CLI usage.
    args.urls = split_and_flatten_list(args.urls)
    args.tags = split_and_flatten_list(args.tags)
    args.hosts = split_and_flatten_list(args.hosts)
    args.prefixes = split_and_flatten_list(args.prefixes)

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
    req_data = {}

    if args.urls:
        req_data["files"] = args.urls

    if args.tags:
        req_data["tags"] = args.tags

    if args.hosts:
        req_data["hosts"] = args.hosts

    if args.prefixes:
        req_data["prefixes"] = args.prefixes

    if not any([args.urls, args.tags, args.hosts, args.prefixes]):
        req_data["purge_everything"] = True

    # create the request
    url = f"https://api.cloudflare.com/client/v4/zones/{args.cf_zone}/purge_cache"
    encoded_data = json.dumps(req_data).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {args.cf_auth}",
        "Content-Type": "application/json",
        "Content-Length": len(encoded_data),
    }

    if os.getenv("NATHANVAUGHN_TESTING"):
        # when testing, don't actually make a request
        print(url)
        print(json.dumps(headers))
        print(json.dumps(req_data))
        sys.exit()
    else:
        print("Request:")
        print(f"\033[0;36m{url}\033[0m")
        # print(f"\033[0;36m{pprint.pformat(headers)}\033[0m")
        print(f"\033[0;36m{pprint.pformat(req_data)}\033[0m")

    req = request.Request(url, data=encoded_data, headers=headers)
    resp = request.urlopen(req)

    # process response
    resp_data = json.loads(resp.read())

    print("\n")
    print("Response:")
    print(f"\033[0;36m{pprint.pformat(resp_data)}\033[0m")

    if resp_data["success"] != True:
        print("::error::Success NOT True")
        sys.exit(1)


if __name__ == "__main__":
    main()
