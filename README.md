# Invoicing Django

Facturacion Django is a web application for managing billing and invoicing. Built using the Django web framework, the application allows users to create and manage customers, create and send invoices, and generate reports.
Getting Started

To get started with Facturacion Django, follow these steps:

    Clone the repository onto your local machine:

    bash

git clone https://github.com/pjavier1988/facturaciondjango.git

Install the required Python packages:

pip install -r requirements.txt

Create a new Django project:

django-admin startproject facturacion

Copy the facturacion directory from the cloned repository into the newly created project directory.

Run the Django development server:

bash

    cd facturacion
    python manage.py runserver

    Open your web browser and go to http://localhost:8000 to access the application.

Features

Facturacion Django includes the following features:

    Customer management: create, view, edit, and delete customers.
    Invoice creation: create new invoices for customers, including line items and taxes.
    Invoice sending: send invoices to customers via email.
    Report generation: generate reports on invoices and customers.

Project Structure

The Facturacion Django project is structured as follows:

    facturacion: Django project directory.
    invoices: Django app for managing invoices.
    clients: Django app for managing customers.
    reports: Django app for generating reports.
    static: static files for the application.
    templates: HTML templates for the application.
    requirements.txt: Python package requirements for the application.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    This project was inspired by Django Invoicing.
