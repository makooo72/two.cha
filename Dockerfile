FROM python:3.12-alpine3.20
EXPOSE 8000 5432
COPY requirments.txt /temp/requirments.txt
RUN pip install -r /temp/requirments.txt
COPY my_site /core 
WORKDIR /core
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]