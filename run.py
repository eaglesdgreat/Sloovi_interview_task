from distutils.log import debug
import os
from application import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
    