FROM robertbeal/gmusicapi

COPY . /app
WORKDIR /app

CMD /usr/bin/python3 gpm_library_cleaner.py
