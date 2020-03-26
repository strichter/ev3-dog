###############################################################################
# SPDX-License-Identifier: MIT
# Copyright 2020 by EV3 Robo Dog Authros
###############################################################################
"""Simple console/debugger/shell for Micropython."""
import sys
from pybricks import tools

def console(ns):
    while True:
        try:
            cmd = input('>>> ')
        except KeyboardInterrupt:
            break
        try:
            res = eval(cmd, ns, globals())
        except Exception as err:
            sys.print_exception(err)
            tools.print(err)
        else:
            tools.print(res)
