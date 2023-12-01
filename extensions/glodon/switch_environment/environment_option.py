# -*- coding: utf-8 -*-

__all__ = ['EnvironmentOption']

from typing import Any

from extensions.glodon.environment import Environment


class EnvironmentOption(object):

    def __init__(self, env: Environment, name: str, enabled: bool):
        self.environment: Environment = env
        self.name: str = name
        self.enabled: bool = enabled

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EnvironmentOption):
            return False
        return self.environment == other.environment and self.name == other.name and self.enabled == other.enabled
