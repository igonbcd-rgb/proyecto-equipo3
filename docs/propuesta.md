# Hito 1. Propuesta

## Proyecto: Diagnóstico de tumor benigno o maligno

### 1. Problema y usuarios

Nuestro proyecto consiste en crear un programa que utilice inteligencia artificial para ayudar a identificar si un tumor de mama es benigno o maligno. Está pensado principalmente para estudiantes y personas interesadas en conocer cómo se puede utilizar la inteligencia artificial en el área de la salud. Este programa será una herramienta de apoyo para aprender y no reemplazará la revisión ni el diagnóstico de un médico.

### 2. Datos

Para realizar el proyecto utilizaremos una base de datos llamada **Breast Cancer Wisconsin (Diagnostic)**, que contiene información sobre diferentes tumores de mama.

- Fuente: https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
- Cantidad de registros: 569.
- Información: 30 características de los tumores, como su tamaño, forma, textura y otras características.
- Resultado que buscamos: saber si el tumor es benigno o maligno.

### 3. Algoritmo

Utilizaremos un método llamado **Regresión Logística**, que ayudará al programa a aprender de los datos y después identificar si un tumor es benigno o maligno. Lo elegimos porque permite trabajar con dos posibles resultados y no necesita una computadora muy potente para funcionar.

### 4. Resultados esperados

Queremos que nuestro programa tenga buenos resultados al identificar los tumores.

Buscamos conseguir:

- Exactitud: mínimo 90%.
- F1: mínimo 90%.
- Identificación de tumores malignos: mínimo 90%.

Lo más importante será evitar que un tumor maligno sea identificado por error como benigno.

### 5. Recursos de cómputo

Para realizar el proyecto utilizaremos una laptop o GitHub Codespaces, donde trabajaremos con Python y las herramientas necesarias para crear el programa. También revisaremos cuánto tiempo tarda en funcionar y cuánta memoria utiliza.

### 6. Riesgos iniciales

1. El programa podría equivocarse al identificar algunos tumores.
2. La información de la base de datos puede no incluir todos los tipos de casos que existen en la vida real.
3. Como es un proyecto relacionado con la salud, debemos cuidar la información y dejar claro que el programa no sustituye la opinión de un médico.

### 7. Reparto de actividades

- **Integrante A:** se encargará de organizar la información y crear el programa que identificará los tumores.
- **Integrante B:** desarrollará la conexión del programa con la página web.
- **Integrante C:** realizará las pruebas, ayudará a preparar el proyecto para su funcionamiento y apoyará con su publicación.

Los tres integrantes participaremos en la revisión del proyecto, la documentación y la presentación final