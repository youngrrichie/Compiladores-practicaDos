# PracticaDos-Compiladores
# Implementación de un Parser Descendente Recursivo

**Camacho Zavala Ricardo**

**Valverde Rojas Gustavo**

Esta práctica tuvo como finalidad desarrollar un analizador sintáctico recursivo simple que permita comprender como la forma de
la gramática puede afectar el funcionamiento del analizador.

Este programa fue desarrollado con el entorno grafico Tkinter de Python 

## Estructura del Proyecto

La aplicación esta separada por módulos (A, B y D), cada uno de ellos demuestra claramente los problemas de recursión izquierda en el módulo A, cómo se resuelven en el módulo B, y la utilidad del backtracking manual en el módulo D.

- **Modulo A**: Se implementa la recursión a la izquierda y muestra los problemas de recursión infinita cuando se analizan ciertas entradas. 

- **Modulo B**: Elimina la recursión a la izquierda y muestra cómo funciona correctamente el parser después de las transformaciones.

- **Modulo C**: Se implementa parsers con y sin backtracking para mostrar las diferencias.

## Evidencia de Funcionamiento 

- **Modulo A**:
  Ejemplo que causa recursión infinita con la primer gramatica: id + id * id 
  ![image](https://github.com/user-attachments/assets/0f058603-f5a1-4e00-a18d-82d35963b691)

- **Modulo B**:
  Ejemplo con la segunda gramatica que muestra entrada válida: (num (id num))
  ![image](https://github.com/user-attachments/assets/cd5223f8-fb86-44ba-9a48-4079ccc0e318)

- **Modulo C**:
  Prueba con bactracking desactivado, pero con activado tendrá el mismo resultado: ab
  ![image](https://github.com/user-attachments/assets/b0c412f2-cc50-4126-82a2-3664fb4c1a8c)

## Instrucciones de Ejecución 

1. **Clonar el repositorio:**
   ```sh
   git clone https://github.com/youngrrichie/Compiladores-practicaDos.git
   ```
2. **Ejecutar main.py para iniciar la aplicación.**
    
3. **Ejecutar main.py para iniciar la aplicación.**
    
4.  **Elegir la gramática específica a utilizar.**
   
5.  **Ingresar la cadena a analizar en el campo de entrada y clck en Analizar**

## Errores conocidos 

Puede haber errores como no poder compilar el entorno gráfico, para eso se requiere clonar el repositorio en cualquier carpeta y ejecutarlo desde ahí.
