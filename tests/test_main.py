import json
import os
import subprocess
import sys
from typing import List, Tuple

import pytest

# weird environment variable to enable testing mode that no one else should ever set
os.environ["NATHANVAUGHN_TESTING"] = "True"


def run_command(options: List[str]) -> Tuple[str, dict, dict]:
    # run the command just as the Action does, and return the results
    main = os.path.join(os.path.dirname(__file__), "..", "main.py")
    output = subprocess.check_output([sys.executable, main] + options, text=True)

    output_split = output.split("\n")
    url = output_split[0]
    headers: dict = json.loads(output_split[1])
    data: dict = json.loads(output_split[2])

    return url, headers, data


def test_legacy():
    # test the legacy method of authentication
    os.environ["CLOUDFLARE_ZONE"] = "zone123"
    os.environ["CLOUDFLARE_AUTH_KEY"] = "key123"
    url, headers, data = run_command(
        [
            "--cf-zone",
            "",
            "--cf-auth",
            "",
            "--urls",
            "",
            "--tags",
            "",
            "--hosts",
            "",
            "--prefixes",
            "",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"purge_everything": True}

    del os.environ["CLOUDFLARE_ZONE"]
    del os.environ["CLOUDFLARE_AUTH_KEY"]


def test_new():
    # test the new method of authentication
    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "key123",
            "--urls",
            "",
            "--tags",
            "",
            "--hosts",
            "",
            "--prefixes",
            "",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"purge_everything": True}


def test_new_missing():
    # test missing authentication
    with pytest.raises(Exception):
        run_command(
            [
                "--cf-zone",
                "",
                "--cf-auth",
                "",
                "--urls",
                "",
                "--tags",
                "",
                "--hosts",
                "",
                "--prefixes",
                "",
            ]
        )

    with pytest.raises(Exception):
        run_command(
            [
                "--cf-zone",
                "zone123",
                "--cf-auth",
                "",
                "--urls",
                "",
                "--tags",
                "",
                "--hosts",
                "",
                "--prefixes",
                "",
            ]
        )

    with pytest.raises(Exception):
        run_command(
            [
                "--cf-zone",
                "",
                "--cf-auth",
                "key123",
                "--urls",
                "",
                "--tags",
                "",
                "--hosts",
                "",
                "--prefixes",
                "",
            ]
        )


def test_legacy_missing():
    # test missing authentication
    os.environ["CLOUDFLARE_AUTH_KEY"] = "key123"
    with pytest.raises(Exception):
        run_command(
            [
                "--cf-zone",
                "",
                "--cf-auth",
                "",
                "--urls",
                "",
                "--tags",
                "",
                "--hosts",
                "",
                "--prefixes",
                "",
            ]
        )
    del os.environ["CLOUDFLARE_AUTH_KEY"]

    os.environ["CLOUDFLARE_ZONE"] = "zone123"
    with pytest.raises(Exception):
        run_command(
            [
                "--cf-zone",
                "",
                "--cf-auth",
                "",
                "--urls",
                "",
                "--tags",
                "",
                "--hosts",
                "",
                "--prefixes",
                "",
            ]
        )
    del os.environ["CLOUDFLARE_ZONE"]

    with pytest.raises(Exception):
        run_command(
            [
                "--cf-zone",
                "",
                "--cf-auth",
                "",
                "--urls",
                "",
                "--tags",
                "",
                "--hosts",
                "",
                "--prefixes",
                "",
            ]
        )


def test_mix():
    # test mixing authentication between new and old
    os.environ["CLOUDFLARE_AUTH_KEY"] = "key123"

    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "",
            "--urls",
            "",
            "--tags",
            "",
            "--hosts",
            "",
            "--prefixes",
            "",
        ]
    )
    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"purge_everything": True}

    del os.environ["CLOUDFLARE_AUTH_KEY"]

    os.environ["CLOUDFLARE_ZONE"] = "zone123"

    url, headers, data = run_command(
        [
            "--cf-zone",
            "",
            "--cf-auth",
            "key123",
            "--urls",
            "",
            "--tags",
            "",
            "--hosts",
            "",
            "--prefixes",
            "",
        ]
    )
    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"purge_everything": True}

    del os.environ["CLOUDFLARE_ZONE"]


def test_urls():
    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "key123",
            "--urls",
            "nathanv.me google.com",
            "--tags",
            "",
            "--hosts",
            "",
            "--prefixes",
            "",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"files": ["nathanv.me", "google.com"]}


def test_tags():
    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "key123",
            "--urls",
            "",
            "--tags",
            "tag1 tag-2",
            "--hosts",
            "",
            "--prefixes",
            "",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"tags": ["tag1", "tag-2"]}


def test_hosts():
    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "key123",
            "--urls",
            "",
            "--tags",
            "",
            "--hosts",
            "nathanv.me google.com",
            "--prefixes",
            "",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"hosts": ["nathanv.me", "google.com"]}


def test_prefixes():
    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "key123",
            "--urls",
            "",
            "--tags",
            "",
            "--hosts",
            "",
            "--prefixes",
            "nathanv.me/assets https://google.com/images",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"prefixes": ["nathanv.me/assets", "https://google.com/images"]}


def test_purge_everything():
    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "key123",
            "--urls",
            "",
            "--tags",
            "",
            "--hosts",
            "",
            "--prefixes",
            "",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"purge_everything": True}


def test_full():
    # test full options suite
    url, headers, data = run_command(
        [
            "--cf-zone",
            "zone123",
            "--cf-auth",
            "key123",
            "--urls",
            "nathanv.me google.com",
            "--tags",
            "tag1 tag-2",
            "--hosts",
            "nathanv.me google.com",
            "--prefixes",
            "nathanv.me/assets https://google.com/images",
        ]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {
        "files": ["nathanv.me", "google.com"],
        "tags": ["tag1", "tag-2"],
        "hosts": ["nathanv.me", "google.com"],
        "prefixes": ["nathanv.me/assets", "https://google.com/images"],
    }


def test_cli():
    # test cli with arguments missing
    url, headers, data = run_command(["--cf-zone", "zone123", "--cf-auth", "key123"])
    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"purge_everything": True}

    url, headers, data = run_command(
        ["--cf-zone", "zone123", "--cf-auth", "key123", "--tags", "tag1", "tag-2"]
    )

    assert url == "https://api.cloudflare.com/client/v4/zones/zone123/purge_cache"
    assert headers["Authorization"] == "Bearer key123"
    assert data == {"tags": ["tag1", "tag-2"]}
