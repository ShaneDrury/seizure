Seizure: Download Twitch VODs
=============================
.. image:: https://travis-ci.org/ShaneDrury/seizure.svg?branch=master
    :target: https://travis-ci.org/ShaneDrury/seizure
    
Seizure is a library that facilitates downloading Twitch VODs. 

.. code-block:: bash

    $ seizure <video_code> --config config.ini
    
Installation
------------
To install Seizure, simply:

.. code-block:: bash

    $ mkvirtualenv seizure
    $(seizure) pip install seizure

Usage
-----
.. code-block:: bash

    $ workon seizure
    $(seizure) seizure 608495073
