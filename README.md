# Django mini-cms-blog blog 


<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/eri-bga/mini-cms-blog">
    <img src="blog/static/images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">mini-cms-blog application</h3>

  <p align="center">
    A mini-cms blog application written in Django and tailwindcss.
    <br />
    ·
    <a href="https://github.com/eri-bga/mini-cms-blog/issues">Report Bug</a>
    ·
    <a href="https://github.com/eri-bga/mini-cms-blog/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Demo

[![Blog application][product-screenshot]](/demo/demo-blog.gif)

### Built With

* [![Django][djangoproject]][djangoproject-url]
* [![PostgreSQL][postgresql]][postgresql-url]
* [![TailwindCSS][tailwindcss]][tailwindcss-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is a fully functional min-cms blog which helps you quickly get started and it's easily customizable as it is build with Django and TailwindCSS.

### Prerequisites

-  Python 3.8+
-  Django 4+

### Installation

`$ git clone https://github.com/eri-bga/mini-cms-blog.git`

`$ cd mini-cms-blog/`

I am using `poetry` to manage dependencies and create virtual environments
If you are not familiar to `poetry`, please refer `https://python-poetry.org/`

I configured `poetry` so that the virtualenv path is inside my project directory but you can use the default path.

Please check `pyproject.toml` for dependencies

Then run the following commands
run `poetry shell` to enter into the virtualenv
or if you setup the virtualenv in your project,
`source venv/bin/activate` assuming your virtualenv path is `venv` inside your project directory

`poetry install` to install all dependencies
This will install all dependencies listed in `pyproject.toml`

You can also add new dependencies as `poetry add package`

There are some changes to the settings
Retrieve your public and secret keys for the google recaptcha from google.com
Then add those keys the settings as follows:

```
RECAPTCHA_PUBLIC_KEY = 'sadfsadfsdfsdfsdfsdfsdfsdfsdfsdfdfss'
RECAPTCHA_PRIVATE_KEY = 'sadfsdfssdfsdfsdfsdfsdfsdf'
```
Run migrations for Database 

`$ poetry run python manage.py makemigrations`

`$ poetry run python manage.py migrate`

Create superuser for Admin Login 🔐

`$ poetry run python manage.py createsuperuser`

Enter your desired username, email and password. Make sure you remember them as you'll need them in future.

eg.

    Username: admin
    
    Email: admin@example.com
    
    Password: sTr0ngP4s$W0rd

All Set! 🤩

Now you can run the server to see your application up & running 🚀

`$ poetry run python manage.py runserver`

To exit the environment ❎

`$ deactivate`


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Features -->
## Features

* Users are able to register from the frontend
* Signing up with regular username and password or using Google authentication(can be easily extended to other social authentication)
* RSS feed subscription
* Newsletter subscription
* Sending email to your subscribers
* uploading images via the TinyMCE library
* Nicely formatted success or error messages
* Pagination
* ReCaptcha support
* Comment support for authenticated users
* tagging support

See the [open issues](https://github.com/eri-bga/mini-cms-blog/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Todo
* Add unit tests
* Add integration tests
* empty test files are already there but feel free to add yours

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Links -->
[djangoproject]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[djangoproject-url]: https://djangoproject.com/
[tailwindcss]: https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white
[tailwindcss-url]: https://tailwindcss.com/
[postgresql]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[postgresql-url]: https://postgresql.org/
[product-screenshot]: demo/demo-blog.gif
[contributors-shield]: https://img.shields.io/github/contributors/eri-bga/mini-cms-blog.svg?style=for-the-badge
[contributors-url]: https://github.com/eri-bga/mini-cms-blog/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/eri-bga/mini-cms-blog.svg?style=for-the-badge
[forks-url]: https://github.com/eri-bga/mini-cms-blog/network/members
[stars-shield]: https://img.shields.io/github/stars/eri-bga/mini-cms-blog.svg?style=for-the-badge
[stars-url]: https://github.com/eri-bga/mini-cms-blog/stargazers
[issues-shield]: https://img.shields.io/github/issues/eri-bga/mini-cms-blog.svg?style=for-the-badge
[issues-url]: https://github.com/eri-bga/mini-cms-blog/issues
[license-shield]: https://img.shields.io/github/license/eri-bga/mini-cms-blog.svg?style=for-the-badge
[license-url]: https://github.com/eri-bga/mini-cms-blog/blob/master/LICENSE.txt

