import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# --- Configuración de la pantalla ---
ancho, alto = 600, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Juego de la Serpiente')

# --- Colores ---
blanco = (255, 255, 255)
negro = (0, 0, 0)
verde = (0, 255, 0)
rojo = (255, 0, 0)

# --- Variables del juego ---
tamaño_bloque = 20
velocidad_serpiente = 15

# --- Reloj para controlar la velocidad ---
reloj = pygame.time.Clock()

# --- Fuente para el texto ---
fuente_puntuacion = pygame.font.Font(None, 35)

def dibujar_serpiente(bloques_serpiente):
    """Dibuja cada bloque de la serpiente."""
    for bloque in bloques_serpiente:
        pygame.draw.rect(pantalla, verde, [bloque[0], bloque[1], tamaño_bloque, tamaño_bloque])

def dibujar_comida(comida_pos):
    """Dibuja la comida."""
    pygame.draw.rect(pantalla, rojo, [comida_pos[0], comida_pos[1], tamaño_bloque, tamaño_bloque])

def mostrar_puntuacion(puntuacion):
    """Muestra la puntuación en la pantalla."""
    texto = fuente_puntuacion.render(f"Puntuación: {puntuacion}", True, negro)
    pantalla.blit(texto, [10, 10])

def mensaje_final(puntuacion):
    """Muestra el mensaje de fin del juego y la puntuación final."""
    fuente_final = pygame.font.Font(None, 50)
    texto_final = fuente_final.render(f"¡Fin del juego! Puntuación final: {puntuacion}", True, negro)
    rect_texto = texto_final.get_rect(center=(ancho // 2, alto // 2))
    pantalla.blit(texto_final, rect_texto)
    pygame.display.flip()
    pygame.time.delay(3000)  # Espera 3 segundos antes de salir

def bucle_juego():
    """Bucle principal del juego."""
    # Posición inicial de la serpiente
    x1 = ancho / 2
    y1 = alto / 2
    
    # Cambio de posición inicial (sin movimiento)
    x1_cambio = 0
    y1_cambio = 0
    
    # Lista para almacenar los bloques de la serpiente
    bloques_serpiente = []
    longitud_serpiente = 1
    puntuacion = 0
    
    # Posición inicial de la comida
    comida_pos = [round(random.randrange(0, ancho - tamaño_bloque) / tamaño_bloque) * tamaño_bloque,
                  round(random.randrange(0, alto - tamaño_bloque) / tamaño_bloque) * tamaño_bloque]
    
    juego_terminado = False
    
    while not juego_terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_terminado = True
            
            # Control de la serpiente con las teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x1_cambio == 0:
                    x1_cambio = -tamaño_bloque
                    y1_cambio = 0
                elif evento.key == pygame.K_RIGHT and x1_cambio == 0:
                    x1_cambio = tamaño_bloque
                    y1_cambio = 0
                elif evento.key == pygame.K_UP and y1_cambio == 0:
                    y1_cambio = -tamaño_bloque
                    x1_cambio = 0
                elif evento.key == pygame.K_DOWN and y1_cambio == 0:
                    y1_cambio = tamaño_bloque
                    x1_cambio = 0

        # Lógica del fin del juego (chocar con los bordes o consigo misma)
        if x1 >= ancho or x1 < 0 or y1 >= alto or y1 < 0:
            mensaje_final(puntuacion)
            juego_terminado = True
            
        x1 += x1_cambio
        y1 += y1_cambio

        pantalla.fill(blanco)
        
        dibujar_comida(comida_pos)
        
        cabeza_serpiente = [x1, y1]
        bloques_serpiente.append(cabeza_serpiente)
        
        # Eliminar el bloque de la cola si la serpiente no ha crecido
        if len(bloques_serpiente) > longitud_serpiente:
            del bloques_serpiente[0]

        # Lógica para chocar consigo misma
        for bloque in bloques_serpiente[:-1]:
            if bloque == cabeza_serpiente:
                mensaje_final(puntuacion)
                juego_terminado = True
                
        dibujar_serpiente(bloques_serpiente)
        mostrar_puntuacion(puntuacion)
        
        pygame.display.flip()
        
        # Lógica para comer la comida
        if x1 == comida_pos[0] and y1 == comida_pos[1]:
            comida_pos = [round(random.randrange(0, ancho - tamaño_bloque) / tamaño_bloque) * tamaño_bloque,
                          round(random.randrange(0, alto - tamaño_bloque) / tamaño_bloque) * tamaño_bloque]
            longitud_serpiente += 1
            puntuacion += 1

        reloj.tick(velocidad_serpiente)

    pygame.quit()
    sys.exit()

bucle_juego()