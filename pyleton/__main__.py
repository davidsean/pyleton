

import argparse

from pyleton.bike_player import BikePlayer
from pyleton.wheel_sensor import WheelSensor

parser = argparse.ArgumentParser(description='Usage.')
parser.add_argument('--file', dest='fname', type=str,
                    default='track.mp3',
                    help='file to play (default 20)')
parser.add_argument('--ref', dest='ref', type=float,
                    default=20,
                    help='reference speed (default 20)')


args = parser.parse_args()

if __name__ == '__main__':
    bp = BikePlayer()
    bp.play_file(args.fname)
    ws = WheelSensor(bp.set_speed, ref_speed=args.ref)