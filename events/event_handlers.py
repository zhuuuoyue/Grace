# -*- coding: utf-8 -*-

__all__ = [
    'ApplicationWillInit', 'ApplicationDidInit', 'ApplicationWillExec', 'ApplicationDidExec',
    'MainWindowWillInit', 'MainWindowDidInit',
    'QuickLauncherWillInit', 'QuickLauncherDidInit',
    'SystemTrayIconWillInit', 'SystemTrayIconDidInit', 'SystemTrayIconWillShow', 'SystemTrayIconDidShow',
    'ExtensionsWillLoad', 'ExtensionsDidLoad'
]

from abc import abstractmethod
from typing import NoReturn

from .event_handler import EventHandler
from .event_handler_manager import get_event_handler_manager


class ApplicationWillInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_application_will_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class ApplicationDidInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_application_did_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class ApplicationWillExec(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_application_will_exec_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class ApplicationDidExec(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_application_did_exec_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class MainWindowWillInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_main_window_will_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class MainWindowDidInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_main_window_did_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class QuickLauncherWillInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_quick_launcher_will_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class QuickLauncherDidInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_quick_launcher_did_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class SystemTrayIconWillInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_system_tray_icon_will_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class SystemTrayIconDidInit(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_system_tray_icon_did_init_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class SystemTrayIconWillShow(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_system_tray_icon_will_show_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class SystemTrayIconDidShow(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_system_tray_icon_did_show_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class ExtensionsWillLoad(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_extensions_will_load_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass


class ExtensionsDidLoad(EventHandler):

    def __init__(self):
        super().__init__()
        get_event_handler_manager().add_extensions_did_load_event_handler(self)

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass
