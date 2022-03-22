import time

import vlc


class BikePlayer:
    """ BikePlayer class handles opening the media and handling playback
    """

    def __init__(self):
        # self.vlc_instance = vlc.Instance('--verbose 2'.split())
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

    def __del__(self):
        self.player.stop()

    def play_file(self, fname: str) -> None:
        """plays file

        :param fname: file name to play
        :type fname: str
        """
        self.player.stop()
        media = self.vlc_instance.media_new(fname)

        self.player.set_media(media)
        self.player.audio_set_mute(True)
        self.player.toggle_fullscreen()
        self.player.play()

    def set_speed(self, rate: float):
        """set playback speed

        :param rate: rate (1 is same, 2 is twice as fast)
        :type rate: float
        """
        self.player.set_rate(rate)
