# Shamrock VLT Kernel

This is a simple python subprocess that receive UDP requests on a given configured
port and replies with local database prize pool results.

## Configuring

Just declares the SHAMROCK_KERNEL_PORT environment variable before running it.

## Development

You need the following software installed.
- Python 3.4+
- Python PIP
- [Py2EXE](https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/)

Run the following command to install python requirements:
```
    $ pip install -r requirements.txt
```

After installing python requirements, compile the application by running:
```
    $ python setup.py py2exe
```

It will create a folder named **dist** with the **shamrock-kernel.exe** binary inside.

Enjoy!
