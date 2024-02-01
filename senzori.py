#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- coding: future_fstrings -*-

# Created on Janry 30 2023
# @author: popai-pc

import time
from threading import Event, Semaphore
# import RPi.GPIO as GPIO
import OPi.GPIO as GPIO
import orangepi.zeroplus2
from .log import log
# XXX stabilim nivelul de loguri afisate, into_log_file=None e defoult, nu fogam in fisier doar in std.out
from logging import INFO, WARNING, ERROR

# log_file = "/home/auto/Log/logfile_col.log"
# log = get_logger(name="rfid_col", level=INFO, into_log_file=log_file)
log.setLevel(INFO)
GPIO.cleanup()
pin_sensor_right = 22  # 16
pin_sensor_left = 24  # 18
pin_sensor_ELM = 18  # 18
GPIO.setmode(orangepi.zeroplus2.BOARD)
GPIO.setwarnings(False)

GPIO.setup(pin_sensor_left, GPIO.IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_sensor_right, GPIO.IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_sensor_ELM, GPIO.IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(pin_sensor_ELM, GPIO.OUT)
# GPIO.output(pin_sensor_ELM, GPIO.LOW)
# GPIO.output(pin_sensor_right, GPIO.LOW)


TIME_ON_OFF = 2  # time to pase to activate on or of state
sz_left_state = False  # state of left sensor
time_sz_left_on = time.time()  # initial time for on state
time_sz_left_off = time.time()  # initial time for off state


def sz_left_on():
    global sz_left_state
    global time_sz_left_on
    global time_sz_left_off

    if GPIO.input(pin_sensor_left) == 0:
        time_sz_left_off = time.time()
        if time_sz_left_off - time_sz_left_on > TIME_ON_OFF:
            sz_left_state = False
    if GPIO.input(pin_sensor_left) == 1:
        time_sz_left_on = time.time()
        if time_sz_left_on - time_sz_left_off > TIME_ON_OFF:
            sz_left_state = True
    # log.info(f"ST TIME ON OFF: {time_sz_left_on} {time_sz_left_off}")
    return sz_left_state


sz_right_state = False
time_sz_right_on = time.time()
time_sz_right_off = time.time()


def sz_right_on():
    global sz_right_state
    global time_sz_right_on
    global time_sz_right_off

    if GPIO.input(pin_sensor_right) == 0:
        time_sz_right_off = time.time()
        if time_sz_right_off - time_sz_right_on > TIME_ON_OFF:
            sz_right_state = False

    if GPIO.input(pin_sensor_right) == 1:
        time_sz_right_on = time.time()
        if time_sz_right_on - time_sz_right_off > TIME_ON_OFF:
            sz_right_state = True
    # log.info(f"DR TIME ON OFF: {time_sz_right_on} {time_sz_right_on}")
    return sz_right_state


# LIFT_UP = False
def lift_up(up_st: bool, up_dr: bool):
    if GPIO.input(pin_sensor_ELM) == 0:
        up_st = True
        up_dr = True
    return up_st, up_dr


av_semaphre = Semaphore(value=0)
av_stopevent = Event()


# XXX ***********AVERTIZARE**************
def avertizare(pin, nr_lop):
    """
    seteaza pin GPIO UP/DOWN de nr_lop ori
    """
    while not av_stopevent.is_set():
        av_semaphre.acquire()
        for _ in range(nr_lop):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.3)
