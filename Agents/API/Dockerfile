FROM crawforc3/raspberrypi-uwsgi-nginx-flask
ENV LISTEN_PORT 5000
# copy over our requirements.txt file
COPY requirements.txt /

# upgrade pip and install required python packages
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r /requirements.txt

# copy over our app code
COPY ./app /app
EXPOSE 5000
