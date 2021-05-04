sudo -u postgres psql

create database tracker

create user with password 'tracker'

grant all privileges on database tracker to tracker

source venv/bin/activate

pip install -r requirements.txt

./manage.py makemigrations

./manage.py migrate

./manage.py runserver

register_1 >> {localhost}/auth/activations/

register_2 >> {lolachost}/auth/activations/activate/

login      >> {localhost}/users/login/

create_task >> {localhost}/core/task/          post_method

change_status >> {localhost}/core/task/        patch_method

also, there is a celery task to remember to executors about their task's deadline

jwt authentication

you can check the postman json format to make a requests. in this directory