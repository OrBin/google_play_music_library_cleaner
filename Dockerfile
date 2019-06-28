FROM robertbeal/gmusicapi

WORKDIR /app
COPY gpm_library_cleaner.py /app/gpm_library_cleaner.py

CMD /usr/bin/python3 gpm_library_cleaner.py
