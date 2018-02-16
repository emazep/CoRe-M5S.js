#!/usr/bin/env python3

__author__ = "Emanuele Zeppieri"
__copyright__ = """

    Copyright 2017-2018 Emanuele Zeppieri

    Licensed under the MIT License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       https://opensource.org/licenses/MIT

    This software is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "MIT"
__status__ = "Beta"
__version__ = "0.0.1"

"""
Minifies tirendiconto data.
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

print( "tirendiconto_fulldata =" )
print( json.dumps(out_data) )
