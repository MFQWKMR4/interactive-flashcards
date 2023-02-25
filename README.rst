========
Overview
========
[fork] small cli tool to study using fl

* Free software: BSD license

Installation
============

::

    pip3 install -r requirements.txt


How does this work
==================

``python-flashcards`` is a small tool, which receives cards from a ``YAML`` file, and shows them in a random order so you can practice.

``YAML`` format:

.. code-block:: yaml

  -
    topic: The topic I will say out loud
    content: The information I'll check after saying out loud what I know
    keywords: reference, words
  -
    topic: Python
    content: Is a widely used high-level programming language for general-purpose programming,
      created by Guido van Rossum and first released in 1991.
    keywords: programming, language


Usage
=====

Let's suppose ``anatomy.yaml`` is your file with information related to anatomy.

::

    python3 cli.py anatomy.yaml

