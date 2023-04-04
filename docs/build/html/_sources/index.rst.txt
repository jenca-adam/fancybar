.. fancybar documentation master file, created by
   sphinx-quickstart on Mon Apr  3 20:49:56 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fancybar's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

#########
fancybar
########
.. image:: fancybar-showcase.gif

`fancybar` is a highly customizable terminal progress bar library.
Usage is very simple:
.. code-block:: 
    
    import fancybar
    for i in fancybar.bar(range(100)):
       # Do something

You can also create a bar without an iterable:
.. code-block::
    
    import fancybar
    bar = fancybar.ProgressBar(100)
       with bar:
           # Do something

Bar Types
---------
Please note that not all bar types will work on all terminals!

