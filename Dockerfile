FROM python:3.9-slim

RUN useradd --create-home --shell /bin/bash user

WORKDIR /home/user

USER user

COPY . .

CMD ["bash"]