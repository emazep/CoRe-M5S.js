#!/usr/bin/env python3
"""
Compresses tirendiconto data.
First download tirendiconto data via M5S_get_restitution.py
(into, let's say, 2017-12-05_tirendiconto.json),
then use this script like this:
$ cat 2017-12-07_tirendiconto.json | python3 compress_tirendiconto_data.py > 2017-12-07_tirendiconto.min.js
"""

import sys
import json

tirendiconto_full_data_py = json.loads( sys.stdin.read() )

out_data = {}

for user, user_data in tirendiconto_full_data_py.items():
    out_data[user] = {}
    for month, month_data in user_data.items():
        out_data[user][month] = (
            month_data['totale_restituito']   ,
            month_data['stipendio']           ,
            month_data['stipendio_restituito'],
            month_data['rimborso']            ,
            month_data['rimborso_restituito'] ,
            month_data['presuntivo']
        )

print( json.dumps(out_data) )
