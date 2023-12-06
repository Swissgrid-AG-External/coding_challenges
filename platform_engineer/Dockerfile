# 
FROM python:3.9

#
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./my_first_api /code/my_first_api

# 
CMD ["uvicorn", "my_first_api.main:app", "--host", "0.0.0.0", "--port", "80"]
