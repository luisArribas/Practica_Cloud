FROM python:3.9.7

##  Set the working directory in the container
WORKDIR /code

##  Copy the dependencies file to the working directory
COPY requirements.txt .

##  Install dependencies
RUN pip install -r requirements.txt

##  Copy the content of the local src directory to the working directory
COPY src/ .

##  Expose the API port
EXPOSE 8080

##  Run the server
CMD ["python","app.py"]