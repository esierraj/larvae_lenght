import cv2  # Paquete de procesamiento y análisis de imagen
import math  # Modulo de funciones matemáticas

## Definición de funciones

# Función para medir la longitud entre dos puntos
def calcular_distancia(punto1, punto2):
    return math.sqrt((punto2[0] - punto1[0]) ** 2 + (punto2[1] - punto1[1]) ** 2)

# Función para calcular la escala de la imagen 
def seleccionar_punto(event, x, y, flags, param):
    global puntos_escala, escala
    if event == cv2.EVENT_LBUTTONDOWN:  # Al presionar el botón izquierdo del mouse
        puntos_escala.append((x, y))
        cv2.circle(imagen_escala, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Ajuste de escala", imagen_escala)

        if len(puntos_escala) == 2:            # Al presionar el botón izquierdo del mouse dos veces
            distancia = calcular_distancia(puntos_escala[0], puntos_escala[1])
            print(f"Distancia entre los puntos: {distancia} píxeles")
            cv2.line(imagen_escala, puntos_escala[0], puntos_escala[1], (255, 0, 0), 2)    # Graficar línea entre los puntos
            cv2.imshow("Ajuste de escala", imagen_escala)
            escala = distancia / longitud
            print(f"Escala: {escala} pi/cm")

# Función para calcular la longitud de la larva
def seleccionar_punto_long(event, x, y, flags, param):
    global puntos_larva
    if event == cv2.EVENT_LBUTTONDOWN:     # Al presionar el botón izquierdo del mouse
        puntos_larva.append((x, y))
        cv2.circle(imagen_larva, (x, y), 5, (0, 255, 0), -1)     # 
        cv2.imshow("Calculo de la longitud de la larva", imagen_larva)
        

        if len(puntos_larva) >= 1:            # Al presionar el botón del mouse más de una vez
            try:
                distancia = (calcular_distancia(puntos_larva[-1], puntos_larva[-2]))/escala
                lista_dist.append(distancia)
                cv2.line(imagen_larva, puntos_larva[-1], puntos_larva[-2], (255, 0, 0), 2)    # Graficar línea entre los puntos
                cv2.imshow("Calculo de la longitud de la larva", imagen_larva)
            except IndexError:
                pass



## Variables globales del código
escala = None        # Escala en pi/cm para conversión de unidades de distancia
puntos_escala = []   # Lista que almacenará los dos puntos que se ubicarán en la imagen para encontrar la escala
puntos_larva = []    # Lista que almacenará los puntos que se ubicarán en la imagen para medir la larva
 
## Cargar la imagen usando OpenCV
ruta_imagen = "c:/Users/EGWER/Desktop/Carpeta prueba/fotos_pruebas/prueba_larva (5).jpg" # Ruta en la que se encuentra guardada la imagen
imagen_cv2 = cv2.imread(ruta_imagen)

## Redimensionar la imagen si es necesario
porcentaje_reduccion = 74.5  # Ej: Escribir 20 si se quiere una reducción del 20% en las dimensiones de la imagen
nuevo_ancho = int(imagen_cv2.shape[1] * ((100 - porcentaje_reduccion) / 100))
nuevo_alto = int(imagen_cv2.shape[0] * ((100 - porcentaje_reduccion) / 100))
imagen_cv2 = cv2.resize(imagen_cv2, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)  # Generar nueva imagen

## Ajuste de escala

# Establecer un valor para la escala
resp = input('¿Ajustar escala?: ')

if resp.lower() in ["si", "sí"]:
    longitud = float(input('Longitud conocida en cm: '))

    # Mostrar la imagen para la selección de puntos
    imagen_escala = cv2.imread(ruta_imagen)
    imagen_escala = cv2.resize(imagen_escala, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)
    
    cv2.imshow("Ajuste de escala", imagen_escala)
    cv2.setMouseCallback("Ajuste de escala", seleccionar_punto)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Si no se ajusta la escala o no se seleccionan dos puntos, usa un valor predeterminado. Útil cuando se tienen muchas imágenes similares.
if escala is None:
    escala = 200 
    print(f"Usando escala predeterminada: {escala} pi/cm")

## Calcular la longitud de la larva

lista_dist = [] # Lista que almacenará las distancias entre los puntos seleccionados en la imagen

# Mostrar la imagen para la selección de puntos
imagen_larva = cv2.imread(ruta_imagen)
imagen_larva = cv2.resize(imagen_larva, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)

cv2.imshow("Calculo de la longitud de la larva", imagen_larva)
cv2.setMouseCallback("Calculo de la longitud de la larva", seleccionar_punto_long)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Calcular la longitud total de la larva
cuenta_long = 0
for distancias in lista_dist:
    cuenta_long += distancias
print(f'La longitud de la larva es {round(cuenta_long,3)} cm')


