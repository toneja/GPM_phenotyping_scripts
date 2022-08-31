from distutils.core import setup
import py2exe

setup(
    console=["analyze_results.py"],
    zipfile = None,
    options = {
        "py2exe": {
            "optimize": 2,
            "bundle_files": 1,
            "compressed": True,
        }
    },
)
