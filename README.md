> **This is a fork — a "slim Cospend" on top of IHateMoney.** Stock IHateMoney has no bill
> categories, no payment methods and no repeating bills (categories have been an
> [open request since 2011](https://github.com/spiral-project/ihatemoney/issues/55); the project
> is in maintenance mode). This fork adds them, wire-compatible with Nextcloud Cospend and
> MoneyBuster, and keeps upstream's own test suite green.
>
> **What it adds**
> - `categoryid` on every bill: negative ids = Cospend's built-in global categories (shown by
>   MoneyBuster without any extra endpoint), positive ids = the project's own categories.
> - **Project categories**: `GET/POST /api/projects/<id>/categories`,
>   `GET/PUT/DELETE …/categories/<cid>` (`name`, `icon`, `color`, `order`). Deleting one detaches
>   it from bills.
> - **Payment methods** (`paymentmodeid` on bills, `…/paymentmodes` CRUD). New projects are
>   seeded with Cospend's five defaults.
> - **Repeating bills**: `repeat` (`n d w b s m y`), `repeatfreq`, `repeatuntil`,
>   `repeatallactive` on bills. Due copies are created lazily whenever bills are listed (API or
>   web UI) — the copy inherits the rule, the source stops repeating, like Cospend. Optional
>   cron: `flask --app ihatemoney.wsgi repeat-bills`.
> - **`GET /api/projects/<id>/settle`**: the server's own settlement plan (`ower`, `receiver`,
>   `amount`).
> - The project info (`GET /api/projects/<id>`) lists `categories`, `paymentmodes` and a
>   `features` array (`categoryid categories paymentmodes settle repeat`) so clients can detect
>   the fork.
> - **Web UI**: category and payment-method dropdowns in the bill form, a *Categories* page to
>   manage both (icon, name, color), repeat options under "More options", markers in the bill
>   list.
>
> Built for **[IHM Tracker](https://github.com/modularidea/obsidian-ihm-tracker)**, an Obsidian
> plugin for IHateMoney/Cospend — the plugin works without this fork (categories then live in a
> vault file); with it, categories, payment methods and repeats are shared with every other
> client of the project.
>
> Base commit: `e66a7672e8e5c41549bf53c4a824c72c43ab9079` (upstream `main`, "Back to development:
> 7.2.2"). Upstream's test suite is green (153 passed incl. the fork's own tests, 5 skipped).
>
> **Run it locally:**
> ```bash
> git clone --branch feat/categoryid https://github.com/modularidea/ihatemoney-cat.git
> cd ihatemoney-cat
> docker compose -f docker-compose.fork.yml up --build
> ```
> Builds this checkout (patched code included) instead of pulling the official
> `ihatemoney/ihatemoney` image, and starts it on `http://localhost:8000`.
> `docker-compose.fork.yml` uses the same environment variables as upstream's own
> `docker-compose.yml` example — see
> [the config docs](https://ihatemoney.readthedocs.io/en/latest/configuration.html) for all of
> them. It's a local-dev example (`SECRET_KEY`/`ADMIN_PASSWORD` are placeholders) — set your own
> values before exposing it beyond `localhost`.

---

# I hate money

[![GitHub Actions Status](https://github.com/spiral-project/ihatemoney/actions/workflows/test-docs.yml/badge.svg)](https://github.com/spiral-project/ihatemoney/actions/workflows/test-docs.yml)
[![Translation status from Weblate](https://hosted.weblate.org/widgets/i-hate-money/-/i-hate-money/svg-badge.svg)](https://hosted.weblate.org/engage/i-hate-money/?utm_source=widget)
[![Donate](https://img.shields.io/liberapay/receives/IHateMoney.svg?logo=liberapay)](https://liberapay.com/IHateMoney/donate)
[![Docker image](https://img.shields.io/badge/-Docker%20image-black?logo=docker)](https://hub.docker.com/r/ihatemoney/ihatemoney)

*I hate money* is a web application made to ease shared budget
management. It keeps track of who bought what, when, and for whom; and
helps to settle the bills.

-   [Online documentation](https://ihatemoney.readthedocs.io)
-   [Hosted version](https://ihatemoney.org)
-   [Cloud Providers](https://ihatemoney.readthedocs.io/en/latest/installation.html#cloud)
-   [Mailing
    list](https://mailman.alwaysdata.com/postorius/lists/info.ihatemoney.org/)
    (to get updates when needed).

The code is distributed under a BSD *beerware* derivative: if you meet
the people in person and you want to pay them a craft beer, you are
highly encouraged to do so.

## Requirements


-   **Python**: version 3.11 to 3.13.
-   **Backends**: SQLite, PostgreSQL, MariaDB (version 10.3.2 or above),
    Memory.

Usually, we aim to support the software environment of the current Linux Debian
stable and the previous one (old-stable). Docker installation is offered for
broader support.

## Current direction (as of 2024)

Ihatemoney was started in 2011, and we believe the project has reached a certain
level of maturity now. The overall energy of contributors is not as high as it
used to be.

In addition, there are now several self-hosted alternatives (for instance
[cospend](https://github.com/julien-nc/cospend-nc/tree/main),
[spliit](https://github.com/spliit-app/spliit)).

As maintainers, we believe that the project is still relevant but should gear
towards some kind of "maintenance mode":

* **Simplicity** is now the main goal of the project. It has always been a compass
for the project, and the resulting software is appreciated by both users and
server administrators. For us, "simplicity" is positive and encompasses both
technical aspects (very few javascript code, manageable dependencies, small code
size...) and user-visible aspects (straightforward interface, no need to create
accounts for people you invite, same web interface on mobile...)

* **Stability** is prioritized over adding major new features. We found ourselves
complexifying the codebase (and the interface) while accepting some
contributions. Our goal now is to have a minimal set of features that do most of
the job. We believe this will help lower the maintainance burden.

* **User interface and user experience improvements** are always super welcome !

It is still possible to propose new features, but they should fit into
this new direction. Simplicity of the UI/UX and simplicity of the technical
implementation will be the main factors when deciding to accept new features.

## Contributing

Do you wish to contribute to IHateMoney? Fantastic! There's a lot of
very useful help on the official
[contributing](https://ihatemoney.readthedocs.io/en/latest/contributing.html)
page.

You can also [donate some
money](https://liberapay.com/IHateMoney/donate). All funds will be used
to maintain the [hosted version](https://ihatemoney.org).

**Join the other contributors.**

[![](https://contrib.rocks/image?repo=spiral-project/ihatemoney)](https://github.com/spiral-project/ihatemoney/graphs/contributors)
 
## Translation status

[![Translation status for each language](https://hosted.weblate.org/widgets/i-hate-money/-/i-hate-money/multi-blue.svg)](https://hosted.weblate.org/engage/i-hate-money/?utm_source=widget)
