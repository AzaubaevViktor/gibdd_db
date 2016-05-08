#!/usr/bin/env python3.4
import sys
# Иначе не запускается(
sys.path.append('./server')

from server import app


app.run("0.0.0.0", port=1488)
