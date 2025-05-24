import requests
import json
import subprocess  # Se importa subprocess para poder ejecutar scripts externos
import logging # Para generar registros de errores o información
#3er Parcial PC

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
    ips = get_ips()  #Obtenemos la lista de direcciones IP activas para trabajar
    if ips:
        print("Revisando IPs con AbuseIPDB...")
        for ip in ips[:3]:     #Se establece límite de búsqueda solo 3 IPs para no saturar la API
            result = checarIP(ip)
            print(result)
    else:
        print("No se encontraron IPs disponibles para validar")
    


if __name__ == "__main__":
    main()
