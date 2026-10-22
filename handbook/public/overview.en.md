{"title": "CheeseSec Plugins", "linkTitle": "Plugins", "weight": 20}

CheeseSec Plugins is an independent product shared across the CheeseSec ecosystem. It provides a common way to discover and develop plugins.

Each plugin declares its compatible hosts, versions, and capabilities. Check both the plugin description and the host documentation before installing it. A shared catalog does not mean every CheeseSec product supports installation or execution.

## Browse plugins

Visit the [plugin store](https://store.cheesesec.com/) to view published plugins without signing in. Only published entries are available; an example or an empty catalog is not an installable plugin.

Applications can read the [v1 plugin catalog](https://store.cheesesec.com/v1/catalog/index.json) and the [v1 stable update index](https://ota.cheesesec.com/v1/channels/stable/index.json).

## Hello CheeseSec example

`Hello CheeseSec 0.1.0` demonstrates startup, health checks, mode promotion, and shutdown. It does not detect attacks, collect data, or provide protection.

The store offers separate Linux amd64 and macOS arm64 packages. Each requires its matching platform and a compatible CheeseWAF process-plugin host. Other CheeseSec products must implement a compatible host before they can run it. Listing and downloading a package do not imply automatic installation or activation.

Packages carry two Ed25519 signatures. Before installation, check the package SHA-256, signatures, and host requirements. Confirm publisher keys through a trusted channel; downloading a package and its public keys from the same website alone does not establish trust in an unknown publisher.

[Browse and download the example](https://store.cheesesec.com/) · [Download reproducible source](https://res.cheesesec.com/sha256/e088a10aee6e24ca728f15584477a440a35df433e1712dced8671f476aaba4d3/hello-cheesesec-source-0.1.0.tar.gz)

## Develop a plugin

Choose a supported host and follow its package and capability requirements. Include clear compatibility information and usage instructions, and verify the package signature before installation.

For the CheeseWAF host, see its [plugin and CRP documentation](/docs/cheesewaf/plugins/). These host-specific instructions do not establish compatibility with other CheeseSec products.
