# -*- coding: utf-8 -*-

import time
import bisect
import logging
import collections

import pigpio

from statistics import mean
from typing import Callable


class WheelSensor:
    """Wheel sensor class handles speed and gpio access
    """

    def __init__(self,
                 callback: Callable,
                 pin: int = 21,
                 radius: float = .311,  # for 700cc
                 ref_speed: float = 20.0) -> None:
        """
        init

        Args:
            callback (function): callback function wheel rotation detection this is called on every detected pusle with agrument of wheel speed %
            pin (int): the GPIO pin number for the reed switch (default pin 29)
            radius (float): The wheel radius in m (default 311mm)
            ref_speed (float): the reference speed in km/h
        """

        self._logger = logging.getLogger(__name__)
        # logging.basicConfig(level=logging.DEBUG)

        self.pin = pin
        self.callback = callback

        # wheel circumference
        self.circumference = 2 * 3.14 * (radius)
        # convert km/h to wheel circumferences per second
        self.kph_2_cps = 1000. / (60 * 60 * self.circumference)
        self.cps_2_kph = 1. / self.kph_2_cps

        # set reference speed in cps
        self.inv_ref_speed = 1 / (ref_speed * self.kph_2_cps)
        self._logger.info(
            "ref speed of %s cps", 1 / self.inv_ref_speed)
        self.last_called = time.time()
        #  init the pulse buffer with pulses one second apart
        self.time_len = 20
        self.timing_buff = collections.deque(maxlen=self.time_len)
        # init with dt's matching ref. speed
        for i in range(self.time_len, 0, -1):
            self.timing_buff.append(self.last_called - i*self.inv_ref_speed)

        # GPIO
        self.gpio = pigpio.pi()
        # set to input
        self.gpio.set_mode(self.pin, pigpio.INPUT)
        self._logger.info(
            "pin %s set to GPIO input",
            self.pin)
        # activate internal pull-up resistor
        self.gpio.set_pull_up_down(self.pin, pigpio.PUD_UP)

        self._logger.info(
            "pin %s set to GPIO pull-up",
            self.pin)

        self.pi_callback_handle = self.gpio.callback(self.pin, pigpio.FALLING_EDGE, self._filter_callback)

        self._logger.info(
            "callback on  pin %s falling edge set",
            self.pin)

        self._logger.info("Instantiation successful")

    def _filter_callback(self, gpio, level, tick) -> None:
        """ debouncing filter
        Only trigger if time since last trigger is more that
        debounce_time (in seconds)
            Args:
            debounce_time (float): the minimum time (in seconds) required between triggers (default 0.1s)
        """
        # confirm the context is ok (right pin, level change to 0)
        if (gpio == self.pin and level == 0):
            # self._logger.debug("ISR filter callback triggered")
            debounce_time: float = 0.1
            now = time.time()
            dt = now - self.last_called
            if dt > debounce_time:
                self._logger.debug('pulse detected')
                self.timing_buff.append(now)
                self.callback(self.get_speed())

            self.last_called = time.time()

    def get_speed(self) -> float:
        """Get wheel speed as time elapsed for the last 20 pulses

        Returns:
            float: wheel speed ratio with reference
        """
        # speed in cps
        speed = 20 / (self.timing_buff[-1] - self.timing_buff[0])
        self._logger.debug(f"speed: {speed} CpS")
        # speed as percent of target
        self._logger.debug(f"speed: {speed*self.inv_ref_speed} % of target")
        return speed * self.inv_ref_speed

    def get_speed2(self) -> float:
        """Compute speed as number pulses in the last 5s

        Returns:
            float: wheel speed ratio with reference
        """
        inv_dt = 0.20
        now = time.time()
        i = bisect.bisect_left(self.timing_buff, now-5)
        speed = (self.time_len-i)*inv_dt
        return speed * self.inv_ref_speed

