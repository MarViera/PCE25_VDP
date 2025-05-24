import requests
import json
import subprocess  # Se importa subprocess para poder ejecutar scripts externos
import logging # Para generar registros de errores o información
#3er Parcial PC
def checarIP():
    #Código para consultar la API de Abuse IP BD
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': '52.123.250.32',
        'maxAgeInDays': '90'
    }
    headers = {
        'Accept': 'application/json',
        'Key': '1351d01769557d0f4f0e59265e9b3b401a122bac5c33b6fcbf15ac6f7a1d7e55b5d53ff5f43a287c'
    }
    response = requests.request(method='GET', url=url,
                                headers=headers, params=querystring)
    # Formatted output
    decodedResponse = json.loads(response.text)
    return json.dumps(decodedResponse, sort_keys=True, indent=4)

def get_ips():# Función para ejecutar el script de powershell (IPs Activas)
    print("Obteniendo todas las conexiones de red activas...")
    try:
        LinPS = "powershell -Executionpolicy Bypass -File VDP_Actividad1.ps1"  #Establecemos permisos de ejecución y archivo a trabajar
        runNetscan=subprocess.run(LinPS, capture_output=True, text=True)
        print("Listado de IPs completado")
        print(runNetscan.stdout)  #Salida estándar
        logging.info("Tarea completada con éxito")  #Registro 
        #Generar salida de la lista de IPs para usarla en API Abuse(.stdout)
        ips = runNetscan.stdout.strip().split('\n')  #Limpiar la salida estandar para facilitar su manipulación (eliminando espacios, saltos de línea y split divide el texto en lista separando cada IP
        ips = [ip.strip() for ip in ips if ip.strip()]
        return ips 
    except Exception as e:
        print(f"Ha ocurrido un error obteniendo conexiones de red activas: {e}")
        logging.error(f"Error en la generación de IPs: " + str(e))

def main():
    #todo el codigo del proyecto estará aquí
    print("Hola mundo")
    print(checarIP())


if __name__ == "__main__":
    main()
