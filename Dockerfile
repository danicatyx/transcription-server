# start by pulling the python image
FROM python:3.9.9

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

#declaring the replicate api token
ARG REPLICATE_API_TOKEN

#assigning that token that was passed in to the env token
ENV REPLICATE_API_TOKEN=$REPLICATE_API_TOKEN

# install whisper
#RUN pip3 install -U openai-whisper

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["whisperapp.py" ]