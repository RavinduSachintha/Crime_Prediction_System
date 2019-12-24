## Process

1. install anaconda for python 3.7 on windows from [here](https://www.anaconda.com/distribution/)

2. conda create -n djangoenv anaconda
   conda activate djangoenv
	will create and start seperate environment for django

3. conda install -c anaconda django 

4. django-admin startproject webapp
	execute at where you need to setup the project

5. python manage.py migrate
	execute at the inside of project folder

6. conda init
   conda activate djangoenv
   conda deactivate

7. python -m pip install bokeh
   python -m pip install openpyxl

*** conda env update --name djangoenv --file environment.yml
