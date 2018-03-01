# Encyclopedia

This is encyclopedia for web-developers. Here you can find useful materials and a brief articles needed for successful performing tasks from [DEVMAN.org](https://devman.org) training course. <br /> The code contained herein (python script and HTML) is written as a part of Devman course.<br />

The purpose of the script is to build a simple static page site by filling HTML templates with appropriate content using [Jinja](http://jinja.pocoo.org/).. <br />
HTML pages are based on [Bootstrap](https://getbootstrap.com) templates.


Pavel Kadantsev, 2018. <br/>
p.a.kadantsev@gmail.com


# Installation

Python 3.5 should be already installed. <br />
Download or clone this repo on your machnine and install dependencies using ```pip install -r requirements.txt``` in CLI. <br />
Usage of virtual environment is recommended. Create it using ```python -m venv your_environment_name```.


# Usage

To execute the script run the command ```python site_generator.py``` in OS console/terminal.

You will see the following:

<pre>
<b>>python site_generator.py </b>
[I 180301 22:38:42 server:283] Serving on http://127.0.0.1:5500
[I 180301 22:38:42 handlers:60] Start watching changes
[I 180301 22:38:42 handlers:62] Start detecting changes
</pre>

Site is now available in your browser at ```http://127.0.0.1:5500```.


When script is executed you will find out that a new ```site``` directory is created in the script root directory.

The ```site``` folder content is like that:

```
├── index.html
├── articles
│   ├── 0_tutorial
│   │   ├── 14_google.html
│   │   ├── 27_devman.html
│   │   ├── 29_english.html
│   │   ├── 7_codenvy.html
│   │   ├── 8_cli.html
│   │   └── 9_git.html
│   ├── 1_python_basics
│   │   ├── 10_pep8.html
│   │   ├── 18_comments.html
│   │   ├── 1_intro.html
│   │   ├── 2_base_types.html
│   │   ├── 3_base_constructions.html
│   │   ├── 4_types.html
│   │   ├── 5_modules.html
│   │   └── 6_tips_and_tricks.html
│   ├── 2_html
│   │   ├── html_injection.html
│   │   └── special &amp; symbol.html
│   └── 4_git
│       └── 22_git_history.html
```

If needed you may write a new article in ```.md``` but also don't forget to update ```config.json``` file. <br />

The script will convert your ```.md``` into ```.html``` and link to the new article will appear in the appropriate section on the Encyclopedia index page. <br />

You don't need to rerun the scripts: [livereload](https://pypi.python.org/pypi/livereload/2.5.1) will take care of it. <br />
It also watches for changes in present articles as well as index page and article page HTML templates and re-render page when any changes appear. <br />


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
