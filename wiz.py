#!env/bin/python
# -*- coding: utf8 -*-
import sys
from wiz import app

if len(sys.argv)>1:
    port = int(sys.argv[1])
else:
    port=5000
app.run(debug=True, host='0.0.0.0',port=port)

