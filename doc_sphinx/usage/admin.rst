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
sure you followed the instructions in :ref:`google configuration` exactly.

Admin panel
-----------

You can get to the admin panel using the URL similar to
``http://YOUR.DOMAIN/admin/``.  When there is a Mechanical Turk run,
the interface will look something like the following:

.. figure:: ../doc_img/crowdsourcer_admin_example_scaled.png
   :align: center

Status
++++++

.. figure:: ../doc_img/crowdsourcer_admin_status_example.png
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

.. _admin upload:

Upload
++++++

.. figure:: ../doc_img/crowdsourcer_admin_upload_example.png
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

.. figure:: ../doc_img/crowdsourcer_admin_recruit_example.png
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

.. figure:: ../doc_img/crowdsourcer_admin_events_example.png
   :align: center

Whenever runs are begun or ended, an entry is recorded in the Events
area.  These events are persisted between sessions and jobs.

HITs
++++

.. figure:: ../doc_img/crowdsourcer_admin_hits_example.png
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

.. figure:: ../doc_img/crowdsourcer_superadmin_example.png
   :align: center

If you are a superadmin, a link with the text "Administer admins" will
appear in the status area of the admin panel.  This panel lets you add
Google accounts which should be able to access the admin panel.
Whenever a superadmins visits the admin panel, they are automatically
added to the list of admins.
