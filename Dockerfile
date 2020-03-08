FROM python:3.7



COPY requirements.txt /tmp/
RUN pip install \
  --no-cache-dir \
  -r /tmp/requirements.txt

COPY . ./

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]