import requests
import json
import subprocess  # Se importa subprocess para poder ejecutar scripts externos
import logging # Para generar registros de errores o información
from datetime import datetime #Logger
import argparse 
#3er Parcial PC
#Configuración inicial del logger
logging.basicConfig(
    filename = 'Log_Actividad3.txt' ,   #Nombre del archivo donde se guardan los registros
    level = logging.INFO,  #Se especifica que el nivel de registro sea INFO este es para mensajes de uso informativo de que el script esta realizando sus tareas correctamente
    format = '%(asctime)s -%(message)s', #Formato con fecha y mensaje
    datefmt= 'Y-%m-%d %H:%M:%S'
)
def get_ips():# Función para ejecutar el script de powershell (IPs Activas)
    print("Obteniendo todas las conexiones de red activas...")
    try:
        LinPS = "powershell -Executionpolicy Bypass -File VDP_Actividad1.ps1"  #Establecemos permisos de ejecución y archivo a trabajar
        runNetscan=subprocess.run(LinPS, capture_output=True, text=True)
        print("Listado de IPs completado")
        print(runNetscan.stdout)  #Salida estándar
        logging.info("Tarea completada con éxito")  #Registro 
        #Generar salida de la lista de IPs para usarla en API Abuse(.stdout)
        ips = runNetscan.stdout.strip()#Limpiar la salida estandar para facilitar su manipulación (eliminando espacios, saltos de línea y split divide el texto en lista separando cada IP
        ips = ips.split(",")
        ips = [ip.strip() for ip in ips if ip.strip()]
        return ips 
    except Exception as e:
        print(f"Ha ocurrido un error obteniendo conexiones de red activas: {e}")
        logging.error(f"Error en la generación de IPs: " + str(e))

def checarIP(ip):
    #Código para consultar la API de Abuse IP BD
    apikey= "d825322d2bc7e8e310024ab061dd8e0c0f4180fbef16390c7d29ff442d99831d46da8a5503c0bf65"  #Configuración de APIKEY
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip,   #Se establece la ip a consultar esta fue tomada de get_ips
        'maxAgeInDays': '90'
    }
    headers = {
        'Accept': 'application/json',
        'Key': apikey
    }
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    if response.status_code == 200: #200 corresponde a código de estado HTTP que significa que la petición fue exitosa
        decodedResponse = response.json() #Convierte la respuesta en texto JSON
        abuse_score = decodedResponse.get('data', {}).get('abuseConfidenceScore', 0)  #Consulta para reportes de abuso
        if abuse_score > 0:   #Condicional para determinar si la IP esta reportada o no
           return f"La IP {ip} tiene reporte con nivel de abuso de {abuse_score}"
        else:
           return f"La IP {ip} no cuenta con reportes de abuso"
        return json.dumps(decodedResponse, sort_keys=True, text=True, indent=4)
      


def main():
    parser = argparse.ArgumentParser(description = "Consulta de IPs con AbuseIPDB") #Crear el parser para que se ejecute desde línea de comandos
    parser.add_argument('-i', '--ips', nargs= '*', help = "Proporcionar opcionalmente una lista de IPs separadas por espacio cada una para consultar en AbuseIPDB") #Definir argumentos a recibir
    args = parser.parse_args()
    logging.info("------ Inicio de ejecución del script ---------") #Para marcar en el archivo de registro log cuando comienza la ejecución
    if args.ips:
        ips = args.ips
        print( "Usando la lista de IPs recibida desde la línea de comandos")
    else:      #En caso de no haber recibido se usa la lista de get_ips)
        ips = get_ips()
        
    if  ips:
       print("Revisando IPs con AbuseIPDB...")
       for ip in ips[:3]:     #Se establece límite de búsqueda solo 3 IPs para no saturar la API
         result = checarIP(ip)
         print(result)
         logging.info(f"IP: {ip} - Resultado: {result}")  #Guardar en el log el resultado e IP
    else:
        print("No se encontraron IPs disponibles para validar")
        logging.info("No se encontraron IPs disponibles para validar") #Guardar en el log el mensaje informativo
    logging.info("-------- Fin de ejecución del script -----")

if __name__ == "__main__":
    main()
