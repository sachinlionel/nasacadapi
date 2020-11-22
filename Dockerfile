# Base OS ubuntu:20.04
# buildbase is used to compile & install python libs
FROM ubuntu:20.04 as buildbase
ENV PYTHONUNBUFFERED=TRUE

ARG APPDIR=/usr/local/app
WORKDIR $APPDIR

# Add requirements.txt
COPY requirements.txt .

# TODO:: Create USER and excute the scripts as user, TBD!
RUN apt-get update && apt-get install -y --no-install-recommends\
    # Install OS essentials, psycopg2 deps, python3 & pip
    build-essential\
    libpq-dev\
    python3-dev python3.8 python3-pip\
    # symlink: python3 to python ==> `python` executable && pip3 to pip ==> `pip` executable
    && ln -s /bin/python3.8 /bin/python && ln -s /bin/pip3 /bin/pip\
    # Install python dependencies
    && pip install --no-cache-dir --no-build-isolation --ignore-installed -r requirements.txt\
    # clean up
    && rm -r /usr/share/python-wheels/\
    && rm -rf /var/lib/apt/lists/*\
    && apt-get clean -y\
    && apt-get autoremove -y\
    && apt-get purge -y --auto-remove python3-pip python3-dev build-essential\
    && find / -name *.pyc | xargs rm -r

# Copy Application to WORKSPACE
COPY app app
COPY utils utils
COPY tests tests
COPY run_tests.py run_tests.py

# Final Docker Image
FROM ubuntu:20.04
WORKDIR /usr/local/app
# Environment Variables
ENV PYTHONUNBUFFERED=TRUE

RUN apt-get update && apt-get install -y --no-install-recommends\
    # Install OS essentials, psycopg2 deps, Python3
    libpq-dev\
    python3.8\
    # clean up
    && rm -rf /var/lib/apt/lists/*\
    && apt-get clean -y\
    && apt-get autoremove -y\
    && find / -name *.pyc | xargs rm -r\
    # symlink: python3 to python ==> `python` executable
    && ln -s /bin/python3.8 /bin/python

COPY --from=buildbase /usr/local/lib/python3.8/dist-packages /usr/local/lib/python3.8/dist-packages
COPY --from=buildbase /usr/local/app /usr/local/app

# EntryPoint
# ENTRYPOINT []
CMD ["bash", "-c", "python run_tests.py"]
