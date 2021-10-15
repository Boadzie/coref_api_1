# Builds a considerably smaller image
FROM python:3.7-slim 

# # set work directory
# COPY ./app /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8008
ENV PATH="$PATH:$HOME/.poetry/bin"


WORKDIR /app

# install curl
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential

# install poetry
RUN pip3 install poetry

# install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

# copy project
COPY . .
RUN poetry install --no-dev

# install language model
RUN poetry run python -m spacy download en_core_web_sm

EXPOSE 8008


# command to run on container start 
CMD ["poetry run", "uvicorn", "bert_summarizer.main:app", "--host", "0.0.0.0", "--port", "8008"]