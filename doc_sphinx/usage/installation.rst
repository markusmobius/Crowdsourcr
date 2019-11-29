.. _installation:

Installation
============

Crowdsourcer is a Python_ program that uses MongoDB_ and the Tornado_
library.  Optionally, it may use nginx_ for load balancing across
multiple processes and for serving static content.

.. _Python: https://www.python.org/
.. _MongoDB: http://www.mongodb.org/
.. _Tornado: https://www.tornadoweb.org/
.. _nginx: http://nginx.org/

Linux
-----

For these installation instructions, we will assume an Ubuntu
installation.

Make sure that Python 3 and ``pip`` are installed.

Then, either install the requirements as described in
``requirements.txt`` (and possibly update the version numbers), or
just run
::

  sudo pip install -r requirements.txt

Make sure MongoDB_ is installed and running. If it is not, follow the
instructions at 
`<http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/>`_.

To set up Crowdsourcer itself, copy ``config/app_config.py.example``
to ``config/app_config.py`` and modify the settings.  Crowdsourcer
uses Google OAuth2 for authentication, so you need to get Google
OAuth2 keys from their `developer console
<https://console.developers.google.com/>`_.  The configuration file
(or `Google configuration`_ below) has more details about this.  Put
your Google account into the list of superadmins so that you can
administrate the administrators for Crowdsourcer.

At this point, it should be possible to start Crowdsourcer by entering
the `src` directory and running
::

 python app.py --port=80 --environment=production

and then going to ``http://YOUR.DOMAIN/admin``.  You will probably
need to allow access to port 80 using the following command:
::

 sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

and then instead run
::

 python app.py --port=8080 --environment=production

On Linux, we support starting Crowdsourcer as a daemon.  For this to
work, copy ``config/daemons_config.py.example`` to
``config/daemons_config.py`` and add an entry to the daemons list
describing on which port(s) you want Crowdsourcer to run (or just use
the ``default`` configuration already provided).  Make sure that the
Python package ``python-daemon``, as described in
``requirements.txt``, is installed, as this is a requirement for
daemonization. Crowdsourcer can be started with ``./daemons start
CONFIGNAME`` or stopped with ``./daemons stop CONFIGNAME``.  You can
get help for these commands with ``./daemons help``.

While this is already sufficient for using Crowdsourcer, we recommend
using nginx_ for serving static content and load balancing across
multiple Python processes.  We already have a daemon configuration
called ``a`` which assumes nginx is set up as a load-balancing proxy.
To be able to use it, first ``sudo apt-get install nginx``.  Then
create a new file called ``/etc/nginx/sites-available/crowdsourcer-a``
with the following content:
::

 upstream crowdsourcer_a {
          server 127.0.0.1:8101;
          server 127.0.0.1:8102;
 }
 
 server {
        charset uft-8;
 
        include mime.types;
        listen 80;
        server_name www.crowdsourcr.org; # REPLACE THIS APPROPRIATELY
 
        client_max_body_size 30m;
 
        location ^~  {
                 expires max;
                 add_header Cache-Control public;
                 root /home/kmill/news_crowdsourcer; # REPLACE THIS APPROPRIATELY
        }
 
        location ~ /.* {
                 proxy_pass_header Server;
                 proxy_set_header Host $http_host;
                 proxy_connect_timeout 3600;
                 proxy_send_timeout 3600;
                 proxy_read_timeout 3600;
                 send_timeout 3600;
                 proxy_buffering off;
                 proxy_redirect off;
                 proxy_set_header X-Real-IP $remote_addr;
                 proxy_set_header X-Scheme $scheme;
                 proxy_pass http://crowdsourcer_a;
        }
 }

Next, run the following command to enable this configuration for
nginx:
::

  sudo ln -s /etc/nginx/sites-available/crowdsourcer-a /etc/nginx/sites-enabled/crowdsourcer-a

and reload nginx:
::

  sudo service nginx reload

From the Crowdsourcer directory, you can start up the ``a``
configuration with
::

  ./daemons start a

This completes the Linux installation.

Windows
-------

First, you will need to download the Crowdsourcer application and put
it somewhere such as ``C:/news_crowdsourcer``.  Depending on the
location of the Crowdsourcer repository, it may be helpful to first
install git_ for windows.

.. _git: http://git-scm.com/

It may be necessary to open port 80 in the Windows firewall, when
using Windows Server for instance.  See
http://windows.microsoft.com/en-us/windows/open-port-windows-firewall
for guidance.

Install Python 3.  Make sure and enable the setting to place Python
in the system path.  Otherwise, you will need to modify the
Crowdsourcer startup script with the location of your Python.

Install the Python packaging system pip_.  You will be running
``python get-pip.py``, which is a good test of your python
installation, too.

.. _pip: https://pip.pypa.io/en/latest/installing.html

With pip installed, now Python libraries may be installed:
::

 pip install tornado
 pip install pymongo
 pip install boto3
 pip install docutils
 pip install validators
 pip install future-fstrings
 pip install jsonpickle
 pip install xmltodict

Install MongoDB_.  To set up the database, go into Mongo's ``bin``
directory with the command promt and run
::

 md \data\db

After this, you need to start ``mongod``, which is also in the ``bin``
directory.

To set up Crowdsourcer itself, copy ``config/app_config.py.example``
to ``config/app_config.py`` and modify the settings.  Crowdsourcer
uses Google OAuth2 for authentication, so you need to get Google
OAuth2 keys from their `developer console
<https://console.developers.google.com/>`_.  The configuration file
(or `Google configuration`_ below) has more details about this.  Put
your Google account into the list of superadmins so that you can
administrate the administrators for Crowdsourcer.

At this point, it should be possible to start Crowdsourcer by entering
the `src` directory and running
::

 python app.py --port=80 --environment=production

and then going to ``http://YOUR.DOMAIN/admin``.

However, it is better to be using nginx as a proxy for load balancing
and for serving static content.

Download a zip package of nginx_ for Windows and unzip it into a
directory such as ``C:/nginx`` (we will assume this is where you
placed it for the rest of the guide).  Then, open
``C:/nginx/conf/nginx.conf`` and replace the server directive with the
following (modifying the marked things appropriately):
::

 upstream crowdsourcer_a {
          server 127.0.0.1:8101;
          server 127.0.0.1:8102;
 }
 
 server {
        charset uft-8;
 
        include mime.types;
        listen 80;
        server_name www.crowdsourcr.org; # REPLACE THIS APPROPRIATELY
 
        client_max_body_size 30m;
 
        location ^~  {
                 expires max;
                 add_header Cache-Control public;
                 root C:/news_crowdsourcer; # REPLACE THIS APPROPRIATELY
        }
 
        location ~ /.* {
                 proxy_pass_header Server;
                 proxy_set_header Host $http_host;
                 proxy_connect_timeout 3600;
                 proxy_send_timeout 3600;
                 proxy_read_timeout 3600;
                 send_timeout 3600;
                 proxy_buffering off;
                 proxy_redirect off;
                 proxy_set_header X-Real-IP $remote_addr;
                 proxy_set_header X-Scheme $scheme;
                 proxy_pass http://crowdsourcer_a;
        }
 }

To start nginx, run ``start nginx`` from the nginx directory (and see
http://nginx.org/en/docs/windows.html for more information about
reloading or stopping nginx)

Then, with nginx set up like this, running ``start_a.bat`` from the
Crowdsourcer package will start up two processes in two windows.

This completes the Windows installation.

.. _google configuration:

Google configuration
--------------------

This was briefly described in each of these sections, but it may be
useful if the details are elaborated upon here.  Crowdsourcer uses
OAuth2 for authentication.  This means that you need to have a Google
account to administer your Crowdsourcer installation and that you need
an OAuth client ID from Google.

There is a brief description for getting the OAuth client ID in
``config/app_config.py``.  In detail, first go to
https://console.developers.google.com and create a new project.  It
does not matter what it is called.  Once this is created, go to
"Credentials."  There should be a button which says
"Create Credentials". Click it, then select "OAuth Client ID". You will
be prompted to first set up your OAuth consent screen. Enter the minimal
amount of information that will let you pass to the next screen. On
the next screen select "Web application", choose a name and click
"Create".  Enter information similar to that in the following image,
replacing the domain appropriately.  Note carefully the trailing
slash in the "Authorized Redirect URI" and the ``http`` rather
than ``https``. Authentication will not work if either of these
are missing.

.. figure:: ../doc_img/crowdsourcer_google_oauth.png
   :alt: Example configuration for an OAuth client id for Crowdsourcer.
   :align: center

After creating the client ID, copy the "Client ID" and "Client secret"
under "Client ID for web application" (and *not* the "Compute Engine
and App Engine") into ``config/app_config.py``.  This should complete
the configuration for Google OAuth2 authentication.