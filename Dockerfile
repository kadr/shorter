# Dockerfile
# Pull base image

FROM python:3.7

# Set work directory
WORKDIR /short_urls

RUN pip3 install virtualenv
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/short_urls/venv
#RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=$VIRTUAL_ENV


COPY . $WORKDIR
# Install dependencies
CMD . venv/bin/activated
RUN pip install -r requirements.txt
CMD ["python",  "manage.py", "migrate"]
CMD ["python", "-m", "celery", "beat", "-A", "short_urls"]