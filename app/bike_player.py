import vlc
import time


class BikePlayer:

    def __init__(self):
        # self.vlc_instance = vlc.Instance('--verbose 2'.split())
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

    def __del__(self):
        self.player.stop()

    def play_file(self, fname: str) -> None:
        self.player.stop()
        media = self.vlc_instance.media_new(fname)

        self.player.set_media(media)
        self.player.play()

    def set_speed(self, rate: float):
        self.player.set_rate(rate)


if __name__ == "__main__":
    bp = BikePlayer()
    bp.play_file('RedHeart.mp3')
    while True:
        time.sleep(1)
