# -*- coding: utf-8 -*-

from command.ICommand import ICommand


class RunCodeReviewCommand(ICommand):

    def exec(self, *args, **kwargs):
        print('Run Code Review Command')

