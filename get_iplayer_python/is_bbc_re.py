IS_BBC_URL_RE = """
(?x)https?://
    (?:www\.)?bbc\.co\.uk/
    (?:
        programmes/(?!articles/)|
        iplayer(?:/[^/]+)?/(?:episode/|playlist/)|
        music/(?:clips|audiovideo/popular)[/#]|
        radio/player/|
        events/[^/]+/play/[^/]+/
    )
    (?P<id>(?:[pbm][\da-z]{7}|w[\da-z]{7,14}))
"""