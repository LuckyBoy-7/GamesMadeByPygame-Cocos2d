from pyglet import media, resource


class Sound:
    resource.path.append("../res/sound")
    resource.reindex()

    attack = resource.media("attack.wav", streaming=False)
    mock = resource.media("mock.wav", streaming=False)
    enter = resource.media("enter.wav", streaming=False)
    hurt = resource.media("hurt.wav", streaming=False)

    birthday = resource.media("birthday.mp3", streaming=True)
    determination = resource.media("determination.mp3", streaming=True)
    bgm = resource.media("bgm.mp3", streaming=True)

    music = media.Player()
    music.queue(bgm)