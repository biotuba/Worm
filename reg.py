#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

s = "日期：2019-11-30"
#s = "aecde"
print(re.search("\d{4}-\d{2}-\d{2}", s).group())
