# -*- coding: utf-8 -*-

__all__ = ['EventHandlerManager', 'get_event_handler_manager']

from typing import List

from .event_handler import EventHandler


class EventHandlerManager(object):

    def __init__(self):
        # application

        self.__application_will_init_event_handlers: List[EventHandler] = list()
        self.__application_did_init_event_handlers: List[EventHandler] = list()

        self.__application_will_exec_event_handlers: List[EventHandler] = list()
        self.__application_did_exec_event_handlers: List[EventHandler] = list()

        # main window

        self.__main_window_will_init_event_handlers: List[EventHandler] = list()
        self.__main_window_did_init_event_handlers: List[EventHandler] = list()

        # quick launcher

        self.__quick_launcher_will_init_event_handlers: List[EventHandler] = list()
        self.__quick_launcher_did_init_event_handlers: List[EventHandler] = list()

        # system tray icon

        self.__system_tray_icon_will_init_event_handlers: List[EventHandler] = list()
        self.__system_tray_icon_did_init_event_handlers: List[EventHandler] = list()

        self.__system_tray_icon_will_show_event_handlers: List[EventHandler] = list()
        self.__system_tray_icon_did_show_event_handlers: List[EventHandler] = list()

        # extensions

        self.__extensions_will_load_event_handlers: List[EventHandler] = list()
        self.__extensions_did_load_event_handlers: List[EventHandler] = list()

    @staticmethod
    def exec_event_handlers(event_handlers: List[EventHandler], *args, **kwargs):
        for event_handler in event_handlers:
            event_handler.exec(*args, **kwargs)

    # register event handler

    def add_application_will_init_event_handler(self, event_handler: EventHandler):
        self.__application_will_init_event_handlers.append(event_handler)

    def add_application_did_init_event_handler(self, event_handler: EventHandler):
        self.__application_did_init_event_handlers.append(event_handler)

    def add_application_will_exec_event_handler(self, event_handler: EventHandler):
        self.__application_will_exec_event_handlers.append(event_handler)

    def add_application_did_exec_event_handler(self, event_handler: EventHandler):
        self.__application_did_exec_event_handlers.append(event_handler)

    def add_main_window_will_init_event_handler(self, event_handler: EventHandler):
        self.__main_window_will_init_event_handlers.append(event_handler)

    def add_main_window_did_init_event_handler(self, event_handler: EventHandler):
        self.__main_window_did_init_event_handlers.append(event_handler)

    def add_quick_launcher_will_init_event_handler(self, event_handler: EventHandler):
        self.__quick_launcher_will_init_event_handlers.append(event_handler)

    def add_quick_launcher_did_init_event_handler(self, event_handler: EventHandler):
        self.__quick_launcher_did_init_event_handlers.append(event_handler)

    def add_system_tray_icon_will_init_event_handler(self, event_handler: EventHandler):
        self.__system_tray_icon_will_init_event_handlers.append(event_handler)

    def add_system_tray_icon_did_init_event_handler(self, event_handler: EventHandler):
        self.__system_tray_icon_did_init_event_handlers.append(event_handler)

    def add_system_tray_icon_will_show_event_handler(self, event_handler: EventHandler):
        self.__system_tray_icon_will_show_event_handlers.append(event_handler)

    def add_system_tray_icon_did_show_event_handler(self, event_handler: EventHandler):
        self.__system_tray_icon_did_show_event_handlers.append(event_handler)

    def add_extensions_will_load_event_handler(self, event_handler: EventHandler):
        self.__extensions_will_load_event_handlers.append(event_handler)

    def add_extensions_did_load_event_handler(self, event_handler: EventHandler):
        self.__extensions_did_load_event_handlers.append(event_handler)

    # execute event handlers

    def application_will_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__application_will_init_event_handlers, *args, **kwargs)

    def application_did_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__application_did_init_event_handlers, *args, **kwargs)

    def application_will_exec(self, *args, **kwargs):
        self.exec_event_handlers(self.__application_will_exec_event_handlers, *args, **kwargs)

    def application_did_exec(self, *args, **kwargs):
        self.exec_event_handlers(self.__application_did_exec_event_handlers, *args, **kwargs)

    def main_window_will_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__main_window_will_init_event_handlers, *args, **kwargs)

    def main_window_did_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__main_window_did_init_event_handlers, *args, **kwargs)

    def quick_launcher_will_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__quick_launcher_will_init_event_handlers, *args, **kwargs)

    def quick_launcher_did_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__quick_launcher_did_init_event_handlers, *args, **kwargs)

    def system_tray_icon_will_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__system_tray_icon_will_init_event_handlers, *args, **kwargs)

    def system_tray_icon_did_init(self, *args, **kwargs):
        self.exec_event_handlers(self.__system_tray_icon_did_init_event_handlers, *args, **kwargs)

    def system_tray_icon_will_show(self, *args, **kwargs):
        self.exec_event_handlers(self.__system_tray_icon_will_show_event_handlers, *args, **kwargs)

    def system_tray_icon_did_show(self, *args, **kwargs):
        self.exec_event_handlers(self.__system_tray_icon_did_show_event_handlers, *args, **kwargs)

    def extensions_will_load(self, *args, **kwargs):
        self.exec_event_handlers(self.__extensions_will_load_event_handlers, *args, **kwargs)

    def extensions_did_load(self, *args, **kwargs):
        self.exec_event_handlers(self.__extensions_did_load_event_handlers, *args, **kwargs)


__event_handler_manager = EventHandlerManager()


def get_event_handler_manager() -> EventHandlerManager:
    return __event_handler_manager
