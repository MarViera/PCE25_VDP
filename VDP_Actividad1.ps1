# Obtener todas las conexiones de red activas
$connections = Get-NetTCPConnection | Select-Object -ExpandProperty RemoteAddress

# Filtrar para eliminar valores vacíos y evitar repetir IPs
$uniqueIPs = $connections | Where-Object { $_ -match "\d+\.\d+\.\d+\.\d+" } | Sort-Object -Unique


# Opcional: Guardar la lista en un archivo de texto
$uniqueIPs | Out-File -FilePath "ConexionesIPs.txt"


#Convertir $uniqueIPs a una lista separada con comas (para que python pueda leer todas las IPs sin problema)
Write-Output ($uniqueIPs -join ",")


#Elimine los write-host ya que para ejecutar el script en la actividad 2 se me mezclaba con las IP y agregue write-output para que python lo pueda leer facilmente"""