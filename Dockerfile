FROM python:2-onbuild

EXPOSE 8080

CMD [ "python", "./pollease/pollease.py" ]
