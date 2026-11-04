# Beeper bridges on Unraid

Run official self-hosted Beeper bridges on Unraid. Each bridge is its own container, using Beeper's image `ghcr.io/beeper/bridge-manager:latest`. This repo does not build that image.

Self-hosting is outside normal Beeper support. For help, use the docs at https://developers.beeper.com/bridges/self-hosting/ or the Matrix room `#self-hosting:beeper.com`.

## Access token

Paste a Beeper access token into the template. Copy it from either place:

- Beeper Desktop: Settings, Help and About.
- After `bbctl login` on another machine: the `access_token` field in `~/.config/bbctl/config.json`.

The copy of `beeper-bridge.xml` in this repo leaves the token empty. Unraid stores the value you enter on the flash drive.

Changing the token in the container settings applies the next time that container starts.

## Supported bridges

Set **Bridge Name** to `sh-` plus an id from this table. A name that contains the id is enough. Examples: `sh-whatsapp`, `sh-telegram`, `sh-signal`.

| Bridge | Identifier |
| --- | --- |
| Telegram | `telegram` |
| WhatsApp | `whatsapp` |
| Signal | `signal` |
| Discord | `discord` |
| Slack | `slack` |
| Google Messages | `gmessages`, `googlemessages`, `rcs`, `sms` |
| Google Voice | `gvoice`, `googlevoice` |
| Meta (Facebook and Instagram) | `meta`, `instagram`, `facebook` |
| Google Chat | `googlechat`, `gchat` |
| X | `twitter` |
| Bluesky | `bluesky`, `bsky` |
| LinkedIn | `linkedin` |
| IRC (Heisenbridge) | `heisenbridge`, `irc` |

iMessage and iMessage Go are not supported by this template. On Linux they ask for a BlueBubbles address and password, or for an iMessage registration code. The official image does not forward extra arguments, so those prompts cannot be answered here.

## Install

1. Copy `beeper-bridge.xml` to `/boot/config/plugins/dockerMan/templates-user/` on the Unraid flash drive.
2. In the Unraid Docker tab, add a container and choose the `beeper-bridge` template.
3. Set the bridge name and paste the access token. Leave the appdata path at `/mnt/user/appdata/beeper-bridge` for the first bridge.
4. Apply.
5. Enable autostart for the container in the Docker tab. The template does not turn autostart on. Autostart brings the bridge back after a reboot.

The first start needs outbound internet. `bbctl` downloads that bridge's program into the appdata folder.

When the container is running, message the bridge bot in Beeper and follow its instructions. The WhatsApp bot is `@sh-whatsappbot:beeper.local`. Other bridges use `@` plus the bridge name plus `bot:beeper.local`.

The container runs as the image's default user. There is no PUID or PGID setting.

## Add another bridge

Add the `beeper-bridge` template again. Set a new container name and a new bridge name. Keep the appdata path at `/mnt/user/appdata/beeper-bridge`.

Every bridge container uses that same folder. `bbctl` separates them inside it:

- `/data/sh-whatsapp` holds that bridge's config, logs, and a Python virtualenv when the bridge needs one.
- `/data/db` holds database files. Names start with the bridge name, such as `sh-whatsapp-`.
- `/data/binaries` holds downloaded bridge programs shared by every container using this folder.

Two containers may use this same folder only when their bridge names differ. Two containers both set to `sh-whatsapp` would write the same files.

## Remove a bridge

1. Open the container console in Unraid and run `bbctl delete sh-<name>`. Confirm the prompt. This deletes the bridge on Beeper's servers and removes `/data/sh-<name>`.
2. Delete files in `/data/db` whose names start with `sh-<name>-`. `bbctl delete` does not remove those files. Starting that bridge name again reuses them and produces errors.
3. Remove the container in the Unraid Docker tab.

Removing the container alone leaves the bridge registered on Beeper and leaves its files in appdata. Deleting the bridge from the Beeper client leaves the local database in place.

## When the container stops

- `BRIDGE_NAME not set` means the bridge name field is empty.
- `MATRIX_ACCESS_TOKEN not set` means the token field is empty.
- A rejected token fails while `bbctl` checks the account. The Unraid log shows the `bbctl` error.
- A bridge removed on Beeper while its database remains under `/data/db` will reuse that database the next time the same bridge name starts. Remove `/data/sh-<name>` and the matching `/data/db/sh-<name>-` files first.
