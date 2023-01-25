FROM python:3.10
WORKDIR /vk_mock
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV VK_URL=0.0.0.0:5000
CMD [ "python3", "./flask_mock.py"]