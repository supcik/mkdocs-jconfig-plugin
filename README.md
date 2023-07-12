# mkdocs-jconfig-plugin

This MkDocs plugin allows to process configuration variables using [Jinja](https://jinja.palletsprojects.com/) templates.

## Installation

Install the package with pip:

```bash
pip install mkdocs-jconfig-plugin
```

Activate the plugin in `mkdocs.yml`:

```yaml
plugins:
  - search
  - calendar
  - jconfig
```

## Configuration

The plugin can be configured in the `plugins` section of `mkdocs.yml` as follows:

```yaml
plugins:
  - search
  - calendar
  - jconfig:
      items:
        - copyright
```

The plugin supports the following configuration options:

| Option  | Description                                               |
|---------|-----------------------------------------------------------|
| `items` | The configuration variables to process. Defaults to `[]`. |

## Typical usage

This plugin is useful when you want to automatically adjust the year in the copyright:

```yaml
copyright: copyright {{ cal.today.year }} The Authors

plugins:
  - search
  - calendar
  - jconfig:
      items:
        - copyright
```

Note that you need to activate the [calendar](https://github.com/supcik/mkdocs-calendar-plugin) plugin for this to work.
