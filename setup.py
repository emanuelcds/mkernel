from distutils.core import setup

import py2exe, os, _mssql, pymssql
import decimal, uuid

data_files = []
data_files.append(os.path.join(os.path.split(pymssql.__file__)[0], 'ntwdblib.dll'))
py2exe_options = {"py2exe":{"includes": ['decimal', 'uuid', '_mssql'],
                "dll_excludes":["mswsock.dll",
                "powrprof.dll",
                "user32.dll",
                "shell32.dll",
                "wsock32.dll",
                "advapi32.dll",
                "kernel32.dll",
                "ntwdblib.dll",
                "ws2_32.dll",
                "oleaut32.dll",
                "ole32.dll",
                            ],
}}

setup(console=["app.py"], options=py2exe_options)


