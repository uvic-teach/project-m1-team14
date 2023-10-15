#!/bin/sh
rq worker --with-scheduler -u redis://cache &
python __main__.py
