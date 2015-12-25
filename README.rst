Django-nmrpro App
=================

The App provides a web interface to the python package, effectively compressing and reformatting NMR spectra into JSON formats. The App also stores users' spectra in a database along with their processing history. Also, the App collects all plugins from the python package and transfers them to the client-side, where they are rendered as GUI. 



Installtion
***********
1. Install `python 2.7 <https://www.python.org/downloads/release/python-2710/>`_ and pip package manager.

2. From the terminal console, install NMRPro python package using the command::    

    pip install nmrpro

 On Windows, from the command prompt::

    python -m pip install nmrpro

3. Install the django-nmrpro App using the command::

    pip install django-nmrpro

 On Windows::

    python -m pip install django-nmrpro

4. pip command automatically installs all necessary package dependencies.
5. There is no need to install SpecdrawJS separately since it is included in the Django App.


Runnig NMRPro server
********************
Once the Django App is installed, the user can integrate it into an existing Django project. To summarize the integration process, briefly:

1. If you do not have an existing Django project, first create one by following `this tutorial <https://docs.djangoproject.com/en/1.8/intro/tutorial01/>`_.
2. In ``settings.py``, add django_nmpro to your ``INSTALLED_APPS``.
3. In ``urls.py``, add the following pattern ``url(r'^', include('django_nmrpro.urls')),``.
4. From the terminal console (*command prompt on Windows*), navigate to the project home directory and run the web server using the command::
    
    python manage.py migrate

5. Run the server using the command::

    python manage.py runserver

6. To make sure that installation is successful, visit the URL http://127.0.0.1:8000/nmrpro_test/, which should display 5 spectra from the Coffees dataset.



