# 🚀 Space Invaders - Pygame Version

Una recreación clásica del legendario juego de arcade **Space Invaders**, construida utilizando **Python** y la librería **Pygame**. El objetivo es defender la Tierra de una invasión alienígena interminable, destruyendo las naves enemigas antes de que lleguen al fondo de la pantalla.

## 📋 Características
  
  * **Mecánicas clásicas:** Movimientos lateral, vertical y disparos de proyectiles.
  * **Enemigos dinámicos:** La nave alienígena (por ahora solo una) se mueven en bloque y descienden al llegar a los bordes.
  * **Game Over:** Detección de colisión cuando el enemigo es alcanzado por un proyectil, toca al jugador o el límite inferior de la pantalla del juego.

-----

## 🛠️ Requisitos del Sistema

Para ejecutar este juego, necesitarás tener instalado:

  * **Python 3.x** (Se recomienda la versión 3.10 o superior).
  * **Pygame** (Librería gráfica).

-----

## 🔧 Instalación y Ejecución

Sigue estos pasos para probar el juego en tu computadora:

### 1\. Clonar el repositorio

Descarga el código fuente a tu máquina local:

```bash
git clone https://github.com/freddyB19/space-invaders-pygame.git
cd space-invaders-pygame
```

### 2\. Crear un entorno virtual (Opcional pero recomendado)

Es una buena práctica para mantener limpias tus dependencias:

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Instalar dependencias

Instala Pygame usando `pip`:

```bash
pip install pygame
```

*(Nota: usa el archivo `requirements.txt`, usando `pip install -r requirements.txt`)*

### 4\. Ejecutar el juego

Inicia el archivo principal:

```bash
python main.py
```

-----

## 🎮 Controles

El manejo de la nave es muy sencillo:

| Tecla | Acción |
| :--- | :--- |
| **Flecha Izquierda** (`←`, `a`) | Mover nave a la izquierda |
| **Flecha Derecha** (`→`, `d`) | Mover nave a la derecha |
| **Barra Espaciadora** | Disparar láser |
| **Esc** | Salir del juego |

-----

## 📂 Estructura del Proyecto

Así está organizado el código fuente:

  * `main.py`: Punto de entrada del juego:
    - Lógica para controlar la nave.
    - Lógica de los movimientos del enemigo.
    - Manejo de los disparos (física y colisiones)
  * `/assets`: Carpeta que contiene imágenes (sprites) y sonidos.

-----

## 🔮 Próximas Mejoras (To-Do)

  * [ ] Organizar el código fuente.
  * [ ] Crear diferentes tipos de enemigos con distintos comportamientos.
  * [ ] Sistema de puntuación: Acumula puntos por cada enemigo derribado.
  * [ ] Implementar sistema de "High Score" (Puntuación máxima).
  * [ ] Mejorar sistema de disparos.
  * [ ] Añadir un menú de inicio.
  * [ ] Añadir barreras defensivas (búnkeres).
  * [ ] Sonidos y efectos: Efectos de disparo y explosiones retro.
-----

## 📝 Créditos

Desarrollado por **[Freddy Bolívar]**.
Este proyecto es con fines educativos para aprender desarrollo de videojuegos con Python.
