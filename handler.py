"""a
Created on Sat Oct 17 21:00:12 2020

@author: dazna
"""
import json


def co2_function(event, context):
    print(event)
    body = {'message': 'OK'}
    params = event['queryStringParameters']

    recibo_luz = float(str(params['luz']))
    recibo_gas = float(str(params['gas']))
    numero_personas = float(str(params['personas']))
    horas_avion = float(str(params['avion']))
    horas_coche = float(str(params['coche']))
    tipo_alimentacion = str(params['alimentacion'])

    body['co2_kg_anual'] = CO2(
        recibo_luz, recibo_gas, numero_personas, horas_avion, horas_coche, tipo_alimentacion)

    print(body)

    response = {
        'statusCode': 200,
        'body': json.dumps(body),
    }

    return response


def CO2(recibo_luz, recibo_gas, numero_personas, horas_avion, horas_coche, tipo_alimentacion):
    FE_luz = 5.05  # obtenido del DOF (2019)
    if recibo_luz < 800:
        precio = 400  # precio medio del rango de la respuesta
        # los primeros dos precios que da CFE
        excedente = precio-(150*.849+130*1.025)
        kwh_excedente = excedente/3.004  # 3.004 es el precio que cobra CFE por el excedente
        # 150 y 130 son los kw que tienes que gastar para estar en los primeros niveles
        kwh_anual = (150+130+kwh_excedente)*6
    elif recibo_luz < 2500:
        precio = 1650
        excedente = precio-(150*.849+130*1.025)
        kwh_excedente = excedente/3.004
        kwh_anual = (150+130+kwh_excedente)*6
    elif recibo_luz > 2500:
        precio = 3000
        excedente = precio-(150*.849+130*1.025)
        kwh_excedente = excedente/3.004
        kwh_anual = (150+130+kwh_excedente)*6

    CO2_luz = kwh_anual*FE_luz

    FE_gas = 2.014  # por cada litro de gas natural
    precio_litro_gas = 1479.704  # este es el precio por litro (agosto 2020)
    if recibo_gas < 500:
        precio = 250
        litros_anual = (precio/precio_litro_gas)*12
    elif recibo_gas < 1000:
        precio = 750
        litros_anual = (precio/precio_litro_gas)*12
    elif recibo_gas > 1000:
        precio = 1500
        litros_anual = (precio/precio_litro_gas)*12

    CO2_gas = litros_anual*FE_gas

    CO2_avion = 90 * horas_avion

    CO2_coche = horas_coche * .0017325 * 365 * 1.5

    if tipo_alimentacion == 'Vegano':
        emision = 1.5
    elif tipo_alimentacion == 'Vegetariano':
        emision = 1.7
    elif tipo_alimentacion == 'Carne':  # carne diario
        emision = 3.3
    elif tipo_alimentacion == 'Mix':  # Carne dos o tres veces a la semaa
        emision = 2.5

    CO2_alimentacion = emision

    # sumar 285 por la basura, 90 por cada hora de avion, litro y medio la hora (coche)
    CO2_total = (CO2_luz + CO2_gas) / numero_personas + 285 + \
        CO2_avion + CO2_coche + CO2_alimentacion*1000

    return(CO2_total)


# print(CO2(1500, 800, 2, 20, 2, 'Mix'))
