.. Crowdsourcr documentation master file, created by
   sphinx-quickstart on Fri Nov 29 09:26:38 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Crowdsourcr!
=======================================

Crowdsourcer is an application for conducting survey-like experiments
online, especially when used in conjunction with Amazon Mechanical
Turk.

Surveys are designed as XML files. A set of tasks are bundled as a HIT that can be posted on Mechanical Turk. The XML survey format allows for multiple-data entry 
and bonuses paid to workers depending on how well they do compare to others. The XML format also allows for conditional questions.

The following is an example from one real experiment asking Turkers to evaluate news articles:

.. figure:: doc_img/crowdsourcer_task_example_news_scaled.png
   :alt: An example task.
   :align: center

.. toctree::
   :maxdepth: 2
   
   usage/installation
   usage/running
   usage/model
   usage/admin
   usage/xmlformat



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
