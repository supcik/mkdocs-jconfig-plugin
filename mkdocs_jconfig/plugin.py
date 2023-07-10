################################################################################
# @brief       : JConfig plugin for MkDocs
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 10. July 2023
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2023 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT OR Apache-2.0
################################################################################

"""JConfig plugin for MkDocs"""

import collections.abc
import logging

import jinja2
from mkdocs.config import config_options as c
from mkdocs.config.base import Config as BaseConfig
from mkdocs.plugins import BasePlugin

logger = logging.getLogger("mkdocs.plugins." + __name__)
TAG = "[jconfig] -"


class JConfigPluginConfig(BaseConfig):
    """Configuration options for the plugin."""

    items = c.Type(list, default=[])


# pylint: disable-next=too-few-public-methods
class JConfigPlugin(BasePlugin[JConfigPluginConfig]):
    """JConfig plugin for MkDocs"""

    def _fix_item(self, key, config, jinja_env):
        subconfig = config
        path = key.split(".")
        for stem in path[:-1]:
            if stem not in subconfig:
                logger.warning("%s Key '%s' not found in config... skipping", TAG, key)
                return
            if not isinstance(subconfig[stem], collections.abc.Mapping):
                logger.warning(
                    "%s - Invalid key '{%s}' [%s]... skipping",
                    TAG,
                    key,
                    type(subconfig[stem]),
                )
                return
            subconfig = subconfig[stem]

        if path[-1] not in subconfig:
            logger.warning("%s - Key '{%s}' not found in config... skipping", TAG, key)
            return

        orig = subconfig[path[-1]]
        template = jinja_env.from_string(orig)

        try:
            res = template.render(config.extra)
            logger.debug("%s - Rendering '%s' -> '%s'", TAG, key, res)
            subconfig[path[-1]] = res
        except jinja2.TemplateError as e:  # pylint: disable=invalid-name
            logger.warning("%s - Failed to render '%s': %s", TAG, key, e)
            subconfig[path[-1]] = orig

    def on_config(self, config):
        """define the today configuration and render the templated options"""
        env = jinja2.Environment()
        for key in self.config.items:
            logger.debug("%s - Fixing %s", TAG, key)
            self._fix_item(key, config, env)

        return config
