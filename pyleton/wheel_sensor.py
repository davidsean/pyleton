# -*- coding: utf-8 -*-

import time
import logging
import wiringpi
import collections

from statistics import mean
from typing import Callable


class WheelSensor:

    def __init__(self,
                 callback: Callable,
                 pin: int = 29,
                 radius: float = 350,
                 ref_speed: float = 20.0) -> None:
        """
        init

        Args:
            callback (function): callback function wheel rotation detection this is called on every detected pusle with agrument of wheel speed %
            pin (int): the GPIO pin number for the reed switch (default pin 29)
            radius (int): The wheel radius, in cm (default 350)
        """

        self._logger = logging.getLogger(__name__)
        self.pin = pin
        self.callback = callback

        # wheel circumference
        self.circumference = 2*3.14*(radius*100)
        # convert km/h to wheel circumferences per second
        self.kph_2_cps = 1000 / (60*60*self.circumference)
        self.cps_2_kph = 1/self.kph_2_cps

        # set reference speed in cps
        self.ref_speed = ref_speed * self.cps_2_kph

        self.last_called = time.time()

        #  init the pulse buffer with pulses one second apart
        self.timing_buff = collections.deque(maxlen=10)
        for i in range(10):
            self.timing_buff.append(self.last_called+i)

        error_code = wiringpi.wiringPiSetupGpio()
        if error_code != 0:
            err_message = "Cannot setup wiringPi: {}".format(error_code)
            self._logger.error(err_message)
            raise OSError(err_message)
        self._logger.info("wiringpi gpio setup successful")
        wiringpi.pinMode(self.pin, wiringpi.GPIO.INPUT)
        self._logger.info(
            "wiringpi pin %s set to GPIO input",
            self.pin)

        wiringpi.pullUpDnControl(self.pin, wiringpi.GPIO.PUD_UP)
        self._logger.info(
            "wiringpi pin %s set to GPIO pull-up set",
            self.pin)

        wiringpi.wiringPiISR(
            self.pin, wiringpi.GPIO.INT_EDGE_FALLING,
            self._filter_callback)

        self._logger.info(
            "wiringpi pin %s set to GPIO ISR edge: %s",
            self.pin,  wiringpi.GPIO.INT_EDGE_FALLING)

        self._logger.info("Instantiation successful")

    def _filter_callback(self, debounce_time: float = 0.1) -> None:
        """ debouncing filter
        Only trigger if time since last trigger is more that
        debounce_time (in seconds)
            Args:
            debounce_time (float): the minimum time (in seconds) required between triggers (default 0.1s)
        """
        self._logger.debug("ISR filter callback triggered")
        now = time.time()
        dt = now-self.last_called
        if dt > debounce_time:
            self._logger.debug('pulse detected')
            self.timing_buff.append(now)
        self.last_called = time.time()

    def get_speed(self) -> float:
        # speed in cps
        speed = 10 / (self.timing_buff[9]-self.timing_buff[0])
        self._logger.debug("speed: {speed} CpS")
        # convert speed to kph
        speed = self.cps_2_kph*speed
        self._logger.debug("speed: {speed} km/h")
        # speed as percent of target
        self._logger.debug("speed: {speed/self.ref_speed} % of target")
        return speed

