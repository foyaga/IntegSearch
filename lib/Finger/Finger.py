#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.Finger.lib.checkenv import CheckEnv
from lib.Finger.lib.req import Request
from lib.Finger.lib.output import Output
from lib.Finger.lib.ipAttributable import IpAttributable
from colorama import init as wininit
from lib.Finger.lib.options import initoptions
wininit(autoreset=True)

def main(urls, output):
    CheckEnv()
    initoptions(urls)
    Request()
    IpAttributable()
    Output(output)




