

1. ¿Por qué queue.Queue es apropiada para compartir trabajos?
Porque es una cola FIFO que ya viene lista para usar con hilos permite que varios trabajadores saquen elementos al mismo tiempo sin que se repitan los documentos ni haya problemas de concurrencia.

2. ¿Qué protege Lock y qué pasaría si se actualizara el resumen sin él?
Protege las variables que comparten los hilos, si no se usa el lock varios hilos intentarían escribir al mismo tiempo y se perderían datos o los totales saldrian mal.

3. ¿Qué cambiarías si cada documento tuviera que guardarse en un archivo real?
Haría que cada hilo guarde su propio archivo para evitar problemas de escritura, si todos tienen que escribir en un solo archivo le pondría un lock para que no se pisen los datos.

4. Análisis sobre el Reto Adicional (Tiempo y Concurrencia vs Secuencial)
En tareas pesadas la versión con hilos termina mas rápido, pero si el tiempo es parecido al secuencial es por la sobrecarga de crear los hilos en Python, las tareas eran muy pequeñas y tardo mas la sincronizacion que el trabajo en sí.