![GitHub repo size][GitHub-size-img]
![GitHub top language][GitHub-top-language-img]
![GitHub last commit][GitHub-last-commit-img]
[![License][License-img]][License-img]
[![codecov][Codecov-badge]][Codecov-url]

<div id="readme-top"></div>


<!-- PROJECT LOGO -->
<div align="center">
  <a href="https://github.com/krzycze4/EDMS">
    <img src="https://i.ibb.co/s6WDH1y/company-logo.jpg" alt="Logo" width="120" height="120">
  </a>
  <h3 align="center">EDMS</h3>
  <p align="center">
    <b>E</b>lectronical <b>D</b>ocument <b>M</b>anagement <b>S</b>ystem
    <br/>
    <br/>
    <a href="https://github.com/krzycze4/EDMS/issues/new?labels=bug&template=bug-report.md">Report Bug</a>
    ·
    <a href="https://github.com/krzycze4/EDMS/issues/new?labels=enhancement&template=feature-request.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
## Table of Contents
  1. [About The Project](#about-the-project)
     * [Built With](#built-with)
  2. [Getting Started](#getting-started)
     * [Prerequisites](#prerequisites)
     * [Installation](#installation)
  3. [Usage](#usage)
  4. [Contact](#contact)


## About The Project

<p align="center">
  <img src="https://i.ibb.co/kxcKnDk/login-page.jpg" alt="Login Page Screenshot" width="45%" />
  <img src="https://i.postimg.cc/RSz12hz4/dashboard.jpg" alt="Dashboard Page Screenshot" width="45%" />
</p>

EDMS is a web application designed for enterprise use. Its primary purpose is to allow users to add, edit, and monitor important documents related to business operations. The application features:
* Adding companies to the database using data from the [Polish KRS system API][KRS-api-url]
* Managing cooperation contracts with external companies
* Adding and linking orders to contracts for accounting purposes
* Managing invoices (income, cost, duplicates, corrections, proforma) linked to orders
* User registration, login, and group-based permissions (4 groups: accountants, CEOs, HRs, managers)
* Editing employee contact and address details
* Managing employee requests (vacations, agreements, terminations)
* Generating plots for earnings overview (company-wide or per employee)
* Full API support

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Built With

Below list of used tools / packages in application:


* [![Python][Python]][Python-docs]
* [![Django][Django]][Django-docs]
* [![DjangoREST][DjangoREST]][DjangoREST-docs]
* [![Docker][Docker]][Docker-docs]
* [![Celery][Celery]][Celery-docs]
* [![Poetry][Poetry]][Poetry-docs]
* [![Redis][Redis]][Redis-docs]
* [![Postgres][Postgres]][Postgres-docs]
* [![Jinja][Jinja]][Jinja-docs]
* [![Plotly][Plotly]][Plotly-docs]
* [![Codecov][Codecov]][Codecov-docs]
* [![Pre-commit][Pre-commit]][Pre-commit-docs]
* [![Silk][Silk]][Silk-docs]
* [![Factory Boy][Factory Boy]][Factory Boy-docs]
* [![Coverage][Coverage]][Coverage-docs]


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

Below are the instructions on how to set up this project locally.
Follow these simple steps to get a local copy up and running.

### Prerequisites

This is the list of tools you need to use the software and how to install them.

* ***Docker***

    Download and install Docker from the [official Docker website][Docker-docs].

        docker --version

    You should see something like:

        Docker version 27.0.3, build 7d4bcd8

* ***Docker Compose***

    Download and install Docker from the [official Docker Compose website][Docker-Compose-docs].

        docker-compose --version

    You should see something like:

        Docker Compose version v2.28.1-desktop.1


### Installation

Follow the steps below to install and set up your Django project locally.

1. Clone the repo
   ```sh
   git clone https://github.com/krzycze4/EDMS.git
   cd EDMS
2. Create `.env` file

    Create a new `.env` file in the directory where `env.dist` is located and add your environment variables.
3. Build Docker containers
   ```sh
   docker-compose build
   ```
4. Create superuser
   ```sh
   docker-compose exec edms-web python manage.py createsuperuser
   ```
5. Optionally create example data in database
    ```sh
   docker-compose exec edms-web python manage.py generate_example_data
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage

After building the Docker images, you can start and use the application locally with the following steps:
1. Start Docker containers:
   ```sh
   docker-compose up
   ```
   or, to run them in the background (detached mode):
    ```sh
   docker-compose up -d
   ```
2. Create superuser
   ```sh
   docker-compose exec edms-web python manage.py createsuperuser
   ```
3. Optionally create example data in database
    ```sh
   docker-compose exec edms-web python manage.py generate_example_data
   ```
4. You can enter to admin dashboard to manage data:
    ```sh
   http://localhost:8000/admin/
   ```
5. You can start to go to the login page:
    ```sh
   http://localhost:8000/login/
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contact

<p>Full name: Krzysztof Czernicki</p>
<p>Email: czernicki.krz@gmail.com</p>

Project Link: [EDMS][My-repo]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->

[Python]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[Python-docs]: https://docs.python.org/3/
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[Django-docs]: https://docs.djangoproject.com/en/4.2/
[DjangoREST]: https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white
[DjangoREST-docs]: https://www.django-rest-framework.org/
[Docker]: https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white
[Docker-docs]: https://docs.docker.com/
[Celery]: https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4
[Celery-docs]: https://docs.celeryq.dev/en/stable/
[Poetry]: https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D
[Poetry-docs]: https://python-poetry.org/docs/
[Redis]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
[Redis-docs]: https://redis.io/docs/latest/
[Postgres]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-docs]: https://www.postgresql.org/docs/
[Jinja]: https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black
[Jinja-docs]: https://jinja.palletsprojects.com/en/3.1.x/
[Plotly]: https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white
[Plotly-docs]: https://plotly.com/python/
[Codecov]: https://img.shields.io/badge/Codecov-F01F7A?style=for-the-badge&logo=Codecov&logoColor=white
[Codecov-docs]: https://img.shields.io/badge/Codecov-F01F7A?style=for-the-badge&logo=Codecov&logoColor=white
[Pre-commit]: https://img.shields.io/badge/pre--commit-F6C915?style=for-the-badge&logoColor=black
[Pre-commit-docs]: https://pre-commit.com/
[Silk]: https://img.shields.io/badge/Silk-18BFFF?style=for-the-badge&logoColor=white
[Silk-docs]: https://silk.readthedocs.io/en/latest/
[Factory Boy]: https://img.shields.io/badge/Factory%20Boy-3498DB?style=for-the-badge&logo=xamarin&logoColor=white
[Factory Boy-docs]: https://factoryboy.readthedocs.io/en/stable/
[Coverage]: https://img.shields.io/badge/Coverage-000?style=for-the-badge&logoColor=white
[Coverage-docs]: https://coverage.readthedocs.io/en/7.6.1/
[GitHub-size-img]: https://img.shields.io/github/repo-size/krzycze4/EDMS
[GitHub-top-language-img]: https://img.shields.io/github/languages/top/krzycze4/EDMS
[GitHub-last-commit-img]: https://img.shields.io/github/last-commit/krzycze4/EDMS
[License-img]: https://img.shields.io/github/license/krzycze4/EDMS
[License-url]: https://github.com/krzycze4/EDMS/blob/main/LICENSE
[Codecov-badge]: https://codecov.io/github/krzycze4/EDMS/branch/main/graph/badge.svg?token=L3DPXR5VOP
[Codecov-url]: https://codecov.io/github/krzycze4/EDMS
[KRS-api-url]: https://prs.ms.gov.pl/krs/openApi
[Docker-docs]: https://www.docker.com/get-started
[Docker-Compose-docs]: https://docs.docker.com/compose/
[My-repo]: https://github.com/krzycze4/EDMS.git
