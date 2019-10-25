import mysql.connector # --> libreria para mysql en python
#==============================================================================================================================================================================
#==================================================================================================================================
#--> IMPORTAMOS LA LIBRERIA PARA OCR EN PYTHON 3 PYTESERACT 
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

#--> CONEXION A ENTORNO MYSQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= "12345",
    database = "ocr_confival"#cuando queremos conectar a una base de datos especifica
)

mycursor = mydb.cursor()

#==============================================================================================================================================================================
#--> CREAR TABLA
#mycursor.execute("CREATE TABLE ingenieros(id INT AUTO_INCREMENT PRIMARY KEY, numero INT(20), nombre VARCHAR(255), apellido VARCHAR(255), fecha_de_nacimiento DATE, lugar_de_nacimiento VARCHAR(255), fecha_de_expedicion DATE, lugar_de_expedicion VARCHAR(255))")

#==================================================================================================================================
#--> UBICACION PAQUETE TESSERACT EN LOCAL
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#==================================================================================================================================
#--> FUNCION PARA ORDENAR FECHA
def ordenarFecha(date):
    if(len(date)==11):
        iz = date[:2]
        cen = date[2:7]
        der = date[7:]
        y = der + cen + iz
        return y
    else:
        print("formato no valido de fecha")

#=================================================================================================================================
#--> FUNCION PARA CAMBIAR FORMATO FECHA
def formatoFecha(date):
    if(date[5:8]=='ENE'):
        fecha = date.replace(date[5:8], '01')
        return fecha

    elif(date[5:8]=='FEB'):
        fecha = date.replace(date[5:8], '02')
        return fecha
    
    elif(date[5:8]=='MAR'):
        fecha = date.replace(date[5:8], '03')
        return fecha
    
    elif(date[5:8]=='ABR'):
        fecha = date.replace(date[5:8], '04')
        return fecha   

    elif(date[5:8]=='MAY'):
        fecha = date.replace(date[5:8], '05')
        return fecha

    elif(date[5:8]=='JUN'):
        fecha = date.replace(date[5:8], '06')
        return fecha
    
    elif(date[5:8]=='JUL'):
        fecha = date.replace(date[5:8], '07')
        return fecha
    
    elif(date[5:8]=='AGO'):
        fecha = date.replace(date[5:8], '08')
        return fecha
    
    elif(date[5:8]=='SEP'):
        fecha = date.replace(date[5:8], '09')
        return fecha

    elif(date[5:8]=='OCT'):
        fecha = date.replace(date[5:8], '10')
        return fecha

    elif(date[5:8]=='NOV'):
        fecha = date.replace(date[5:8], '11')
        return fecha

    elif(date[5:8]=='DIC'):
        fecha = date.replace(date[5:8], '12')
        return fecha

    else :
        return "formato no valido"

#=================================================================================================================================
#--->SE GUARDA LOS DATOS DE IMAGEN PROCESADA POR PYTESSERACT 
d = pytesseract.image_to_string(Image.open("resolucionAceptable1.png"))
d2 = pytesseract.image_to_string(Image.open("newL2.jpg"))
#print(d) #imprime el string de datos obtenidos a traves de pytesseract

#=================================================================================================================================
#-->SE DIVIDE EL STRING DE DATOS EN ITEMS PARA ALMACENAR EN UNA LISTA
datos = d.splitlines() 
print("******************************************************************************************************************************************************")
print("DATOS CEDULA LADO 1")
print(datos)
print("******************************************************************************************************************************************************")

datos2 = d2.splitlines()
#print(type(datos)) retorna el tipo de dato para la variable datos ()
print("******************************************************************************************************************************************************")
print("DATOS CEDULA LADO 2")
print(datos2)
print("******************************************************************************************************************************************************")

#-->COMVERTIMOS LOS DATOS DE NUMERO DE CEDULA OBTENIDOS A UN NUEVO ARRAY PARA MANIPULACION
datos_cedula = []
temp1 = datos[3]
tempcedula = temp1.split(" ")
#-->SE QUITAN LOS LOS PUNTOS DEL NUMERO DE CEDULA
cedula = tempcedula[1].replace(".", "")
NumCedula = int(cedula)

#=================================================================================================================================
#-->SE CLASIFICA LA INFORMACION OBTENIDA POR OCR TESSERACT

#NUMERO
print("==================================================")
print("Numero de Cedula: ", NumCedula)
print(type(NumCedula))
datos_cedula.append(NumCedula)
print("==================================================")

#NOMBRES
print("==================================================")
nombres = datos[6]
print("Nombres: ", nombres)
print(type(nombres))
datos_cedula.append(nombres)
print("==================================================")

#APELLIDOS
print("==================================================")
apellidos = datos[4]
print("Apellidos: ", apellidos)
print(type(apellidos))
datos_cedula.append(apellidos)
print("==================================================")

#FECHA DE NACIMIENTO
print("==================================================")
temp2 = datos2[0].split(" ")
#print(temp2)
fechaNacimiento = temp2[4]
#print(type(fechaNacimiento))
print("Fecha Nacimiento Original: ", fechaNacimiento)
# print(type(fechaNacimiento))
fechaModificada = ordenarFecha(fechaNacimiento)
print("Fecha de Nacimiento Ordenada: ", fechaModificada)
fechaFormateada = formatoFecha(fechaModificada)
print("Fecha de Nacimiento con formato: ", fechaFormateada) # sujeto a verificacion en registros para base de datos
print(type(fechaFormateada))
datos_cedula.append(fechaFormateada)
print("==================================================")

#LUGAR DE NACIMIENTO
print("==================================================")
tempMunicipio = datos2[9]
municipio = tempMunicipio.split(" ")
tempDepartamento = datos2[10]
lugarNacimiento = municipio[0]+tempDepartamento
print("Lugar de Nacimiento :" , lugarNacimiento) # sujeto a verificación en requerimientos de base de datos
datos_cedula.append(lugarNacimiento)
print("==================================================")

#FECHA DE EXPEDICION DE DOCUMENTO
print("==================================================")
tempExpedicion = datos2[14].split(" ")
tempFechaExpedicion = ordenarFecha(tempExpedicion[0])
print("Fecha de expedicion ordenada: ", tempFechaExpedicion)
fechaExpedicion = formatoFecha(tempFechaExpedicion)
print("Fecha de expedicion con formato: ", fechaExpedicion)
datos_cedula.append(fechaExpedicion)
print("==================================================")


#LUGAR DE EXPEDICION DE DOCUMENTO
print("==================================================")
lugarExpedicion = tempExpedicion[1]
print("Lugar de expedicion de documento: ", lugarExpedicion)
datos_cedula.append(lugarExpedicion)
print("==================================================")


#=================================================================================================================================
#-->PRUEBAS DE DATOS QUE SE QUIEREN EXTRAER
print("***************************************************************************************************************************")
print("arreglo de datos cedula")
print("Datos cedula => ", datos_cedula)

print("***************************************************************************************************************************")
print("diccionario variable cedula")
var_cedula={
    "numero":datos_cedula[0],
    "nombre":datos_cedula[1],
    "apellido":datos_cedula[2],
    "fecha de nacimiento":datos_cedula[3],
    "lugar de nacimiento":datos_cedula[4],
    "fecha de expedicion de documento":datos_cedula[5],
    "lugar de expedicion de documento": datos_cedula[6]}

print("var_cedula => ", var_cedula)
print("***************************************************************************************************************************")

#==============================================================================================================================================================================
#--> INSERTAR EN UNA TABLA EN BASE DE DATOS MYSQL

sql = "INSERT INTO ingenieros(numero, nombre, apellido, fecha_de_nacimiento, lugar_de_nacimiento, fecha_de_expedicion, lugar_de_expedicion) VALUES (%s, %s, %s, CAST(%s AS DATE), %s, CAST(%s AS DATE), %s)" 


val = (var_cedula["numero"], var_cedula["nombre"], var_cedula["apellido"], var_cedula["fecha de nacimiento"], var_cedula["lugar de nacimiento"], var_cedula["fecha de expedicion de documento"], var_cedula["lugar de expedicion de documento"])
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted")