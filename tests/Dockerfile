FROM pollease:latest

RUN [ "pip", "install", "unittest2" ]

COPY . /usr/src/tests/

WORKDIR /usr/src

CMD [ "python", "-m", "unittest2", "discover" ]
