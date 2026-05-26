# Changelog

Details about the changes between verisons.

|      Version     |
|:----------------:|
|[**0.1.0**](#v010)|

<!--hr style="height:2px" /-->
<!--hr style="height:4px" /-->

<hr/>

### v0.1.0

* **Added new dependencies**:
    - `discord.py` (**2.7.1**)
    - `peewee` (**4.0.5**)
    - `peewee-migrate` (**1.15.0**)
    - `Pillow` (**12.2.0**)
    - `emoji` (**2.15.0**)
* **Added dev dependencies**
    - `coverage` (**7.14.0**)
    - `ruff` (**0.15.14**)
* **New ORM style for database** using `peewee`
* **new commands**
    - `/profile`
        * `/profile show`
        * `/profile edit`
    - `/play`
    - `/dev` _(for admin)_
        * `/dev shutdown`
        * `/dev reboot`
        * `/dev reload`
    - `/log` _(for admin)_
        * `/log get`
        * `/log tail`
        * `/log purge`
    - `/about`
* New game "Element Rock-Paper-Scissors"