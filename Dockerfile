FROM python:3.12.9-slim-bookworm

# set a directory for the app
WORKDIR /lorekeeper

# Copy the reuirements for installation
COPY . /lorekeeper

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "lorekeeper.py" ]