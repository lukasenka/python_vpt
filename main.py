import datetime
import requests
import random

from tkinter import *
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError
from operator import attrgetter
from klases import Darbuotojas
from statistics import mean, median

sarasas = []
apz_sarasas = []
data = []

engine = create_engine("sqlite:///darbuotojai.db")
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    try:
        create_tables.status.destroy()
    except AttributeError:
        pass

    watch.i = 10

    try:
        vardas = iterpti.laukelis_iterpti_vardas.get()
        pavarde = iterpti.laukelis_iterpti_pavarde.get()

        gimimo_data = datetime.datetime.strptime(iterpti.laukelis_iterpti_gimimo_data.get(), "%Y-%m-%d").date()

        pareigos = iterpti.laukelis_iterpti_pareigos.get()
        atlyginimas = iterpti.laukelis_iterpti_atlyginimas.get()
        db = Darbuotojas(vardas, pavarde, gimimo_data, pareigos, atlyginimas)
        session.add(db)
        session.commit()
        status = Label(langas, text="---------- Irasas sukurtas ----------")
        status.grid(row=watch.i + 1, column=0)
        sarasas.append(status)
        create_tables.status = status

    except ValueError:
        status = Label(langas, text="[SUKURTI LENTELES - KLAIDA] Neteisingas gimimo dienos formatas"
                                    ". Turi buti pvz: 2022-01-22")
        status.grid(row=watch.i + 1, column=0)
        sarasas.append(status)
        create_tables.status = status


def watch():
    try:
        delete_table.uzrasas_irasas_istrinta.destoy()
        delete_table.uzrasas_irasas_istrinta_klaida.destroy()
        update_table.uzrasas_irasas_atnaujintas.destroy()
        update_table.uzrasas_irasas_atnaujintas.destroy()
        play_apz_start.uzrasas_choose_apz_klaida.destroy()
        play_apz_start.uzrasas_choose_apz.destroy()
        play_apz_start.uzrasas_choose_apz_lygiosios.destroy()
        play_apz_start.uzrasas_choose_apz_akmuo.destroy()
        play_apz_start.uzrasas_choose_apz_akmuo2.destroy()
        play_apz_start.uzrasas_choose_apz_popierius.destroy()
        play_apz_start.uzrasas_choose_apz_popierius2.destroy()
        play_apz_start.uzrasas_choose_apz_zirkles.destroy()
        play_apz_start.uzrasas_choose_apz_zirkles2.destroy()
    except AttributeError:
        pass

    i = 10  # esamu naudojamu eiluciu kiekis

    darbuotojai = session.query(Darbuotojas).all()

    for darbuotojas in darbuotojai:
        i += 1
        apacia = Label(langas, text=f"{darbuotojas}")
        apacia.grid(row=i, column=0)
        sarasas.append(apacia)  # itraukiam ciklo elementus i sarasa
    watch.i = i


def edit():
    # sunaikinam langelius
    for label in sarasas:
        label.destroy()  # naikinam is ciklo visus label

    for label in apz_sarasas:
        label.destroy()

    # ---------------------------------------------------
    uzrasas_redaguoti = Label(langas, text="Iveskite asmens ID kuri norite redaguoti:")
    laukelis_redaguoti = Entry(langas, validate="key", validatecommand=(validation, '%S'))
    sarasas.append(uzrasas_redaguoti)
    # sarasas.append(laukelis_redaguoti)

    mygtukas_redaguoti = Button(langas, text="Patvirtinti", command=edit_table)
    sarasas.append(mygtukas_redaguoti)
    uzrasas_redaguoti.grid(row=0, column=0)
    laukelis_redaguoti.grid(row=1, column=0)
    mygtukas_redaguoti.grid(row=2, column=0)

    edit.laukelis_redaguoti = laukelis_redaguoti


def istrinti():
    # sunaikinam langelius

    for label in sarasas:
        label.destroy()  # naikinam is ciklo visus label

    for label in apz_sarasas:
        label.destroy()

    try:
        edit.laukelis_redaguoti.destroy()
    except AttributeError:
        pass

    uzrasas_istrinti = Label(langas, text="Iveskite asmens ID kuri norite pasalinti:")
    laukelis_istrinti = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_istrinti)
    sarasas.append(laukelis_istrinti)

    mygtukas_istrinti = Button(langas, text="Patvirtinti", command=delete_table)

    sarasas.append(mygtukas_istrinti)

    uzrasas_istrinti.grid(row=0, column=0)
    laukelis_istrinti.grid(row=1, column=0)
    mygtukas_istrinti.grid(row=2, column=0)

    istrinti.laukelis_istrinti = laukelis_istrinti
    istrinti.mygtukas_istrinti = mygtukas_istrinti


def delete_table():
    run_try()

    try:

        watch.i = 2

        ivedimas = istrinti.laukelis_istrinti.get()

        trinam = session.query(Darbuotojas).get(ivedimas)
        session.delete(trinam)
        session.commit()

        uzrasas_irasas_istrinta = Label(langas, text="---------- Irasas panaikintas ----------")

        sarasas.append(uzrasas_irasas_istrinta)

        uzrasas_irasas_istrinta.grid(row=watch.i + 4, column=0)

        delete_table.uzrasas_irasas_istrinta = uzrasas_irasas_istrinta

        watch()

    except (AttributeError, UnmappedInstanceError):

        ivedimas = istrinti.laukelis_istrinti.get()

        uzrasas_irasas_istrinta_klaida = Label(langas, text=f"[KLAIDA] Iraso {ivedimas} bazeje nera.")

        sarasas.append(uzrasas_irasas_istrinta_klaida)

        uzrasas_irasas_istrinta_klaida.grid(row=watch.i + 4, column=0)

        delete_table.uzrasas_irasas_istrinta_klaida = uzrasas_irasas_istrinta_klaida


def run_try():
    try:
        delete_table.uzrasas_irasas_istrinta.destoy()
        delete_table.uzrasas_irasas_istrinta_klaida.destroy()
    except AttributeError:
        pass


def edit_table():
    # sunaikinam langelius

    for label in sarasas:
        label.destroy()  # naikinam is ciklo visus label

    for label in apz_sarasas:
        label.destroy()

    uzrasas_redaguoti_vardas = Label(langas, text="Iveskite varda:")
    laukelis_redaguoti_vardas = Entry(langas)

    sarasas.append(uzrasas_redaguoti_vardas)
    sarasas.append(laukelis_redaguoti_vardas)

    uzrasas_redaguoti_pavarde = Label(langas, text="Iveskite pavarde:")
    laukelis_redaguoti_pavarde = Entry(langas)

    sarasas.append(uzrasas_redaguoti_pavarde)
    sarasas.append(laukelis_redaguoti_pavarde)

    uzrasas_redaguoti_gimimo_metai = Label(langas, text="Iveskite gimimo metus:")
    laukelis_redaguoti_gimimo_metai = Entry(langas)

    sarasas.append(uzrasas_redaguoti_gimimo_metai)
    sarasas.append(laukelis_redaguoti_gimimo_metai)

    uzrasas_redaguoti_pareigos = Label(langas, text="Iveskite pareigas:")
    laukelis_redaguoti_pareigos = Entry(langas)

    sarasas.append(uzrasas_redaguoti_pareigos)
    sarasas.append(laukelis_redaguoti_pareigos)

    uzrasas_redaguoti_atlyginimas = Label(langas, text="Iveskite atlyginima:")
    laukelis_redaguoti_atlyginimas = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_redaguoti_atlyginimas)
    sarasas.append(laukelis_redaguoti_atlyginimas)

    mygtukas_redaguoti_patvirtinti = Button(langas, text="Patvirtinti", command=update_table)

    sarasas.append(mygtukas_redaguoti_patvirtinti)

    uzrasas_redaguoti_vardas.grid(row=0, column=0)
    laukelis_redaguoti_vardas.grid(row=1, column=0)

    uzrasas_redaguoti_pavarde.grid(row=2, column=0)
    laukelis_redaguoti_pavarde.grid(row=3, column=0)

    uzrasas_redaguoti_gimimo_metai.grid(row=4, column=0)
    laukelis_redaguoti_gimimo_metai.grid(row=5, column=0)

    uzrasas_redaguoti_pareigos.grid(row=6, column=0)
    laukelis_redaguoti_pareigos.grid(row=7, column=0)

    uzrasas_redaguoti_atlyginimas.grid(row=8, column=0)
    laukelis_redaguoti_atlyginimas.grid(row=9, column=0)

    mygtukas_redaguoti_patvirtinti.grid(row=10, column=0)

    edit_table.laukelis_redaguoti_vardas = laukelis_redaguoti_vardas
    edit_table.laukelis_redaguoti_pavarde = laukelis_redaguoti_pavarde
    edit_table.laukelis_redaguoti_gimimo_metai = laukelis_redaguoti_gimimo_metai
    edit_table.laukelis_redaguoti_pareigos = laukelis_redaguoti_pareigos
    edit_table.laukelis_redaguoti_atlyginimas = laukelis_redaguoti_atlyginimas


def update_table():
    try:
        update_table.uzrasas_irasas_atnaujintas.destroy()
        update_table.uzrasas_irasas_atnaujintas.destroy()
    except AttributeError:
        pass

    ivedimas = edit.laukelis_redaguoti.get()
    r_darbuotojas = session.query(Darbuotojas).get(ivedimas)

    try:

        if len(edit_table.laukelis_redaguoti_vardas.get()) != 0:
            r_darbuotojas.vardas = edit_table.laukelis_redaguoti_vardas.get()

            uzrasas_irasas_atnaujintas = Label(langas, text=f"---------- Irasas atnaujintas ----------")
            uzrasas_irasas_atnaujintas.grid(row=11, column=0)

            sarasas.append(uzrasas_irasas_atnaujintas)

            update_table.uzrasas_irasas_atnaujintas = uzrasas_irasas_atnaujintas

            watch()

        if len(edit_table.laukelis_redaguoti_pavarde.get()) != 0:

            r_darbuotojas.pavarde = edit_table.laukelis_redaguoti_pavarde.get()

            uzrasas_irasas_atnaujintas = Label(langas, text=f"---------- Irasas atnaujintas ----------")
            uzrasas_irasas_atnaujintas.grid(row=11, column=0)

            sarasas.append(uzrasas_irasas_atnaujintas)

            update_table.uzrasas_irasas_atnaujintas = uzrasas_irasas_atnaujintas

            watch()

        if len(edit_table.laukelis_redaguoti_gimimo_metai.get()) != 0:

            r_darbuotojas.gimimo_data = datetime.datetime.strptime(edit_table.laukelis_redaguoti_gimimo_metai.get(), "%Y-%m-%d").date()

            uzrasas_irasas_atnaujintas = Label(langas, text=f"---------- Irasas atnaujintas ----------")
            uzrasas_irasas_atnaujintas.grid(row=11, column=0)

            sarasas.append(uzrasas_irasas_atnaujintas)

            update_table.uzrasas_irasas_atnaujintas = uzrasas_irasas_atnaujintas

            watch()

        if len(edit_table.laukelis_redaguoti_pareigos.get()) != 0:

            r_darbuotojas.pareigos = edit_table.laukelis_redaguoti_pareigos.get()

            uzrasas_irasas_atnaujintas = Label(langas, text=f"---------- Irasas atnaujintas ----------")
            uzrasas_irasas_atnaujintas.grid(row=11, column=0)

            sarasas.append(uzrasas_irasas_atnaujintas)

            update_table.uzrasas_irasas_atnaujintas = uzrasas_irasas_atnaujintas

            watch()

        if len(edit_table.laukelis_redaguoti_atlyginimas.get()) != 0:

            r_darbuotojas.atlyginimas = float(edit_table.laukelis_redaguoti_atlyginimas.get())

            uzrasas_irasas_atnaujintas = Label(langas, text=f"---------- Irasas atnaujintas ----------")
            uzrasas_irasas_atnaujintas.grid(row=11, column=0)

            sarasas.append(uzrasas_irasas_atnaujintas)

            update_table.uzrasas_irasas_atnaujintas = uzrasas_irasas_atnaujintas

            watch()

    except AttributeError:

        uzrasas_irasas_atnaujintas_klaida = Label(langas, text=f"[KLAIDA] Iraso {ivedimas} bazeje nera.")
        uzrasas_irasas_atnaujintas_klaida.grid(row=11, column=0)

        sarasas.append(uzrasas_irasas_atnaujintas_klaida)

        update_table.uzrasas_irasas_atnaujintas_klaida = uzrasas_irasas_atnaujintas_klaida

    session.commit()


def timedelta_add():
    for label in sarasas:
        label.destroy()  # naikinam is ciklo visus label

    for label in apz_sarasas:
        label.destroy()

    try:
        filter_gimimo_data.laukelis_paieska_gimimo_data.destroy()
        filter_gimimo_data.labelis_paieska_gimimo_data.destroy()
        filter_gimimo_data.mygtukas_paieska_gimimo_data.destroy()

        filter_atlyginimas.laukelis_paieska_atlyginimas.destroy()
        filter_atlyginimas.mygtukas_paieska_atlyginimas.destroy()
        filter_atlyginimas.labelis_paieska_atlyginimas.destroy()
    except AttributeError:
        pass


    uzrasas_add_timedelta = Label(langas, text="Iveskite asmens ID kurio data norite redaguoti:")
    laukelis_add_timedelta = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_timedelta)
    # sarasas.append(laukelis_add_timedelta)

    mygtukas_add_timedelta = Button(langas, text="Patvirtinti", command=timedelta_add_x)

    sarasas.append(mygtukas_add_timedelta)

    uzrasas_add_timedelta.grid(row=0, column=0)
    laukelis_add_timedelta.grid(row=1, column=0)
    mygtukas_add_timedelta.grid(row=2, column=0)

    timedelta_add.laukelis_add_timedelta = laukelis_add_timedelta


def timedelta_add_x():
    for label in sarasas:
        label.destroy()  # naikinam is ciklo visus label

    for label in apz_sarasas:
        label.destroy()

    uzrasas_add_savaites = Label(langas, text="Iveskite savaites:")
    laukelis_add_savaites = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_savaites)
    sarasas.append(laukelis_add_savaites)

    uzrasas_add_dienos = Label(langas, text="Iveskite dienas:")
    laukelis_add_dienos = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_dienos)
    sarasas.append(laukelis_add_dienos)

    uzrasas_add_valandos = Label(langas, text="Iveskite valandas:")
    laukelis_add_valandos = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_valandos)
    sarasas.append(laukelis_add_valandos)

    uzrasas_add_minutes = Label(langas, text="Iveskite minutes:")
    laukelis_add_minutes = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_minutes)
    sarasas.append(laukelis_add_minutes)

    uzrasas_add_sekundes = Label(langas, text="Iveskite sekundes:")
    laukelis_add_sekundes = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_sekundes)
    sarasas.append(laukelis_add_sekundes)

    uzrasas_add_milisekundes = Label(langas, text="Iveskite milisekundes:")
    laukelis_add_milisekundes = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_milisekundes)
    sarasas.append(laukelis_add_milisekundes)

    uzrasas_add_mikrosekundes = Label(langas, text="Iveskite mikrosekundes:")
    laukelis_add_mikrosekundes = Entry(langas, validate="key", validatecommand=(validation, '%S'))

    sarasas.append(uzrasas_add_mikrosekundes)
    sarasas.append(laukelis_add_mikrosekundes)

    mygtukas_add_timedelta_patvirtinti = Button(langas, text="Patvirtinti", command=timedelta_table_add_update)

    sarasas.append(mygtukas_add_timedelta_patvirtinti)

    uzrasas_add_savaites.grid(row=0, column=0)
    laukelis_add_savaites.grid(row=1, column=0)

    uzrasas_add_dienos.grid(row=2, column=0)
    laukelis_add_dienos.grid(row=3, column=0)

    uzrasas_add_valandos.grid(row=4, column=0)
    laukelis_add_valandos.grid(row=5, column=0)

    uzrasas_add_minutes.grid(row=6, column=0)
    laukelis_add_minutes.grid(row=7, column=0)

    uzrasas_add_sekundes.grid(row=8, column=0)
    laukelis_add_sekundes.grid(row=9, column=0)

    uzrasas_add_milisekundes.grid(row=10, column=0)
    laukelis_add_milisekundes.grid(row=11, column=0)

    uzrasas_add_mikrosekundes.grid(row=12, column=0)
    laukelis_add_mikrosekundes.grid(row=13, column=0)

    mygtukas_add_timedelta_patvirtinti.grid(row=14, column=0)

    timedelta_add_x.laukelis_add_savaites = laukelis_add_savaites
    timedelta_add_x.laukelis_add_dienos = laukelis_add_dienos
    timedelta_add_x.laukelis_add_valandos = laukelis_add_valandos
    timedelta_add_x.laukelis_add_minutes = laukelis_add_minutes
    timedelta_add_x.laukelis_add_sekundes = laukelis_add_sekundes
    timedelta_add_x.laukelis_add_milisekundes = laukelis_add_milisekundes
    timedelta_add_x.laukelis_add_mikrosekundes = laukelis_add_mikrosekundes


def timedelta_table_add_update():
    try:
        timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas.destroy()
        timedelta_table_add_update.uzrasas_add_timetable_atnaujintas_klaida.destroy()
    except AttributeError:
        pass


    ivedimas = timedelta_add.laukelis_add_timedelta.get()
    r_darbuotojas = session.query(Darbuotojas).get(ivedimas)

    try:

        if len(timedelta_add_x.laukelis_add_savaites.get()) != 0:
            datax = r_darbuotojas.created_date
            savaites = timedelta_add_x.laukelis_add_savaites.get()
            rez = datax + datetime.timedelta(weeks=int(savaites))

            r_darbuotojas.created_date = rez

            uzrasas_add_timedelta_atnaujintas = Label(langas, text="---------- Irasas atnaujintas ----------")
            uzrasas_add_timedelta_atnaujintas.grid(row=15, column=0)

            sarasas.append(uzrasas_add_timedelta_atnaujintas)

            timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas = uzrasas_add_timedelta_atnaujintas

        if len(timedelta_add_x.laukelis_add_dienos.get()) != 0:
            datax = r_darbuotojas.created_date
            dienos = timedelta_add_x.laukelis_add_dienos.get()
            rez = datax + datetime.timedelta(days=int(dienos))

            r_darbuotojas.created_date = rez

            uzrasas_add_timedelta_atnaujintas = Label(langas, text="---------- Irasas atnaujintas ----------")
            uzrasas_add_timedelta_atnaujintas.grid(row=15, column=0)

            sarasas.append(uzrasas_add_timedelta_atnaujintas)

            timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas = uzrasas_add_timedelta_atnaujintas

        if len(timedelta_add_x.laukelis_add_valandos.get()) != 0:
            datax = r_darbuotojas.created_date
            valandos = timedelta_add_x.laukelis_add_valandos.get()
            rez = datax + datetime.timedelta(hours=int(valandos))

            r_darbuotojas.created_date = rez

            uzrasas_add_timedelta_atnaujintas = Label(langas, text="---------- Irasas atnaujintas ----------")
            uzrasas_add_timedelta_atnaujintas.grid(row=15, column=0)

            sarasas.append(uzrasas_add_timedelta_atnaujintas)

            timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas = uzrasas_add_timedelta_atnaujintas

        if len(timedelta_add_x.laukelis_add_minutes.get()) != 0:
            datax = r_darbuotojas.created_date
            minutes = timedelta_add_x.laukelis_add_minutes.get()
            rez = datax + datetime.timedelta(minutes=int(minutes))

            r_darbuotojas.created_date = rez

            uzrasas_add_timedelta_atnaujintas = Label(langas, text="---------- Irasas atnaujintas ----------")
            uzrasas_add_timedelta_atnaujintas.grid(row=15, column=0)

            sarasas.append(uzrasas_add_timedelta_atnaujintas)

            timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas = uzrasas_add_timedelta_atnaujintas

        if len(timedelta_add_x.laukelis_add_sekundes.get()) != 0:
            datax = r_darbuotojas.created_date
            sekundes = timedelta_add_x.laukelis_add_sekundes.get()
            rez = datax + datetime.timedelta(seconds=int(sekundes))

            r_darbuotojas.created_date = rez

            uzrasas_add_timedelta_atnaujintas = Label(langas, text="---------- Irasas atnaujintas ----------")
            uzrasas_add_timedelta_atnaujintas.grid(row=15, column=0)

            sarasas.append(uzrasas_add_timedelta_atnaujintas)

            timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas = uzrasas_add_timedelta_atnaujintas

        if len(timedelta_add_x.laukelis_add_milisekundes.get()) != 0:
            datax = r_darbuotojas.created_date
            milisekundes = timedelta_add_x.laukelis_add_milisekundes.get()
            rez = datax + datetime.timedelta(milliseconds=int(milisekundes))

            r_darbuotojas.created_date = rez

            uzrasas_add_timedelta_atnaujintas = Label(langas, text="---------- Irasas atnaujintas ----------")
            uzrasas_add_timedelta_atnaujintas.grid(row=15, column=0)

            sarasas.append(uzrasas_add_timedelta_atnaujintas)

            timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas = uzrasas_add_timedelta_atnaujintas

        if len(timedelta_add_x.laukelis_add_mikrosekundes.get()) != 0:
            datax = r_darbuotojas.created_date
            mikrosekundes = timedelta_add_x.laukelis_add_mikrosekundes.get()
            rez = datax + datetime.timedelta(microseconds=int(mikrosekundes))

            r_darbuotojas.created_date = rez

            uzrasas_add_timedelta_atnaujintas = Label(langas, text="---------- Irasas atnaujintas ----------")
            uzrasas_add_timedelta_atnaujintas.grid(row=15, column=0)

            sarasas.append(uzrasas_add_timedelta_atnaujintas)

            timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas = uzrasas_add_timedelta_atnaujintas

    except AttributeError:

        ivedimas = timedelta_add.laukelis_add_timedelta.get()

        uzrasas_add_timedelta_atnaujintas_klaida = Label(langas,
                                                         text=f"[KLAIDA] Tokio darbuotojo ID : {ivedimas} bazeje nera.")
        uzrasas_add_timedelta_atnaujintas_klaida.grid(row=15, column=0)

        sarasas.append(uzrasas_add_timedelta_atnaujintas_klaida)

        timedelta_table_add_update.uzrasas_add_timedelta_atnaujintas_klaida = uzrasas_add_timedelta_atnaujintas_klaida

    session.commit()


def orai(num):

    try_destroy_laukelis()

    try:

        play_apz.laukelis_play_apz.destroy()
        play_apz.mygtukas_play_apz.destroy()

        istrinti.laukelis_istrinti.destroy()
        istrinti.mygtukas_istrinti.destroy()

        search_ban_by_username.laukelis_search.destroy()

    except AttributeError:
        pass

    if num == 1:

        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        source = requests.get("http://www.meteo.lt/lt/miestas?placeCode=Moletai").text

        uzrasas_orai_pirmas = Label(langas, text="----------------------")
        uzrasas_orai_antras = Label(langas, text="Oras Molėtuose")
        uzrasas_orai_trecias = Label(langas, text="---------------------")

        sarasas.append(uzrasas_orai_pirmas)
        sarasas.append(uzrasas_orai_antras)
        sarasas.append(uzrasas_orai_trecias)

        uzrasas_orai_pirmas.grid(row=0, column=0)
        uzrasas_orai_antras.grid(row=1, column=0)
        uzrasas_orai_trecias.grid(row=2, column=0)

    elif num == 2:

        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        source = requests.get("http://www.meteo.lt/lt/miestas?placeCode=Vilnius").text

        uzrasas_orai_vilnius_pirmas = Label(langas, text="----------------------")
        uzrasas_orai_vilnius_antras = Label(langas, text="Oras Vilniuje")
        uzrasas_orai_vilnius_trecias = Label(langas, text="---------------------")

        sarasas.append(uzrasas_orai_vilnius_pirmas)
        sarasas.append(uzrasas_orai_vilnius_antras)
        sarasas.append(uzrasas_orai_vilnius_trecias)

        uzrasas_orai_vilnius_pirmas.grid(row=0, column=0)
        uzrasas_orai_vilnius_antras.grid(row=1, column=0)
        uzrasas_orai_vilnius_trecias.grid(row=2, column=0)

    elif num == 3:

        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        source = requests.get("http://www.meteo.lt/lt/miestas?placeCode=Kaunas").text

        uzrasas_orai_kaunas_pirmas = Label(langas, text="----------------------")
        uzrasas_orai_kaunas_antras = Label(langas, text="Oras Kaune")
        uzrasas_orai_kaunas_trecias = Label(langas, text="---------------------")

        sarasas.append(uzrasas_orai_kaunas_pirmas)
        sarasas.append(uzrasas_orai_kaunas_antras)
        sarasas.append(uzrasas_orai_kaunas_trecias)

        uzrasas_orai_kaunas_pirmas.grid(row=0, column=0)
        uzrasas_orai_kaunas_antras.grid(row=1, column=0)
        uzrasas_orai_kaunas_trecias.grid(row=2, column=0)

    elif num == 4:

        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        source = requests.get("http://www.meteo.lt/lt/miestas?placeCode=Klaipeda").text

        uzrasas_orai_klaipeda_pirmas = Label(langas, text="----------------------")
        uzrasas_orai_klaipeda_antras = Label(langas, text="Oras Klaipėdoje")
        uzrasas_orai_klaipeda_trecias = Label(langas, text="---------------------")

        sarasas.append(uzrasas_orai_klaipeda_pirmas)
        sarasas.append(uzrasas_orai_klaipeda_antras)
        sarasas.append(uzrasas_orai_klaipeda_trecias)

        uzrasas_orai_klaipeda_pirmas.grid(row=0, column=0)
        uzrasas_orai_klaipeda_antras.grid(row=1, column=0)
        uzrasas_orai_klaipeda_trecias.grid(row=2, column=0)

    elif num == 5:

        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        source = requests.get("http://www.meteo.lt/lt/miestas?placeCode=Panevezys").text

        uzrasas_orai_panevezys_pirmas = Label(langas, text="----------------------")
        uzrasas_orai_panevezys_antras = Label(langas, text="Oras Panevėžyje")
        uzrasas_orai_panevezys_trecias = Label(langas, text="---------------------")

        sarasas.append(uzrasas_orai_panevezys_pirmas)
        sarasas.append(uzrasas_orai_panevezys_antras)
        sarasas.append(uzrasas_orai_panevezys_trecias)

        uzrasas_orai_panevezys_pirmas.grid(row=0, column=0)
        uzrasas_orai_panevezys_antras.grid(row=1, column=0)
        uzrasas_orai_panevezys_trecias.grid(row=2, column=0)

    else:

        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        source = requests.get("http://www.meteo.lt/lt/miestas?placeCode=Moletai").text

    soup = BeautifulSoup(source, "html.parser")

    oras = soup.find("span", class_="feelLike").text
    dregme = soup.find("span", class_="humidityGround").text
    vejo_greitis = soup.find("span", class_="windSpeedGround").text
    slegis = soup.find("span", class_="pressureTendency").text

    uzrasas_orai_oras = Label(langas, text=f"Dabar yra : {oras}°C")
    uzrasas_orai_dregme = Label(langas, text=f"Dregme : {dregme} %")
    uzrasas_orai_vejo_greitis = Label(langas, text=f"Vejo Greitis : {vejo_greitis} m/s")
    uzrasas_orai_slegis = Label(langas, text=f"Slegis : {slegis}")

    sarasas.append(uzrasas_orai_oras)
    sarasas.append(uzrasas_orai_dregme)
    sarasas.append(uzrasas_orai_vejo_greitis)
    sarasas.append(uzrasas_orai_slegis)

    uzrasas_orai_oras.grid(row=3, column=0)
    uzrasas_orai_dregme.grid(row=4, column=0)
    uzrasas_orai_vejo_greitis.grid(row=5, column=0)
    uzrasas_orai_slegis.grid(row=6, column=0)


def try_destroy_laukelis():
    try:
        timedelta_add.laukelis_add_timedelta.destroy()
        edit.laukelis_redaguoti.destroy()
    except AttributeError:
        pass


def play_apz():
    for label in sarasas:
        label.destroy()  # naikinam is ciklo visus label

    try:
        search_ban_by_username.laukelis_search.destroy()
        search_user.labelis_search.destroy()
        edit.laukelis_redaguoti.destroy()
    except (NameError, AttributeError):
        pass

    uzrasas_play_apz = Label(langas, text="Iveskite 'akmuo', 'popierius' ar 'zirkles':")
    laukelis_play_apz = Entry(langas)

    mygtukas_play_apz = Button(langas, text="Žaisti", command=play_apz_start)

    uzrasas_play_apz.grid(row=0, column=0)
    laukelis_play_apz.grid(row=1, column=0)
    mygtukas_play_apz.grid(row=2, column=0)

    play_apz.laukelis_play_apz = laukelis_play_apz
    play_apz.mygtukas_play_apz = mygtukas_play_apz


def play_apz_start():

    for label in sarasas:
        label.destroy()  # naikinam is ciklo visus label

    try:
        search_ban_by_username.laukelis_search.destroy()
        search_user.labelis_search.destroy()
        edit.laukelis_redaguoti.destroy()
    except (NameError, AttributeError):
        pass

    pasirinkimas = play_apz.laukelis_play_apz.get()

    galimi_variantai = ["akmuo", "popierius", "zirkles"]
    kompiuteris = random.choice(galimi_variantai)

    if pasirinkimas == "akmuo":

        uzrasas_choose_apz = Label(langas, text=f"\nTu pasirinkai {pasirinkimas}, kompiuteris - {kompiuteris}.\n")
        sarasas.append(uzrasas_choose_apz)

        uzrasas_choose_apz.grid(row=3, column=0)

        play_apz_start.uzrasas_choose_apz = uzrasas_choose_apz

    elif pasirinkimas == "popierius":

        uzrasas_choose_apz = Label(langas, text=f"\nTu pasirinkai {pasirinkimas}, kompiuteris - {kompiuteris}.\n")
        sarasas.append(uzrasas_choose_apz)

        uzrasas_choose_apz.grid(row=3, column=0)

        play_apz_start.uzrasas_choose_apz = uzrasas_choose_apz

    elif pasirinkimas == "zirkles":

        uzrasas_choose_apz = Label(langas, text=f"\nTu pasirinkai {pasirinkimas}, kompiuteris - {kompiuteris}.\n")
        sarasas.append(uzrasas_choose_apz)

        uzrasas_choose_apz.grid(row=3, column=0)

        play_apz_start.uzrasas_choose_apz = uzrasas_choose_apz

    else:

        uzrasas_choose_apz_klaida = Label(langas, text="[APZ ŽAIDIMAS"
                                                       " - KLAIDA] Pasirinkimas neteisingas. Reikia naudoti 'akmuo',"
                                                       " 'popierius' arba 'zirkles'")
        sarasas.append(uzrasas_choose_apz_klaida)

        uzrasas_choose_apz_klaida.grid(row=3, column=0)

        play_apz_start.uzrasas_choose_apz_klaida = uzrasas_choose_apz_klaida

    if pasirinkimas == kompiuteris:

        for label in apz_sarasas:
            label.destroy()

        uzrasas_choose_apz_lygiosios = Label(langas, text=f"Abu pasirinko {pasirinkimas}. Lygiosios!")
        sarasas.append(uzrasas_choose_apz_lygiosios)

        uzrasas_choose_apz_lygiosios.grid(row=4, column=0)

        play_apz_start.uzrasas_choose_apz_lygiosios = uzrasas_choose_apz_lygiosios

    elif pasirinkimas == "akmuo":
        if kompiuteris == "zirkles":

            uzrasas_choose_apz_akmuo = Label(langas, text="Akmuo sudaužo žirkles. Tu laimėjai !")
            sarasas.append(uzrasas_choose_apz_akmuo)

            pasirinkimas_akmuo = PhotoImage(file="images/rock.png")
            label_akmuo = Label(langas, image=pasirinkimas_akmuo)
            label_akmuo.img = pasirinkimas_akmuo
            apz_sarasas.append(label_akmuo)

            pasirinkimas_vs = PhotoImage(file="images/vs.png")
            label_vs = Label(langas, image=pasirinkimas_vs)
            label_vs.img = pasirinkimas_vs
            apz_sarasas.append(label_vs)

            pasirinkimas_zirkles = PhotoImage(file="images/scissors.png")
            label_zirkles = Label(langas, image=pasirinkimas_zirkles)
            label_zirkles.img = pasirinkimas_zirkles
            apz_sarasas.append(label_zirkles)

            pasirinkimas_lygu = PhotoImage(file="images/equal.png")
            label_lygu = Label(langas, image=pasirinkimas_lygu)
            label_lygu.img = pasirinkimas_lygu
            apz_sarasas.append(label_lygu)

            pasirinkimas_success = PhotoImage(file="images/success.png")
            label_success = Label(langas, image=pasirinkimas_success)
            label_success.img = pasirinkimas_success
            apz_sarasas.append(label_success)

            label_akmuo.grid(row=4, column=1)
            label_vs.grid(row=4, column=2)
            label_zirkles.grid(row=4, column=3)
            label_lygu.grid(row=4, column=4)
            label_success.grid(row=4, column=5)
            uzrasas_choose_apz_akmuo.grid(row=5, column=0)

            play_apz_start.uzrasas_choose_apz_akmuo = uzrasas_choose_apz_akmuo

        else:
            uzrasas_choose_apz_akmuo2 = Label(langas, text="Popierius uzdengia akmeni. Tu pralaimėjai !")
            sarasas.append(uzrasas_choose_apz_akmuo2)

            pasirinkimas_popierius = PhotoImage(file="images/paper.png")
            label_popierius = Label(langas, image=pasirinkimas_popierius)
            label_popierius.img = pasirinkimas_popierius
            apz_sarasas.append(label_popierius)

            pasirinkimas_vs = PhotoImage(file="images/vs.png")
            label_vs = Label(langas, image=pasirinkimas_vs)
            label_vs.img = pasirinkimas_vs
            apz_sarasas.append(label_vs)

            pasirinkimas_akmuo = PhotoImage(file="images/rock.png")
            label_akmuo = Label(langas, image=pasirinkimas_akmuo)
            label_akmuo.img = pasirinkimas_akmuo
            apz_sarasas.append(label_akmuo)

            pasirinkimas_lygu = PhotoImage(file="images/equal.png")
            label_lygu = Label(langas, image=pasirinkimas_lygu)
            label_lygu.img = pasirinkimas_lygu
            apz_sarasas.append(label_lygu)

            pasirinkimas_fail = PhotoImage(file="images/fail.png")
            label_fail = Label(langas, image=pasirinkimas_fail)
            label_fail.img = pasirinkimas_fail
            apz_sarasas.append(label_fail)

            label_popierius.grid(row=4, column=1)
            label_vs.grid(row=4, column=2)
            label_akmuo.grid(row=4, column=3)
            label_lygu.grid(row=4, column=4)
            label_fail.grid(row=4, column=5)
            uzrasas_choose_apz_akmuo2.grid(row=5, column=0)

            play_apz_start.uzrasas_choose_apz_akmuo2 = uzrasas_choose_apz_akmuo2

    elif pasirinkimas == "popierius":
        if kompiuteris == "akmuo":

            uzrasas_choose_apz_popierius = Label(langas, text="Popierius uzdengia akmeni. Tu laimėjai !")
            sarasas.append(uzrasas_choose_apz_popierius)

            pasirinkimas_popierius = PhotoImage(file="images/paper.png")
            label_popierius = Label(langas, image=pasirinkimas_popierius)
            label_popierius.img = pasirinkimas_popierius
            apz_sarasas.append(label_popierius)

            pasirinkimas_vs = PhotoImage(file="images/vs.png")
            label_vs = Label(langas, image=pasirinkimas_vs)
            label_vs.img = pasirinkimas_vs
            apz_sarasas.append(label_vs)

            pasirinkimas_akmuo = PhotoImage(file="images/rock.png")
            label_akmuo = Label(langas, image=pasirinkimas_akmuo)
            label_akmuo.img = pasirinkimas_akmuo
            apz_sarasas.append(label_akmuo)

            pasirinkimas_lygu = PhotoImage(file="images/equal.png")
            label_lygu = Label(langas, image=pasirinkimas_lygu)
            label_lygu.img = pasirinkimas_lygu
            apz_sarasas.append(label_lygu)

            pasirinkimas_success = PhotoImage(file="images/success.png")
            label_success = Label(langas, image=pasirinkimas_success)
            label_success.img = pasirinkimas_success
            apz_sarasas.append(label_success)

            label_popierius.grid(row=4, column=1)
            label_vs.grid(row=4, column=2)
            label_akmuo.grid(row=4, column=3)
            label_lygu.grid(row=4, column=4)
            label_success.grid(row=4, column=5)
            uzrasas_choose_apz_popierius.grid(row=5, column=0)

            play_apz_start.uzrasas_choose_apz_popierius = uzrasas_choose_apz_popierius
        else:
            uzrasas_choose_apz_popierius2 = Label(langas, text="Zirkles sukarpo popieriu. Tu pralaimėjai !")
            sarasas.append(uzrasas_choose_apz_popierius2)

            pasirinkimas_zirkles = PhotoImage(file="images/scissors.png")
            label_zirkles = Label(langas, image=pasirinkimas_zirkles)
            label_zirkles.img = pasirinkimas_zirkles
            apz_sarasas.append(label_zirkles)

            pasirinkimas_vs = PhotoImage(file="images/vs.png")
            label_vs = Label(langas, image=pasirinkimas_vs)
            label_vs.img = pasirinkimas_vs
            apz_sarasas.append(label_vs)

            pasirinkimas_popierius = PhotoImage(file="images/paper.png")
            label_popierius = Label(langas, image=pasirinkimas_popierius)
            label_popierius.img = pasirinkimas_popierius
            apz_sarasas.append(label_popierius)

            pasirinkimas_lygu = PhotoImage(file="images/equal.png")
            label_lygu = Label(langas, image=pasirinkimas_lygu)
            label_lygu.img = pasirinkimas_lygu
            apz_sarasas.append(label_lygu)

            pasirinkimas_fail = PhotoImage(file="images/fail.png")
            label_fail = Label(langas, image=pasirinkimas_fail)
            label_fail.img = pasirinkimas_fail
            apz_sarasas.append(label_fail)

            label_zirkles.grid(row=4, column=1)
            label_vs.grid(row=4, column=2)
            label_popierius.grid(row=4, column=3)
            label_lygu.grid(row=4, column=4)
            label_fail.grid(row=4, column=5)

            uzrasas_choose_apz_popierius2.grid(row=5, column=0)

            play_apz_start.uzrasas_choose_apz_popierius2 = uzrasas_choose_apz_popierius2

    elif pasirinkimas == "zirkles":
        if kompiuteris == "popierius":

            uzrasas_choose_apz_zirkles = Label(langas, text="Zirkles sukarpo popieriu. Tu laimėjai !")
            sarasas.append(uzrasas_choose_apz_zirkles)

            pasirinkimas_zirkles = PhotoImage(file="images/scissors.png")
            label_zirkles = Label(langas, image=pasirinkimas_zirkles)
            label_zirkles.img = pasirinkimas_zirkles
            apz_sarasas.append(label_zirkles)

            pasirinkimas_vs = PhotoImage(file="images/vs.png")
            label_vs = Label(langas, image=pasirinkimas_vs)
            label_vs.img = pasirinkimas_vs
            apz_sarasas.append(label_vs)

            pasirinkimas_popierius = PhotoImage(file="images/paper.png")
            label_popierius = Label(langas, image=pasirinkimas_popierius)
            label_popierius.img = pasirinkimas_popierius
            apz_sarasas.append(label_popierius)

            pasirinkimas_lygu = PhotoImage(file="images/equal.png")
            label_lygu = Label(langas, image=pasirinkimas_lygu)
            label_lygu.img = pasirinkimas_lygu
            apz_sarasas.append(label_lygu)

            pasirinkimas_success = PhotoImage(file="images/success.png")
            label_success = Label(langas, image=pasirinkimas_success)
            label_success.img = pasirinkimas_success
            apz_sarasas.append(label_success)

            label_zirkles.grid(row=4, column=1)
            label_vs.grid(row=4, column=2)
            label_popierius.grid(row=4, column=3)
            label_lygu.grid(row=4, column=4)
            label_success.grid(row=4, column=5)

            uzrasas_choose_apz_zirkles.grid(row=5, column=0)

            play_apz_start.uzrasas_choose_apz_zirkles = uzrasas_choose_apz_zirkles
        else:
            uzrasas_choose_apz_zirkles2 = Label(langas, text="Akmuo sudauzo zirkles. Tu pralaimėjai !")
            sarasas.append(uzrasas_choose_apz_zirkles2)

            pasirinkimas_akmuo = PhotoImage(file="images/rock.png")
            label_akmuo = Label(langas, image=pasirinkimas_akmuo)
            label_akmuo.img = pasirinkimas_akmuo
            apz_sarasas.append(label_akmuo)

            pasirinkimas_vs = PhotoImage(file="images/vs.png")
            label_vs = Label(langas, image=pasirinkimas_vs)
            label_vs.img = pasirinkimas_vs
            apz_sarasas.append(label_vs)

            pasirinkimas_zirkles = PhotoImage(file="images/scissors.png")
            label_zirkles = Label(langas, image=pasirinkimas_zirkles)
            label_zirkles.img = pasirinkimas_zirkles
            apz_sarasas.append(label_zirkles)

            pasirinkimas_lygu = PhotoImage(file="images/equal.png")
            label_lygu = Label(langas, image=pasirinkimas_lygu)
            label_lygu.img = pasirinkimas_lygu
            apz_sarasas.append(label_lygu)

            pasirinkimas_fail = PhotoImage(file="images/fail.png")
            label_fail = Label(langas, image=pasirinkimas_fail)
            label_fail.img = pasirinkimas_fail
            apz_sarasas.append(label_fail)

            label_akmuo.grid(row=4, column=1)
            label_vs.grid(row=4, column=2)
            label_zirkles.grid(row=4, column=3)
            label_lygu.grid(row=4, column=4)
            label_fail.grid(row=4, column=5)

            uzrasas_choose_apz_zirkles2.grid(row=5, column=0)

            play_apz_start.uzrasas_choose_apz_zirkles2 = uzrasas_choose_apz_zirkles2


def only_numbers(char):
    return char.isdigit()


def datos_formatas(char):
    return char.isdigit() or char == "-"


def show_new_ban():

    for label in sarasas:
        label.destroy()

    for label in apz_sarasas:
        label.destroy()

    source = requests.get("http://gungan.lt/amxbans/ban_list.php").text
    soup = BeautifulSoup(source, "html.parser")
    total_items = soup.find("span", class_="first").text

    puslapiai = int(total_items[13:].replace(":", ""))

    for x in range(1, puslapiai + 1):
        source2 = requests.get(f"http://gungan.lt/amxbans/ban_list.php?site={x}").text

        soup2 = BeautifulSoup(source2, "html.parser")
        table = soup2.find("table")
        table_body = table.find("tbody")

        rows = table_body.find_all("tr", class_="list")

        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    banai_label = Label(langas, text=f"Data: {data[0][0]}\nŽaidėjas: {data[0][1]}\nAdministratorius: {data[0][2]}"
                                     f"\nPriežastis: {data[0][3]}\nTrukmė: {data[0][4]}\n")
    sarasas.append(banai_label)
    banai_label.grid(row=0, column=0)


def show_old_ban():
    for label in sarasas:
        label.destroy()

    for label in apz_sarasas:
        label.destroy()

    source = requests.get("http://gungan.lt/amxbans/ban_list.php").text
    soup = BeautifulSoup(source, "html.parser")

    total_items = soup.find("span", class_="first").text
    puslapiai = int(total_items[13:].replace(":", ""))

    for x in range(1, puslapiai + 1):
        source2 = requests.get(f"http://gungan.lt/amxbans/ban_list.php?site={x}").text

        soup2 = BeautifulSoup(source2, "html.parser")

        table = soup2.find("table")
        table_body = table.find("tbody")

        rows = table_body.find_all("tr", class_="list")

        for row in rows:
            cols = row.find_all("td")

            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    banai_label_old = Label(langas, text=f"Data: {data[-1][0]}\nŽaidėjas: {data[-1][1]}"
                                         f"\nAdministratorius: {data[-1][2]}"
                                         f"\nPriežastis: {data[-1][3]}\n"
                                         f"Trukmė: {data[-1][4]}\n")
    sarasas.append(banai_label_old)
    banai_label_old.grid(row=0, column=0)


def search_ban_by_username():

    for label in sarasas:
        label.destroy()

    for label in apz_sarasas:
        label.destroy()

    labelis_search = Label(langas, text="Ieskokite bano pagal slapyvardi:")
    laukelis_search = Entry(langas)
    butonas_search = Button(langas, text="Patvirtinti", command=search_user)
    sarasas.append(butonas_search)
    sarasas.append(labelis_search)

    labelis_search.grid(row=0, column=0)
    laukelis_search.grid(row=1, column=0)
    butonas_search.grid(row=2, column=0)

    source = requests.get('http://gungan.lt/amxbans/ban_list.php').text
    soup = BeautifulSoup(source, "html.parser")

    total_items = soup.find('span', class_='first').text
    puslapiai = int(total_items[13:].replace(":", ""))

    for x in range(1, puslapiai + 1):
        source2 = requests.get(f'http://gungan.lt/amxbans/ban_list.php?site={x}').text

        soup2 = BeautifulSoup(source2, "html.parser")

        table = soup2.find("table")
        table_body = table.find("tbody")

        rows = table_body.find_all("tr", class_="list")

        for row in rows:
            cols = row.find_all('td')

            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    search_ban_by_username.laukelis_search = laukelis_search


def statistikos():

    for label in sarasas:
        label.destroy()

    for label in apz_sarasas:
        label.destroy()

    try:
        edit.laukelis_redaguoti.destroy()
    except AttributeError:
        pass

    darbuotojai = session.query(Darbuotojas).all()

    atlyginimai = [atl.atlyginimas for atl in darbuotojai]

    try:

        minamali = min(atlyginimai)

        maximali = max(atlyginimai)

        vidurkis = round(mean(atlyginimai), 2)
        mediana = round(median(atlyginimai))

        labelis_minamali = Label(langas, text=f"[INFO] Minimalus atlyginimas : {minamali}")
        labelis_maximali = Label(langas, text=f"[INFO] Didziausias atlyginimas : {maximali}")
        labelis_vidurkis = Label(langas, text=f"[INFO] Atlyyginimu vidurkis: {vidurkis}")
        labelis_mediana = Label(langas, text=f"[INFO] Atlyginimu mediana: {mediana}")

        sarasas.append(labelis_minamali)
        sarasas.append(labelis_maximali)
        sarasas.append(labelis_vidurkis)
        sarasas.append(labelis_mediana)

        labelis_minamali.grid(row=0, column=0)
        labelis_maximali.grid(row=1, column=0)
        labelis_vidurkis.grid(row=2, column=0)
        labelis_mediana.grid(row=3, column=0)

    except ValueError:
        label_nera_duomenu = Label(langas, text="[INFO] Nera duomenu.")
        label_nera_duomenu.grid(row=0, column=0)

def filter_atlyginimas():
    for label in sarasas:
        label.destroy()

    for label in apz_sarasas:
        label.destroy()

    try:
        edit.laukelis_redaguoti.destroy()
    except AttributeError:
        pass

    labelis_paieska_atlyginimas = Label(langas, text="Iveskite atlyginima")
    laukelis_paieska_atlyginimas = Entry(langas, validate="key", validatecommand=(validation, '%S'))
    mygtukas_paieska_atlyginimas = Button(langas, text="Ieskoti", command=filteris)

    if not laukelis_paieska_atlyginimas.get():
        laukelis_paieska_atlyginimas.insert(0, 0)

        labelis_paieska_atlyginimas_rez = Label(langas, text=f"Nera duomenu")
        labelis_paieska_atlyginimas_rez.grid(row=3, rowspan=3, column=0)
        sarasas.append(labelis_paieska_atlyginimas_rez)

        labelis_paieska_atlyginimas.grid(row=0, column=0)
        laukelis_paieska_atlyginimas.grid(row=1, column=0)
        mygtukas_paieska_atlyginimas.grid(row=2, column=0)

    else:

        filteris()

    filter_atlyginimas.laukelis_paieska_atlyginimas = laukelis_paieska_atlyginimas
    filter_atlyginimas.mygtukas_paieska_atlyginimas = mygtukas_paieska_atlyginimas
    filter_atlyginimas.labelis_paieska_atlyginimas = labelis_paieska_atlyginimas

def filteris():
    darbuotojai = session.query(Darbuotojas).filter(Darbuotojas.atlyginimas == float(filter_atlyginimas.laukelis_paieska_atlyginimas.get())).all()
    i = 0
    if not darbuotojai:
        labelis_paieska_atlyginimas_tuscias = Label(langas, text="[PAIESKA] Nera duomenu.")
        labelis_paieska_atlyginimas_tuscias.grid(row=3, column=0)


        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        try:
            edit.laukelis_redaguoti.destroy()
        except AttributeError:
            pass

        sarasas.append(labelis_paieska_atlyginimas_tuscias)

    for darbuotojas in darbuotojai:
        i += 1
        labelis_paieska_atlyginimas_rez = Label(langas, text=f"{darbuotojas}")
        labelis_paieska_atlyginimas_rez.grid(row=2+i, column=0)
        sarasas.append(labelis_paieska_atlyginimas_rez)


def filter_gimimo_data():
    for label in sarasas:
        label.destroy()

    for label in apz_sarasas:
        label.destroy()

    try:
        edit.laukelis_redaguoti.destroy()
    except AttributeError:
        pass

    labelis_paieska_gimimo_data = Label(langas, text="Iveskite gimimo data")
    laukelis_paieska_gimimo_data = Entry(langas, validate="key", validatecommand=(validation_data, '%S'))
    mygtukas_paieska_gimimo_data = Button(langas, text="Ieskoti", command=filteris_data)

    if not laukelis_paieska_gimimo_data.get():
        laukelis_paieska_gimimo_data.insert(0, 0)

        labelis_paieska_gimimo_data_rez = Label(langas, text=f"Nera duomenu")
        labelis_paieska_gimimo_data_rez.grid(row=3, rowspan=3, column=0)
        sarasas.append(labelis_paieska_gimimo_data_rez)

        labelis_paieska_gimimo_data.grid(row=0, column=0)
        laukelis_paieska_gimimo_data.grid(row=1, column=0)
        mygtukas_paieska_gimimo_data.grid(row=2, column=0)

    else:

        filteris_data()

    filter_gimimo_data.laukelis_paieska_gimimo_data = laukelis_paieska_gimimo_data
    filter_gimimo_data.mygtukas_paieska_gimimo_data = mygtukas_paieska_gimimo_data
    filter_gimimo_data.labelis_paieska_gimimo_data = labelis_paieska_gimimo_data



def filteris_data():
    darbuotojai = session.query(Darbuotojas).filter(
        Darbuotojas.gimimo_data == filter_gimimo_data.laukelis_paieska_gimimo_data.get()).all()
    i = 0
    if not darbuotojai:
        labelis_paieska_gimimo_data_tuscias = Label(langas, text="[PAIESKA] Nera duomenu.")
        labelis_paieska_gimimo_data_tuscias.grid(row=3, column=0)

        for label in sarasas:
            label.destroy()

        for label in apz_sarasas:
            label.destroy()

        try:
            edit.laukelis_redaguoti.destroy()
        except AttributeError:
            pass

        sarasas.append(labelis_paieska_gimimo_data_tuscias)

    for darbuotojas in darbuotojai:
        i += 1
        labelis_paieska_gimimo_data_rez = Label(langas, text=f"{darbuotojas}")
        labelis_paieska_gimimo_data_rez.grid(row=2 + i, column=0)
        sarasas.append(labelis_paieska_gimimo_data_rez)


def search(listas, platform):
    for i in range(len(listas)):
        if listas[i][1] == platform:
            return f"Data: {listas[i][0]}\nŽaidėjas: {listas[i][1]}\nAdministratorius: {listas[i][2]}\n" \
                   f"Priežastis: {listas[i][3]}\nTrukmė: {listas[i][4]}\n"
    return False


def search_user():

    platform = search_ban_by_username.laukelis_search.get()

    try:
        search_user.labelis_nerastas.destroy()
    except (NameError, AttributeError):
        pass

    if search(data, platform):

        labelis_search = Label(langas, text=f"{search(data, platform)}")
        labelis_search.grid(row=3, column=0)

        search_user.labelis_search = labelis_search
    else:
        try:
            search_user.labelis_search.destroy()
        except (NameError, AttributeError):
            pass

        labelis_nerastas = Label(langas, text="[AMXBans] Šis žaidėjas nerastas.")
        sarasas.append(labelis_nerastas)
        labelis_nerastas.grid(row=3, column=0)
        search_user.labelis_nerastas = labelis_nerastas


def bye():
    langas.destroy()


langas = Tk()

langas.iconphoto(False, PhotoImage(file='images/icon.gif'))
langas.title("Visko Po Truputi")

meniu = Menu(langas)

langas.config(menu=meniu)

validation = langas.register(only_numbers)
validation_data = langas.register(datos_formatas)

submeniu = Menu(meniu, tearoff=0)
submeniu_timedelta = Menu(meniu, tearoff=0)
submeniu_prognoze = Menu(meniu, tearoff=0)
submeniu_apz = Menu(meniu, tearoff=0)
submeniu_blocked = Menu(meniu, tearoff=0)
submeniu_filtras = Menu(meniu, tearoff=0)

meniu.add_cascade(label="Duomenu Baze", menu=submeniu)
submeniu.add_command(label="Peržiūrėti Duomenis", command=watch)
submeniu.add_command(label="Istrinti Pasirinkta Asmeni", command=istrinti)
submeniu.add_command(label="Redaguoti Pasirinkta Asmeni", command=edit)
submeniu.add_separator()
submeniu.add_command(label="Statistikos", command=statistikos)
submeniu.add_separator()
submeniu.add_command(label="Išeiti", command=bye)

meniu.add_cascade(label="Filtras", menu=submeniu_filtras)
submeniu_filtras.add_command(label="Ieskoti pagal atlyginima", command=filter_atlyginimas)
submeniu_filtras.add_command(label="Ieskoti pagal gimimo data", command=filter_gimimo_data)
submeniu_filtras.add_separator()
submeniu_filtras.add_command(label="Išeiti", command=bye)


meniu.add_cascade(label="TimeDelta", menu=submeniu_timedelta)
submeniu_timedelta.add_command(label="Prideti X laika", command=timedelta_add)
submeniu_timedelta.add_separator()
submeniu_timedelta.add_command(label="Išeiti", command=bye)

meniu.add_cascade(label="Oru Prognoze", menu=submeniu_prognoze)
submeniu_prognoze.add_command(label="Moletai", command=lambda: orai(1))
submeniu_prognoze.add_command(label="Vilnius", command=lambda: orai(2))
submeniu_prognoze.add_command(label="Kaunas", command=lambda: orai(3))
submeniu_prognoze.add_command(label="Klaipeda", command=lambda: orai(4))
submeniu_prognoze.add_command(label="Panevėžys", command=lambda: orai(5))
submeniu_prognoze.add_separator()
submeniu_prognoze.add_command(label="Išeiti", command=bye)

meniu.add_cascade(label="Uzblokuoti Zaidejai", menu=submeniu_blocked)
submeniu_blocked.add_command(label="Perziureti naujausia", command=show_new_ban)
submeniu_blocked.add_command(label="Perziureti seniausia", command=show_old_ban)
submeniu_blocked.add_command(label="Ieskoti pagal slapyvardi", command=search_ban_by_username)
submeniu_blocked.add_separator()
submeniu_blocked.add_command(label="Išeiti", command=bye)

meniu.add_cascade(label="Akmuo/popierius/žirkles", menu=submeniu_apz)
submeniu_apz.add_command(label="Žaisti", command=play_apz)
submeniu_apz.add_separator()
submeniu_apz.add_command(label="Išeiti", command=bye)


uzrasas_iterpti_vardas = Label(langas, text="Iveskite varda")
laukelis_iterpti_vardas = Entry(langas)

sarasas.append(uzrasas_iterpti_vardas)
sarasas.append(laukelis_iterpti_vardas)

uzrasas_iterpti_pavarde = Label(langas, text="Iveskite pavarde")
laukelis_iterpti_pavarde = Entry(langas)

sarasas.append(uzrasas_iterpti_pavarde)
sarasas.append(laukelis_iterpti_pavarde)

uzrasas_iterpti_gimimo_metai = Label(langas, text="Iveskite gimimo metus")
laukelis_iterpti_gimimo_metai = Entry(langas, validate="key", validatecommand=(validation_data, '%S'))

sarasas.append(uzrasas_iterpti_gimimo_metai)
sarasas.append(laukelis_iterpti_gimimo_metai)

uzrasas_iterpti_pareigos = Label(langas, text="Iveskite pareigas")
laukelis_iterpti_pareigos = Entry(langas)

sarasas.append(uzrasas_iterpti_pareigos)
sarasas.append(laukelis_iterpti_pareigos)

uzrasas_iterpti_atlyginimas = Label(langas, text="Iveskite atlyginima")
laukelis_iterpti_atlyginimas = Entry(langas, validate="key", validatecommand=(validation, '%S'))

sarasas.append(uzrasas_iterpti_atlyginimas)
sarasas.append(laukelis_iterpti_atlyginimas)

langas.bind("<Escape>", lambda event: bye())

mygtukas_iterpti_patvirtinti = Button(langas, text="Patvirtinti", command=create_tables)

sarasas.append(mygtukas_iterpti_patvirtinti)

uzrasas_iterpti_vardas.grid(row=0, column=0)
laukelis_iterpti_vardas.grid(row=1, column=0)

uzrasas_iterpti_pavarde.grid(row=2, column=0)
laukelis_iterpti_pavarde.grid(row=3, column=0)

uzrasas_iterpti_gimimo_metai.grid(row=4, column=0)
laukelis_iterpti_gimimo_metai.grid(row=5, column=0)

uzrasas_iterpti_pareigos.grid(row=6, column=0)
laukelis_iterpti_pareigos.grid(row=7, column=0)

uzrasas_iterpti_atlyginimas.grid(row=8, column=0)
laukelis_iterpti_atlyginimas.grid(row=9, column=0)

mygtukas_iterpti_patvirtinti.grid(row=10, column=0)


def iterpti():
    pass


iterpti.laukelis_iterpti_vardas = laukelis_iterpti_vardas
iterpti.laukelis_iterpti_pavarde = laukelis_iterpti_pavarde
iterpti.laukelis_iterpti_gimimo_data = laukelis_iterpti_gimimo_metai
iterpti.laukelis_iterpti_pareigos = laukelis_iterpti_pareigos
iterpti.laukelis_iterpti_atlyginimas = laukelis_iterpti_atlyginimas

langas.mainloop()
