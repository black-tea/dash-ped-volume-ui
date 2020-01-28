FROM python:3

# set directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# port number the container should expose
EXPOSE 8050

# run the command
CMD ["python", "./app.py"]
