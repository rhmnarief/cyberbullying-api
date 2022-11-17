# Project Flask MVC

__author__ = "Muhammad Arief"
__version__ = "1"
__email__ = "rhmnarief8@gmail.com"

from project import app

if __name__ == 'project':
    app.run(host="localhost", port=8000, debug=True)
