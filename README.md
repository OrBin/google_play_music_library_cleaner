# google_play_music_library_cleaner
A process that every hour deletes all the downvoted songs.

It depends on [gmusicapi](https://github.com/simon-weber/Unofficial-Google-Music-API). If you do not have [gmusicapi](https://github.com/simon-weber/Unofficial-Google-Music-API) installed, install it by running:
```
pip install gmusicapi
```

Another requirement is a configuration file named ```.google_play_music_cleaner_config```, which is as the following:
```
your_username@gmail.com
your_password
```

To use it, run:
```
python google_play_music_cleaner.py
```

