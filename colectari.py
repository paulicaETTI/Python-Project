#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- coding: future_fstrings -*-

# Created on Noiembrie 4, 2021
# @author: popai-pc

import serial
import time
from threading import Thread, Event, Semaphore
from copy import copy
from queue import Queue
from dependinte.db_create import table_colectare, table_tagClient, db, engine
from dependinte.nmeastreamer import NMEAStreamer
from dependinte.sz_gpio import *
# from dependinte.loggers import get_logger
from dependinte.log import log
# XXX stabilim nivelul de loguri afisate, into_log_file=None e defoult, nu fogam in fisier doar in std.out
from logging import INFO, WARNING, ERROR

# log_file = "/home/auto/Log/logfile_col.log"
# log = get_logger(name="rfid_col", level=INFO, into_log_file=log_file)
log.setLevel(INFO)

# coduri
START = b'\x02'  # defineste strtul framului rs485 de la antena
STOP = b'\x03'  # defineste sfrsirul framului rs485 de la antena

# defineste codurile pentru partea in care avem recipient scrise in DB
# parte_id = {STANGA: 1, DREAPTA: 2, CENTRU: 3}


# greutate_up_id = {'L': 0, 'R': 0, 'T': 0}
# g_sum = 0

# XXX Dfinire Evenimente in db coloana evenimente
#   1 -> Fara tag
#   2 -> Tgaul nu exista in db
#   3 -> Tg neplatit
#   4 -> Tip gunoi gresit
#   5 -> colectare OK fara evenimente
#   6 -> System UP, nu este folosit in acest script
eveniment = {
    "far_tag": 1,
    "nu_e_in_db": 2,
    "neplatit": 3,
    "tip_gunoi_gresit": 4,
    "fara_eveniment": 5
}


def get_pi_id():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        # f = open('cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except FileNotFoundError:
        cpuserial = "ERROR000000000"
    return cpuserial


ID_MASINA = get_pi_id()

# XXX initializam colectare cu valorile implicite
pubela_init = {
    'id_masina': ID_MASINA,
    'id_tag': 0,
    'tag_code': "",
    'colectat': 1,
    'lat': "00.0000",
    'lon': "00.00000",
    'eveniment': eveniment["fara_eveniment"],
    'parte': 2
}


def CheckSum(uBuff):
    # c function on microcontroler
    # byte CheckSum(char *uBuff, int uBuffLen)
    # {
    #     byte i, uSum = 0;
    #     for (i = 0; i < uBuffLen; i++)
    #     {
    #         uSum = uSum + uBuff[i];
    #     }
    #     uSum = (~uSum) + 1;
    #     return uSum;
    # }

    r = 0x0000
    for c in uBuff:
        r += c
        if r > 255:
            r %= 256
    # log.info(bin(r & 0x00ff))
    r = (~r & 0xff) + 1

    # log.info(hex(r & 0xf0))
    return bytes([r])


storage = Queue()  # retine datele citite la serial


# serial_stopevent = Event()

def get_serial_data(ser):
    """
    Citeste datele de la antena
    returneaza datele citite
    """
    read_data = set()  # retinem citiri unuce
    # clear_data_time = time.time()
    # while not serial_stopevent.is_set():
    while 1:
        try:
            ser.reset_input_buffer()
            serial_data = ser.read(1)
            if serial_data == START:
                serial_data += ser.read_until(expected=STOP, size=50)
            if len(serial_data) > 1:
                crc = ser.read(1)
                log.info(f"{serial_data}")
                log.info(f"CRC read: {crc}")
                log.info(f"CRC calc: {CheckSum(serial_data)}")

                if CheckSum(serial_data) == crc:
                    log.info(f"SERIAL_READ_DATA: {serial_data} \n")
                    if serial_data not in read_data:
                        storage.put(serial_data)
                        read_data.add(serial_data)
                        av_semaphre.release()
            if read_data.__len__() > 10:
                read_data.clear()
            time.sleep(0.1)
        except Exception as e:
            log.error(f"eroare in get_serial_data(): {str(e)}")
            break
    log.warning("Serial port thread terminate...")
    ser.close()
    time.sleep(0.5)


def tag_from_db(_tag):
    """ luam tagul din DB daca exista, altfel NULL"""
    with engine.connect() as connection:
        query = db.select([table_tagClient]).where(table_tagClient.c.tag_code == _tag)
        # query = f"SELECT * FROM {table_tagClient} where tag_code = {_tag}"
        result = connection.execute(query).fetchone()
    return result


def scrie_in_db(table_raw):
    """ inregistram in DB colectarea """
    with engine.connect() as connection:
        query = db.insert(table_colectare)
        result = connection.execute(query, table_raw)
    return result


# XXX *************************************

# def verificare_tag(serial_in):
#     """
#     verifica tagul primit in serial_in daca e in DB si dam avertizari corespunzatoare
#     """
#     log.info("\n********************************************************  VERIFIC TAG  **************************************")
#     # end_tag = serial_in.find(b'\x03')
#     # tag = serial_in[3:end_tag].decode('UTF-8')
#     tag = serial_in[3:27].decode('UTF-8')
#     log.info(tag)
#     tag_db = tag_from_db(tag)
#     # log.info("TAG IN DB:", tag_db)
#     if tag_db:
#         if tag_db.status == 0:
#             avertizare_therad(serial_in, eveniment["neplatit"])

#         elif tag_db.valid == 0:
#             avertizare_therad(serial_in, eveniment["tip_gunoi_gresit"])

#     else:
#         avertizare_therad(serial_in, eveniment["nu_e_in_db"])
#     log.info('\n')


# old_tag,dictionar  retine ultimul tag pe partea corespunzatoare
# old_tag = {STANGA: '', DREAPTA: ''}
# old_tag = set()
# time_citiri_tag = time.time() # pentru timp resetare old_tag


def colectare(tag_in):
    """
    populeaza campurile din pubela si inregisteaza pubela primit in DB
    """
    log.info(
        "\n*********************************************************  CEOLECTARE  ****************************************")
    # global time_citiri_tag
    # global old_tag
    coord = gps.get_data()

    log.info(f"tag curent: {tag_in}")
    pubela = copy(pubela_init)
    pubela['lat'] = coord["latitude"]
    pubela['lon'] = coord["longitude"]
    pubela['tag_code'] = tag_in
    tag_db = tag_from_db(tag_in)

    if tag_db:
        # log.info("TAG IN DB:", {tag_db})
        pubela['id_tag'] = tag_db.Id
        if tag_db.status == 0:
            pubela['eveniment'] = eveniment["neplatit"]  # "neplatit":  # setings_local.tip_gunoi:
        elif tag_db.valid == 0:
            pubela['eveniment'] = eveniment["tip_gunoi_gresit"]  # "tip gunoi gresit":
    else:
        pubela['eveniment'] = eveniment["nu_e_in_db"]  # "tag nu exista in db"

    scrie_in_db(pubela)
    log.info(f"PUBELA INSERATA: {pubela}")
    pubela.clear()


def storage_proces(storage_q):
    nr_tag = 0
    while True:
        if storage_q.empty():
            if nr_tag == 0:
                log.info(f"ISERT ERROR")
                nr_tag += 1
            break
        else:
            nr_tag += 1
            serial_in = storage_q.get()
            log.info(f"QUE TAG: {serial_in}")
            tag = serial_in[2:-1].decode('UTF-8')
            colectare(tag)
            if tag_from_db(tag) != None:
                break


if __name__ == '__main__':
    try:

        log.info(
            F"\r\npin_senzor_D = {GPIO.input(pin_sensor_right)}\r\npin_senzor_S = {GPIO.input(pin_sensor_left)}\r\npin_senzor_ELM = {GPIO.input(pin_sensor_ELM)}\r\n")

        # setam portul pentru serial si pornim threadul de comunicarea cu IO-ul
        rs485_port = '/dev/ttyS2'
        rs485_baud = 9600
        # ser = serial.Serial(rs485_port, rs485_baud, timeout=0.05)
        ser = serial.Serial(rs485_port, rs485_baud, timeout=None)
        # ser = serial.Serial(port='/dev/ttyS2', baudrate=57600, parity=serialog.PARITY_NONE, stopbits=serialog.STOPBITS_ONE,
        #                     bytesize=serialog.EIGHTBITS, xonxoff=False, rtscts=False, dsrdtr=False, timeout=5)
        log.info(F"Connecting to serial port {rs485_port} at {rs485_baud} baud...")
        log.info("Starting RS485 reader thread...\n")
        serial_thread = Thread(name="Serial_IO", target=get_serial_data, args=(ser,), daemon=True)
        serial_thread.start()
        log.info(F"Starting avertizare thread")
        # av_thread = Thread(name="Serial_IO", target=avertizare, args=(pin_sensor_ELM,2), daemon=True)
        # av_thread.start()

        # setam portul si pornim threadul pentru GPS
        gps_port = "/dev/modemGPS"
        gps_baudrate = 115200
        # gps_timeout = 0.1
        gps_timeout = None
        gps = NMEAStreamer(gps_port, gps_baudrate, gps_timeout)
        if gps.connect():
            gps.start_read_thread()

        # astept GPS-ul
        # for _ in range(30):
        #     coord = gps.get_data()
        #     if coord["latitude"]:
        #         break
        #     time.sleep(0.5)
        lift_up_left, lift_up_right = False, False
        colect_st, colect_dr = True, True
        while 1:
            try:
                if not gps.is_alive():
                    if gps.connect():
                        gps.start_read_thread()
                        log.error("New GPS streamer thread...")
                    time.sleep(1)
                if not serial_thread.is_alive():
                    ser.open()
                    serial_data = Thread(name="Serial_IO", target=get_serial_data, args=(ser,), daemon=True)
                    serial_data.start()
                    log.error("New Serial IO thread...")
                    time.sleep(1)

                lift_up_left, lift_up_right = lift_up(lift_up_left, lift_up_right)
                log.info(f"st dr state: {sz_left_on()} {sz_right_on()}     {lift_up_left} {lift_up_right}")
                if sz_left_on() and lift_up_left and colect_st:
                    storage_proces(storage)
                    colect_st = False
                if not sz_left_on():
                    lift_up_left = False
                    colect_st = True

                if sz_right_on() and lift_up_right and colect_dr:
                    storage_proces(storage)
                    colect_dr = False
                if not sz_right_on():
                    lift_up_right = False
                    colect_dr = True

                time.sleep(0.5)
            except Exception as e:
                log.error(f"EROARE GENERALA !!!!! {str(e)}")
                break
        raise KeyboardInterrupt
    except:
        log.error('colectare script killed')
        GPIO.cleanup()
        gps.stop_read_thread()
        time.sleep(1)  # wait for shutdown
        gps.disconnect()
        # av_stopevent.set()
        ser.close()
        log.error("\n\nMain Thread Terminated\n\n")
