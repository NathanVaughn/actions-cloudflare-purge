# Cloudflare Cache Purge Action

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This action uses Cloudflare's API to purge their
[cache](https://api.cloudflare.com/#zone-purge-all-files) of your site.

## Inputs

You can mix and match the various inputs however you want
(other than the zone and auth key). If you don't provide
`files` or `tags` or `hosts` or `prefixes`, then all files will be purged.

### `cf_zone` or `CLOUDFLARE_ZONE` environment variable

The zone ID of your Cloudflare site. Example:

```text
023e105f4ecef8ad9ca31a8372d0c353
```

### `cf_auth` or `CLOUDFLARE_AUTH_KEY` environment variable

The Cloudflare API key you've generated for your zone. Example:

```text
c2547eb745079dac9320b638f5e225cf483cc5cfdda41
```

### `files` (optional)

A space seperated list of URLs to purge. Example:

```yml
files: https://nathanv.me/assets/images/profile.png https://nathanv.me/assets/images/favicons/apple-touch-icon.png
```

The key `urls` is also accepted for backwards compatibility.

### `tags` (optional)

A space seperated list of tags to purge. Example:

```yml
tags: some-tag another-tag
```

### `hosts` (optional)

A space seperated list of hosts to purge. Example:

```yml
hosts: nathanv.me blog.nathanv.me
```

### `prefixes` (optional)

A space seperated list of prefixes to purge. Example:

```yml
prefixes: nathanv.me/assets/ blog.nathanv.me/assets
```

## Outputs

None

## Example Usages

```yml
- name: Purge cache
  uses: nathanvaughn/actions-cloudflare-purge@master
  # preferred
  with:
      cf_zone: ${{ secrets.CLOUDFLARE_ZONE }}
      cf_auth: ${{ secrets.CLOUDFLARE_AUTH_KEY }}
```

```yml
- name: Purge cache
  uses: nathanvaughn/actions-cloudflare-purge@master
  # legacy
  env:
      CLOUDFLARE_ZONE: ${{ secrets.CLOUDFLARE_ZONE }}
      CLOUDFLARE_AUTH_KEY: ${{ secrets.CLOUDFLARE_AUTH_KEY }}
```

```yml
- name: Purge cache
  uses: nathanvaughn/actions-cloudflare-purge@master
  with:
      cf_zone: ${{ secrets.CLOUDFLARE_ZONE }}
      cf_auth: ${{ secrets.CLOUDFLARE_AUTH_KEY }}
      files: |
         https://nathanv.me/assets/images/profile.png
         https://nathanv.me/assets/images/favicons/apple-touch-icon.png
      tags: |
         some-tag
         another-tag
      hosts: |
         nathanv.me
         blog.nathanv.me
      prefixes: |
         nathanv.me/assets/
         blog.nathanv.me/assets
```

## Getting Cloudflare Info

1. First, go to the [API tokens page](https://dash.cloudflare.com/profile/api-tokens)
   in your Cloudflare account.

![](images/api-tokens.jpg)

2. Click "Create Token", and fill out the form. Make sure to give the permission of
   zone cache purge.

![](images/token-creation.jpg)

3. Click "Continue to summary", then "Confirm".

4. Copy the value of the token.

![](images/copy-token.jpg)

5. To find the zone ID for your site, go to your dashboard for the site, and look on the
   right-hand panel.

![](images/zone-id.jpg)

Follow GitHub's [documentation](https://help.github.com/en/articles/virtual-environments-for-github-actions#creating-and-using-secrets-encrypted-variables)
to add these values to your repository's secrets.

![](images/secrets.jpg)
