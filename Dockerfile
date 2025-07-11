FROM python:3.13.5-slim

# set a directory for the app
WORKDIR /lorekeeper

# Copy the directory
COPY . /lorekeeper

# install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "lorekeeper.py" ]
