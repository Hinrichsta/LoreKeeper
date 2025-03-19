FROM python:3.12.9-slim-bookworm

# set a directory for the app
WORKDIR /lorekeeper

# Copy the directory
COPY . /lorekeeper

# install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "lorekeeper.py" ]