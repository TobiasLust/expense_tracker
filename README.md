# Expense Tracker

Expense Tracker es una herramienta de línea de comandos en Python que permite gestionar y realizar un seguimiento de tus gastos de forma sencilla. Puedes agregar, eliminar, actualizar, listar y exportar tus gastos, además de establecer un presupuesto mensual y obtener un resumen de tus gastos.

## Características

- **Agregar gastos**: Añade nuevos gastos con descripción, categoría, y monto.
- **Eliminar gastos**: Elimina un gasto existente utilizando su ID.
- **Actualizar gastos**: Actualiza la descripción, categoría o monto de un gasto existente.
- **Listar gastos**: Muestra todos los gastos registrados, con la opción de filtrar por categoría.
- **Resumen de gastos**: Muestra el resumen total de los gastos, con la opción de ver solo los gastos de un mes específico.
- **Establecer presupuesto**: Configura un presupuesto mensual para controlar los gastos.
- **Exportar a CSV**: Exporta todos los gastos a un archivo CSV.

## Instalación

1.Clona este repositorio en tu máquina local:

```bash
   git clone https://github.com/TobiasLust/expense_tracker.git
```

2.Navega al directorio del proyecto:

```bash
    cd expense-tracker
```

## Estructura del Proyecto

expense_tracker.py: Contiene la lógica principal de la aplicación.

expenses.json: Archivo donde se almacenan los datos de los gastos. Like this:

budgets.json: Archivo donde se almacenan los presupuestos mensuales.

## Uso

Puedes usar la herramienta directamente desde la línea de comandos. Aquí hay algunos ejemplos de cómo usar cada comando:

```bash
# Agregar un gasto
python main.py add -d "Compra de supermercado" -c "groceries" -a 200

# Eliminar un gasto
python main.py delete --id 1

# Actualizar un gasto
python main.py update --id 1 -d "Compra semanal supermercado" -a 250

# Listar todos los gastos
python main.py list

# Listar gastos por categoría
python main.py list -c "groceries"

# Obtener un resumen de los gastos
python main.py summary

# Obtener un resumen de los gastos de un mes específico
python main.py summary --month 5

# Establecer un presupuesto mensual
python main.py setbudget --month 5 -a 1000

# Exportar los gastos a un archivo CSV
python main.py export
```
