#!/usr/bin/env  python3
# Python Script using Netmiko to run commands on IOS Router

from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from json import load
import time
from getpass import getpass
from telegram import Bot
import requests


# Colores para impresion en pantalla.
color_reset = "\x1b[0m"
red = "\x1b[00;00;1;031m"
red_blink = "\x1b[00;00;05;031m"
magent = "\x1b[00;00;02;033m"
magent_blink = "\x1b[00;00;05;033m"
blue = "\x1b[00;00;1;034m"
blue_blink = "\x1b[00;00;5;034m"
green = "\x1b[00;00;01;092m"
green_blink = "\x1b[00;00;5;092m"
green_2 = "\x1b[00;00;5;092m"

bot_token = "TELEGRAM_TOKEN"
chat_id = "CHAT_ID_INT"

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=data)
    return response.status_code, response.text


mensaje_alive = "🟢 *Servidores Alive:*\n"
mensaje_dead = "🔴 *Servidores Dead:*\n"

def main():

    access = []
    for line in open(file="Pass.txt", mode="r"):
        access.append(line.strip("\n"))

    username, password = access[0], access[1]

    with open(file="test.json", mode="r") as file:
        data_json = load(file)

    for sucursal in data_json["Branches"]:
        print(f"{blue}{'='*80}")
        print(f"{red}Esta es la sucursal {blue}{sucursal['Name']}{color_reset}")

        for dispositivos in sucursal["Devices"]:
            name = dispositivos["Name"]
            ip = dispositivos["IPv4"]

            if "Firewall" in dispositivos["Type"]:
                try:
                    remote_device = {
                        "device_type": "fortinet",
                        "username": username,
                        "password": password,
                        "ip": ip,
                        "port": "22"
                    }

                    print(f"{'#'*27} Connecting to the Device {'#'*27}")
                    connection = ConnectHandler(**remote_device)
                    # connection.enable()
                    print(f" Firewall {blue} {connection.find_prompt()} {color_reset}")
                    print(f"{'#'*34} Connected {'#'*35}")

                    time.sleep(2)

                    lines = connection.send_command(
                        "diagnose sys sdwan health-check").splitlines()

                    links_up, links_down = [], []
                    for line in lines:
                        if "Health" in line:
                            line = line.replace("(", " ").replace(")", " ").split(" ")[-3]
                            links_up.append(line)

                        elif "state(alive)" in line:

                            line = line.replace("(", " ").replace(")", " ").replace(
                                ":", "").replace("Seq", "").replace(",", "").replace(
                                "sla_map=0x1", "").replace("sla_map=0x0", "")

                            line = line.split()
                            line.pop(0)
                            alias = connection.send_command(
                                f"show system interface {line[0]}").splitlines()
                            alias = alias[6].strip().split()[2]
                            line.insert(1, alias)
                            line = " ".join(line)
                            links_up.append(line)

                        elif "state(dead)" in line:
                            line = line.replace("(", " ").replace(")", " ").replace(
                                ":", "").replace("Seq", "").replace(
                                ",", "").replace("sla_map=0x0", "")

                            line = line.split()
                            line.pop(0)
                            alias = connection.send_command(
                                f"show system interface {line[0]}").splitlines()

                            line[0] = alias
                            line = " ".join(line)
                            links_down.append(line)

                        else:
                            continue

                    for link in links_up:
                        link = f"{link}"
                        txt = link.split(" ")
                        linea = ""
                        for x in txt[0:10]:
                            linea += x + " "
                        print(f"{green}{linea}{color_reset}")
                        mensaje_alive += f"{linea}\n"

                    for link in links_down:
                        link = f"{link}"
                        txt = link.split(" ")
                        linea = ""
                        for x in txt[0:10]:
                            linea += x + " "
                        print(f"{red}{linea}{color_reset}")
                        mensaje_dead += f"{linea}\n"

                    enviar_telegram(mensaje_alive)
                    enviar_telegram(mensaje_dead)

                    print(f"{blue}{'='*17}{red} Te conectaste a {green}{name} {red}con la {green}{ip} {blue}{'='*17}{color_reset}")
                    connection.disconnect()

                except NetmikoAuthenticationException:
                    print(f"{red_blink}El Usuario o contraseña de {blue_blink}{name} {green_blink}{ip} {red_blink}no son las correctas{color_reset}")
                    continue
            else:
                continue
        print(f"{blue}{'='*80}{color_reset}")
        print()


if __name__ == '__main__':
    main()
