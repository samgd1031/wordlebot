FROM python:3.10

LABEL  "author"="samgd1031@gmail.com"

# set directory and copy files over
WORKDIR /wordleapp
COPY . .

# environment variables for mongo/discord
ENV MONGO_URI = "URI for mongo database" \
    DISCORD_TOKEN="private_discord_token here"

# setup logging directory
RUN mkdir "logs"
VOLUME /logs

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./wordle_reader_main.py"]