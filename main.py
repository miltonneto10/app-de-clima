from email.mime import image
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import requests
from datetime import datetime

import json
import pytz
import pycountry_convert as pc


janela = Tk()

cor1 = "#000000"
cor2 = "#ffffff"
cor3 = "#4169E1"
cor4 = "#A9A9A9"

fundo_dia = "#1E90FF"
fundo_noite = "#363636"
fundo_tarde = "#FF8C00"
fundo = fundo_dia

janela.title("")
janela.geometry("320x350")
janela.configure(bg=fundo)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

frame_top = Frame(janela, width=320, height=50, bg=cor2, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=320, height=300, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=NW)

estilo = ttk.Style(janela)
estilo.theme_use("clam")

global imagem

#função que retorna as informações
def informacao():

    chave = "4d47ed4a09902a5c04035f581ac8a19c"
    cidade = e_local.get()
    api_link = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=pt_br&units=metric".format(cidade, chave)

    #fazendo a chamada da API usando requests
    r = requests.get(api_link)

    #convertendo os dados presntes na variavel r em dicionario
    dados = r.json()

    print(dados)
    #obtendo zona, país e horas
    pais_codigo = dados["sys"]["country"]


    #zona
    zona_fuso = pytz.country_timezones[pais_codigo]

    #país
    pais = pytz.country_names[pais_codigo]

    #data
    zona = pytz.timezone(zona_fuso[0])
    zona_horas = datetime.now(zona)
    zona_horas = zona_horas.strftime("%d %m %Y | %H:%M %p")


    #tempo
    tempo = round(dados["main"]["temp"])
    print(tempo)
    pressao = dados["main"]["pressure"]
    velocidade = dados["wind"]["speed"]
    descricao = dados["weather"][0]["description"]

    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continente_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continente_codigo)

        return pais_continente_nome

    continente = pais_para_continente(pais)

    #passando informações nas labels
    l_cidade["text"] = cidade + " - " + pais + " / " + continente
    l_data["text"] = zona_horas
    l_temperatura["text"] = tempo
    l_t_simbol["text"] = "°C"
    l_t_nome["text"] = "Temperatura"
    l_velocidade["text"] = "Velocidade do Vento: "+str(velocidade)
    l_pressao["text"] = "Pressão: "+str(pressao)
    l_descricao["text"] = descricao

    #lógica para trocar o período do dia
    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime("%H")

    global imagem
    zona_periodo = int(zona_periodo)
    if zona_periodo <= 4:
        imagem = Image.open("images/lua.png")
        fundo = fundo_noite
    elif zona_periodo <= 11:
        imagem = Image.open("images/sol.png")
        fundo = fundo_dia
    elif zona_periodo <= 17:
        imagem = Image.open("images/sol_tarde.png")
        fundo = fundo_tarde
    elif zona_periodo <= 23:
        imagem = Image.open("images/lua.png")
        fundo = fundo_noite
    else:
        pass

    imagem = imagem.resize((130, 130))
    imagem = ImageTk.PhotoImage(imagem)

    l_icon= Label(frame_corpo, image=imagem, bg=fundo)
    l_icon.place(x=160, y=50)

    #passando informações nas labels
    janela.configure(bg=fundo)
    frame_top.configure(bg=fundo)
    frame_corpo.configure(bg=fundo)

    l_cidade["bg"] = fundo
    l_data["bg"] = fundo 
    l_temperatura["bg"] = fundo 
    l_t_simbol["bg"] = fundo 
    l_t_nome["bg"] = fundo 
    l_velocidade["bg"] = fundo 
    l_pressao["bg"] = fundo 
    l_descricao["bg"] = fundo 



#frame_top
e_local = Entry(frame_top, width=20, justify="left", font=("", 14), highlightthickness=1, relief="solid")
e_local.place(x=15, y=10)

b_ver = Button(frame_top,command= informacao,text="Buscar", bg=cor4 , fg=cor1, font=("Ivy, 9 bold"), relief="raised", overrelief=RIDGE)
b_ver.place(x=250, y=10)

#frame_corpo
l_cidade = Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 12"))
l_cidade.place(x=10, y=4)

l_data = Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 10"))
l_data.place(x=10, y=54)

l_temperatura = Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 45"))
l_temperatura.place(x=10, y=100)

l_t_simbol = Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 10 bold"))
l_t_simbol.place(x=85, y=110)

l_t_nome = Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 8"))
l_t_nome.place(x=85, y=140)

l_pressao = Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 10"))
l_pressao.place(x=10, y=184)

l_velocidade= Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 10"))
l_velocidade.place(x=10, y=212)

l_descricao= Label(frame_corpo, text="", anchor="center", bg=fundo , fg=cor2, font=("Arial 10"))
l_descricao.place(x=170, y=190)

janela.mainloop()