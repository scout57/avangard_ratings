FROM python:3.12-slim

ARG JYPUTER_PORT=8000
ENV JYPUTER_PORT=${JYPUTER_PORT}
EXPOSE ${JYPUTER_PORT}

WORKDIR /project

COPY project/ /project/

RUN chmod +x /project/install.sh /project/one-shot.sh

RUN bash /project/install.sh

CMD ["bash", "/project/one-shot.sh"]
