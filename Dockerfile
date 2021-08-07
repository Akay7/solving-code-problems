FROM ubuntu:20.04
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --no-install-suggests -y  \
    python3-pip nginx \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# forward access and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY configs/nginx_server.conf /etc/nginx/sites-enabled/default
COPY backend ./backend/

RUN python3 ./backend/manage.py collectstatic -l
CMD nginx && \
    gunicorn --bind unix:/tmp/gunicorn.sock --timeout 1800 --workers 5 \
             --chdir backend solving_code_problems.wsgi:application
