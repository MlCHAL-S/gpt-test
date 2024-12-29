FROM python:3.12-slim

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

ENV DEBUG=True
ENV HOST=0.0.0.0
ENV PORT=5000
ENV FLASK_APP=api

CMD ["flask", "run"]
