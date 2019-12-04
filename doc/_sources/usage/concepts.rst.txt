Concepts
========

Confusingly, Crowdsourcr overloads the word HIT ("human intelligence
task").  There is the HIT in Amazon Mechanical Turk, which is a single
entry that is published for workers to see.  This appears as something
like the following, at least in the Amazon Mechanical Turk Requester
interface:

.. figure:: ../doc_img/crowdsourcer_amazon_hit_example.png
   :align: center

For each assignment in the MTurk HIT, there is a corresponding HIT in
Crowdsourcr, also known as a cHIT (for "Crowdsourcr HIT").  As
workers follow the link in the HIT, they are assigned one of the cHITs
that has been assigned to no one else yet.  The Admin interface tends
to call cHITs a "HIT," but hopefully there won't be too much
confusion.

After accepting your HIT on Amazon and clicking on the associated crowdsourcr link a worker is directed to a login where she has to enter her worker id:

.. figure:: ../doc_img/crowdsourcer_worker_login.png
   :alt: Worker login.
   :align: center

This ID is used to later pay the worker's reward as well a bonus (if applicable).

Each cHIT has a number of tasks.  Tasks happen in sequence, and a task
is shown to the worker as a single screen.  The screen is divided into
two parts.  The left division is an iframe that can hold HTML
configured by the task.  The right division is a number of modules.

.. figure:: ../doc_img/crowdsourcer_task_example_news_scaled.png
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
