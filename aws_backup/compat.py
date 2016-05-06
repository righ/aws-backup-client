# coding: utf-8

try:
    from dateutil.relativedelta import relativedelta as timedelta
except ImportError:
    from datetime import timedelta
