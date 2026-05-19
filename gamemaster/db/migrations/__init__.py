"""Migrations Package.

All files in here should follow the format `<timestamp>_<task>.py`, and include a function inside
called `migration` that accepts only one argument of type `playhouse.migrate.SqliteMigrator`.

An example:
```
# in `202605182231_test.py`

from playhouse.migrate import migrate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playhouse.migrate import SqliteMigrator


def migration(migrator: "SqliteMigrator"):
    migrate(
        migrator.add_column(...)
    )
```
"""