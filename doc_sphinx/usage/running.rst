.. _running:

Running
=======

In this section, we summarize the ways in which Crowdsourcr can be
invoked on both Linux and Windows.  Some of the basics are already
described in the :ref:`installation` section.

The Crowdsourcr program is in the ``src`` directory and is invoked by
::

  python app.py [options]

where ``python`` may be ``python3`` if Python 2 is also installed. Note, that Crowdsourcr only runs under Python 3.

This is a description of the options ``app.py`` accepts:

--config=CONFIG_FILENAME  Filename for JSON file that contains the basic configuration settings such as Google authentication, AWS key and secret, port and database. Default is ``config.json``.
--environment=MODE  Options are ``development`` and ``production``.
                    When in ``development`` (the default), HITs are
                    posted to Amazon's sandbox.
--drop=REALLYREALLY  This clears all of the data in the databases.
                     Crowdsourcr will quit immediately after this
                     operation.  ``REALLYREALLY`` should be the
                     literal string ``REALLYREALLY``.
--daemonize=BOOL  Options are either ``True`` or ``False``, defaults to ``False``.
                  This only works in Linux, and it runs Crowdsourcr
                  in the background.  It will kill other daemonized
                  Crowdsourcr instances running on the same port.
                  The log is stored in ``log/tornado.PORTNUM.log``.

Daemonizer
----------

The daemonizer works only under Linux.  It manages instances described
in ``config/daemons_config.py`` running as a background process.  A
benefit for running Crowdsourcr as a background process is that there
is no need to fuss with multiple ``screen`` sessions for each process
in a load-balanced set and that it stores the log in the filesystem.

The ``./daemons`` script manages the daemons.  When run by itself, it
provides a description of its options.  A few useful ways to invoke it
include:

``./daemons list``
  Prints a description of all the daemon configurations in
  ``config/daemons_config.py``.

``./daemons start DAEMON_NAME``
  Starts or restarts the daemon ``DAEMON_NAME``.  Be aware that if two
  daemon configurations have overlapping port numbers that this may
  have unexpected behavior.  See the description of ``--daemonize``
  for more information.

``./daemons stop DAEMON_NAME``
  Makes sure that the daemon ``DAEMON_NAME`` is no longer running.

Windows Batch File
------------------

There is an example batch file in the root of the project called
``start_a.bat``.  It is designed for use with the nginx configuration
given above.  The batch file starts two Command Prompt windows, each
with a running Crowdsourcr instance on a different port, one of which
being responsible for payments.
