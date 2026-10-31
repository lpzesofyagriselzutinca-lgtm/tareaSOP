import queue
import random
import threading
import time


def trabajador(nombre, cola_documentos, resultados, lock_resultados, registro_detallado):
    while True:
        try:
            documento = cola_documentos.get_nowait()
        except queue.Empty:
            break

        time.sleep(random.uniform(0.05, 0.15))

        with lock_resultados:
            resultados[nombre]["documentos_procesados"] += 1
            resultados[nombre]["tamano_acumulado"] += documento["tamano"]
            registro_detallado.append({
                "doc_id": documento["id"],
                "trabajador": nombre,
                "tamano": documento["tamano"]
            })

        cola_documentos.task_done()


def main():
    total_docs = 24
    cola_documentos = queue.Queue()
    
    for i in range(1, total_docs + 1):
        cola_documentos.put({
            "id": f"DOC-{i:03d}",
            "tamano": random.randint(10, 500)
        })

    resultados = {}
    cantidad_hilos = 4
    for i in range(1, cantidad_hilos + 1):
        resultados[f"Trabajador-{i}"] = {
            "documentos_procesados": 0,
            "tamano_acumulado": 0
        }

    lock_resultados = threading.Lock()
    registro_detallado = []

    inicio = time.time()

    hilos = []
    for i in range(1, cantidad_hilos + 1):
        nombre = f"Trabajador-{i}"
        hilo = threading.Thread(
            target=trabajador,
            args=(nombre, cola_documentos, resultados, lock_resultados, registro_detallado)
        )
        hilos.append(hilo)

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    duracion = time.time() - inicio

    print("=" * 50)
    print("RESUMEN DE EJECUCIÓN")
    print("=" * 50)
    
    documentos_totales = sum(datos["documentos_procesados"] for datos in resultados.values())
    for trabajador_nombre, datos in sorted(resultados.items()):
        print(f"{trabajador_nombre}: {datos['documentos_procesados']} documentos procesados | Tamaño total: {datos['tamano_acumulado']}")

    print("-" * 50)
    print(f"Total procesado: {documentos_totales} de {total_docs}")
    print(f"Tiempo transcurrido: {duracion:.2f} segundos")

    assert documentos_totales == 24, "Error: la cantidad de documentos procesados no coincide con 24."
    print("Verificación 1 aprobada: Se procesaron exactamente 24 documentos.")

    ids = [registro["doc_id"] for registro in registro_detallado]
    assert len(ids) == len(set(ids)) == 24, "Error: se encontraron identificadores duplicados o incompletos."
    print("Verificación 2 aprobada: Cada identificador fue procesado una sola vez.")

    print("Verificación 3 aprobada: La totalidad de los hilos finalizó de manera exitosa.")
    print("=" * 50)


if __name__ == "__main__":
    main()