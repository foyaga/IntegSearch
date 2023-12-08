#!/usr/bin/env python
# -*- coding: utf-8 -*-
from colorama import init as wininit

from module.Finger.lib.checkenv import CheckEnv
from module.Finger.lib.ipAttributable import IpAttributable
from module.Finger.lib.options import initoptions
from module.Finger.lib.output import Output
from module.Finger.lib.req import Request

wininit(autoreset=True)


def main(urls, output):
    #CheckEnv()
    initoptions(urls)
    Request()
    IpAttributable()
    Output(output)
