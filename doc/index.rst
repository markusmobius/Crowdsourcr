============================
 Crowdsourcer Documentation
============================

:Author:
  Kyle Miller
:Modified: June 2014

.. contents:: Table of Contents

Introduction
============

Crowdsourcer is an application for conducting survey-like experiments
online, especially when used in conjunction with Amazon Mechanical
Turk.  It is designed to show some number of questions next to some
document, such as a news article.

The following is an example from one real experiment:

.. figure:: /static/doc_img/crowdsourcer_task_example_news_scaled.png
   :alt: An example task.
   :align: center

Installation
============

Crowdsourcer is a Python_ program that uses MongoDB_ and the Tornado_
library.  Optionally, it may use nginx_ for load balancing across
multiple processes and for serving static content.

.. _Python: https://www.python.org/
.. _MongoDB: http://www.mongodb.org/
.. _Tornado: http://www.tornadowebd.org/
.. _nginx: http://nginx.org/

Linux
-----

For these installation instructions, we will assume an Ubuntu
installation.

Make sure that Python 2.7 and ``pip`` are installed:
::

  sudo apt-get install python2.7 python-pip

Then, either install the requirements as described in
``requirements.txt`` (and possibly update the version numbers), or
just run
::

  sudo pip install -r requirements.txt

Make sure MongoDB_ is installed.  The developers recommend following
`<http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/>`_,
however we have had success with
::

  sudo pip install mongodb

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
 
        location ^~ /static/ {
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

Install Python_ 2.7.  Make sure and enable the setting to place Python
in the system path.  Otherwise, you will need to modify the
Crowdsourcer startup script with the location of your Python.  Make
sure that ``python`` refers to Python 2.7 and not Python 3, otherwise
the software is likely not to work correctly!

Install the Python packaging system pip_.  You will be running
``python get-pip.py``, which is a good test of your python
installation, too.

.. _pip: https://pip.pypa.io/en/latest/installing.html

With pip installed, now Python libraries may be installed:
::

 python -m pip install tornado
 python -m pip install pymongo==2.5.2
 python -m pip install boto
 python -m pip install docutils
 python -m pip install validators==0.11.3

It may be necessary to specify version numbers if Crowdsourcer ends up
not working later.  These commands install the newest versions of
these packages.  For instance:
::

 python -m pip install boto==2.29.1

Look in ``requirements.txt`` for a known set of version numbers that
work.

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
 
        location ^~ /static/ {
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
does not matter what it is called.  Once this is created, go to "APIs
& auth" then "Credentials."  There should be a button which says
"Create new client ID".  Enter information similar to that in the
following image, replacing the domain appropriately.  Note carefully
the trailing slash in the "Authorized Redirect URI" and the ``http``
rather than ``https``.  Authentication will not work if either of
these are missing.

.. figure:: /static/doc_img/crowdsourcer_google_oauth.png
   :alt: Example configuration for an OAuth client id for Crowdsourcer.
   :align: center

After creating the client ID, copy the "Client ID" and "Client secret"
under "Client ID for web application" (and *not* the "Compute Engine
and App Engine") into ``config/app_config.py``.  This should complete
the configuration for Google OAuth2 authentication.

Running
=======

In this section, we summarize the ways in which Crowdsourcer can be
invoked on both Linux and Windows.  Some of the basics are already
described in the Installation_ section.

The Crowdsourcer program is in the ``src`` directory and is invoked by
::

  python app.py [options]

where ``python`` may be ``python2.7`` if Python 3 is also installed.

This is a description of the options ``app.py`` accepts:

--port=NUM  Tells Crowdsourcer which port number to listen on.  Each
            process *must* listen on a different port.
--environment=MODE  Options are ``development`` and ``production``.
                    When in ``development`` (the default), HITs are
                    posted to Amazon's sandbox.
--drop=REALLYREALLY  This clears all of the data in the databases.
                     Crowdsourcer will quit immediately after this
                     operation.  ``REALLYREALLY`` should be the
                     literal string ``REALLYREALLY``.
--db_name=NAME  Sets which MongoDB database this process should use.
                This is useful when running multiple experiments on
                the same machine. Defaults to ``news_crowdsourcing``.
--make_payments=BOOL  Options are either ``True`` or ``False``, defaults to ``True``.
                      Only one process per load-balanced set should
                      have ``True`` set.  This sets whether the
                      process is responsible for accepting worker
                      responses.  The ``daemons`` script handles this
                      automatically.
--daemonize=BOOL  Options are either ``True`` or ``False``, defaults to ``False``.
                  This only works in Linux, and it runs Crowdsourcer
                  in the background.  It will kill other daemonized
                  Crowdsourcer instances running on the same port.
                  The log is stored in ``log/tornado.PORTNUM.log``.

Daemonizer
----------

The daemonizer works only under Linux.  It manages instances described
in ``config/daemons_config.py`` running as a background process.  A
benefit for running Crowdsourcer as a background process is that there
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
with a running Crowdsourcer instance on a different port, one of which
being responsible for payments.


Model
=====

Confusingly, Crowdsourcer overloads the word HIT ("human intelligence
task").  There is the HIT in Amazon Mechanical Turk, which is a single
entry that is published for workers to see.  This appears as something
like the following, at least in the Amazon Mechanical Turk Requester
interface:

.. figure:: /static/doc_img/crowdsourcer_amazon_hit_example.png
   :align: center

For each assignment in the MTurk HIT, there is a corresponding HIT in
Crowdsourcer, also known as a cHIT (for "Crowdsourcer HIT").  As
workers follow the link in the HIT, they are assigned one of the cHITs
that has been assigned to no one else yet.  The Admin interface tends
to call cHITs a "HIT," but hopefully there won't be too much
confusion.

Each cHIT has a number of tasks.  Tasks happen in sequence, and a task
is shown to the worker as a single screen.  The screen is divided into
two parts.  The left division is an iframe that can hold HTML
configured by the task.  The right division is a number of modules.

.. figure:: /static/doc_img/crowdsourcer_task_example_news_scaled.png
   :alt: An example task.
   :align: center

Each section in the right division is a module.  Modules are a labeled
collection of questions of various types.  A worker is forced to
complete each module before going onto the next task for the cHIT.

Multiple cHITs can refer to the same tasks.  There is a mechanism for
preventing a worker from being assigned a cHIT if that cHIT has a task
which is contained in exclusion lists of tasks they have already
completed.

Multiple tasks can refer to the same modules.  Task/module pairs are
used for defining the group of users who have done the "same" question
for purposes of assigning bonuses.

Just to emphasize the structure of the model once more: there is a
many-to-many relation between cHITs and tasks, and a many-to-many
relation between tasks and modules.  The task/module pair defines the
context for the questions in the module.


Administration
==============

Once Crowdsourcer is installed and running, there are two important
URLs.  The first is
::

  http://YOUR.DOMAIN/doc/

which has this online documentation for Crowdsourcer, and the other is
::

  http://YOUR.DOMAIN/admin/

which is the main administrative panel.  You will be redirected to
Google for authentication.  Crowdsourcer asks for your identity so
that it can record who begins and ends HITs for accountability.

You may find that Crowdsourcer does not let you see the Admin panel.
If this happens, check ``config/app_config.py`` to see that your
Google account is indeed in the superadmins list.  Worse, you may find
that Google is not wanting to authenticate.  If this happens, make
sure you followed the instructions in `Google configuration`_ exactly.

Admin panel
-----------

You can get to the admin panel using the URL similar to
``http://YOUR.DOMAIN/admin/``.  When there is a Mechanical Turk run,
the interface will look something like the following:

.. figure:: /static/doc_img/crowdsourcer_admin_example_scaled.png
   :align: center

Status
++++++

.. figure:: /static/doc_img/crowdsourcer_admin_status_example.png
   :align: center

The status is in the upper left corner of the interface.  It tells you
whether the system is running in ``development`` or ``production``
mode, whether you are a superadmin (and a link to the `Superadmin
panel`_), how many cHITs and tasks are loaded and completed,
information about your Mechanical Turk account (if one has been
entered), as well as the HIT id for the current HIT (if one is
currently running).

If a Mechanical Turk account has been provided in the Recruit_
interface, then there will be one of two buttons: "Begin Run" or "End
Run."

Begin Run
  Publishes a HIT on Amazon Mechanical Turk with the information
  provided under Recruit_.  The cHITs shown in HITs_ will be assigned
  to the MTurk workers as they visit your Crowdsourcer
  installation. The published HIT will have exactly as many
  assignments as there are uncompleted cHITs.  Beginning a run does
  not clear the database of prior responses; this is accomplished by
  uploading an XML file again.

End Run
  Expires the HIT on Amazon Mechanical Turk and computes and pays out
  bonuses (if applicable).

In both cases, an event will be recorded and show up in the Events_
area.

Upload
++++++

.. figure:: /static/doc_img/crowdsourcer_admin_upload_example.png
   :align: center

The format for a Crowdsourcer run description is XML as described in
this document.

Upload XML
  If there is no ongoing run, then this button will be enabled.
  Select a Crowdsourcer XML file and click "Upload XML" to upload a
  job description.  This operation will also clear all prior results
  from the database, so make sure to use the following download
  buttons *before* uploading a new XML file.

Download current data
  At any point (even during an ongoing run), you may download the
  resulting data from the job.  The output format is described in this
  document.

Download bonus info
  After ending a run and after the bonus info has been computed, this
  button will be enabled and it will contain JSON describing all of
  the awarded bonuses.

Note that the only way to run an experiment again is to re-upload the
XML, as this is the only way to clear the database (except for using
the ``--drop`` option, described above).

Recruit
+++++++

.. figure:: /static/doc_img/crowdsourcer_admin_recruit_example.png
   :align: center

To be able to publish a HIT onto Amazon Mechanical Turk, you must
enter the Access Key and the Secret Key for your account, as well as
how much you want to pay per HIT, a title, a description, and some
keywords for the HIT.  After changing this information, you must click
"Update Turk Info" for the change to take effect.

All admins share the same Mechanical Turk information, and all admins
can see the access key and secret key for the account.

While there is an ongoing run, clicking "Update Turk Info" will not
change the posted description on Mechanical Turk.  It is not wise to
click this button while there is an ongoing run because this has been
untested.

Events
++++++

.. figure:: /static/doc_img/crowdsourcer_admin_events_example.png
   :align: center

Whenever runs are begun or ended, an entry is recorded in the Events
area.  These events are persisted between sessions and jobs.

HITs
++++

.. figure:: /static/doc_img/crowdsourcer_admin_hits_example.png
   :align: center

When an XML file has been uploaded, this area is populated with all of
the cHITs described in that file.  When an MTurk worker accepts the
published HIT, they are directed to ``http://YOUR.DOMAIN/HIT/``, where
they are assigned one of these cHITs.

Each cHIT is formatted based on if it is being worked on or if it has
been completed.  It should be clear form experience which formatting
style corresponds to HITs that no one is working on, that someone is
working on, and that have been completed.  At the time of writing,
though, the formats were orange normal, red bold, and green italics,
respectively.

Note that if another admin uploads a new XML file, this area will not
be updated.  You must refresh the page.

Upon clicking on a cHIT, a Tasks section appears just below which
shows all of the tasks inside that cHIT.  When clicking on any of the
tasks, you can see what an MTurk worker would see for that task.  When
clicking on "Show HIT" in this Tasks section, the cHIT is reserved for
you and you may take the cHIT yourself, recording the data in the
database (here, "reserve" means that no other worker will be assigned
this cHIT unless the system automatically releases the assignment
because it goes "stale").  The URL for these "Show HIT" links can be
given to anyone if you want them to take a particular cHIT.

Superadmin panel
----------------

.. figure:: /static/doc_img/crowdsourcer_superadmin_example.png
   :align: center

If you are a superadmin, a link with the text "Administer admins" will
appear in the status area of the admin panel.  This panel lets you add
Google accounts which should be able to access the admin panel.
Whenever a superadmins visits the admin panel, they are automatically
added to the list of admins.


XML Format
==========

This section describes the structure of the XML file used for
describing an experiment (see Upload_ for how to upload the XML file
to Crowdsourcer).

The main structure of the XML file is as follows:
::

 <xml>
   <modules>
     ... module definitions ...
   </modules>
   <tasks>
     ... task definitions ...
   </tasks>
   <hits>
     ... hit definitions ...
   </hits>
   <documents>
     ... document definitions ...
   </documents>
 </xml>

The ``documents`` section is optional if it is empty, otherwise the
first three are required.

Modules
-------

A module has an internal name, a visible header, and a list of
questions:
::

 <module>
   <name>module_name</name>
   <header>Visible Module Header</header>
   <questions>
     ... question definitions ...
   </questions>
 </module>

Questions
---------

There are a few types of questions which have been defined.  The
general format for a question definition is
::

 <question>
   <varname>internal_variable_name</varname>
   <questiontext>Visible question text</questiontext>
   (<helptext>Optional help text</helptext>)
   <valuetype>some_value_type</valuetype>
   ...
 </question>

The variable name is for determining how the answer is recorded into
the response data.  The value type determines how the question is
rendered.

Numeric questions
+++++++++++++++++

A numeric question (value type ``numeric``) displays as a text box
that only accepts a number.  An example:

.. figure:: /static/doc_img/crowdsourcer_numeric.png
   :align: center

::

 <question>
   <varname>age</varname>
   <valuetype>numeric</valuetype>
   <questiontext>What is your age?</questiontext>
   <helptext>This is your age in years.</helptext>
 </question>

Text questions
++++++++++++++

A text question (value type ``text``) displays as a text box that
accepts any non-empty textual content.  An example:

.. figure:: /static/doc_img/crowdsourcer_text.png
   :align: center

::

 <question>
   <varname>thoughts</varname>
   <valuetype>text</valuetype>
   <questiontext>What were your overall perceptions of the survey?
     Which questions were most confusing? You may also submit any
     other comments that you may have.</questiontext>
   <helptext>We want to better understand the strenghts and weaknesses
     of our survey in order to improve it for future workers. Your
     answer to this question will not influence your
     payment.</helptext>
  </question>

Categorical questions
+++++++++++++++++++++

A categorical question (value type ``categorical``) displays as a set
of radio buttons that accepts exactly one response.  An example:

.. figure:: /static/doc_img/crowdsourcer_categorical.png
   :align: center

::

 <question>
   <varname>married</varname>
   <questiontext>Are you married?</questiontext>
   <helptext>Please answer metaphorically.</helptext>
   <valuetype>categorical</valuetype>
   <content>
     <categories>
       <category>
         <text>Yes</text>
         <value>yes</value>
       </category>
       <category>
         <text>No</text>
         <value>no</value>
       </category>
     </categories>
   </content>
 </question>

The ``text`` element holds what is shown to the worker, and the
``value`` element holds what is recorded to the database for that
categorical response.

Nested categorical questions
++++++++++++++++++++++++++++

For some questions, it is better to show categorical options
hierarchically.  The syntax is exactly the same for ``categorical``
questions, except that the ``text`` elements hold ``|``-separated
options.  The responses will be shown in a tree-like fashion.  An example:

.. figure:: /static/doc_img/crowdsourcer_categorical_nested.png
   :align: center

::

 <question>
   <varname>level_category</varname>
   <valuetype>categorical</valuetype>
   <questiontext>What is this category?</questiontext>
   <content>
     <categories>
       <category>
         <text>Hard|Science|Interesting</text>
         <value>hard_science_interesting</value>
       </category>
       <category>
         <text>Hard|Law</text>
         <value>hard_law</value>
       </category>
       <category>
         <text>Hard|Science|Difficult</text>
         <value>hard_science_difficult</value>
       </category>
       <category>
         <text>Hard|Science|Boring</text>
         <value>hard_science_boring</value>
       </category>
       <category>
         <text>Soft|Animals</text>
         <value>soft</value>
       </category>
     </categories>
   </content>
 </question>


It is possible to have optional specificity.  For example, if we added
a category with text ``Soft|Animals|Teddy Bear`` to the above
definition, then a user could answer either ``Soft|Animals`` or the
sub-category ``Soft|Animals|Teddy Bear``.

Scale questions
+++++++++++++++

For some categorical questions, the options are along a scale that is
best presented horizontally.  This is specified using the
``horizontal`` layout in the ``options`` element for the question.  An
example:

.. figure:: /static/doc_img/crowdsourcer_scale.png
   :align: center

::

 <question>
   <varname>bias</varname>
   <valuetype>categorical</valuetype>
   <questiontext>How biased is this?</questiontext>
   <options>
     <layout>horizontal</layout>
     <lowLabel>Conservative</lowLabel>
     <highLabel>Liberal</highLabel>
     <outsideCategories>N/A</outsideCategories>
     <outsideCategories>Unsure</outsideCategories>
   </options>
   <content>
     <categories>
       <category>
         <text>1</text>
         <value>1</value>
       </category>
       <category>
         <text>2</text>
         <value>2</value>
       </category>
       <category>
         <text>3</text>
         <value>3</value>
       </category>
       <category>
         <text>4</text>
         <value>4</value>
       </category>
       <category>
         <text>5</text>
         <value>5</value>
       </category>
       <category>
         <text>6</text>
         <value>6</value>
       </category>
     </categories>
   </content>
 </question>
