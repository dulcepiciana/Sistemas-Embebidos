class FingerprintSimulator:
    FINGERPRINT_OK = 0
    FINGERPRINT_NOFINGER = 1

    def __init__(self):
        self.fingerID = None
        self.confidence = 0
        self.templates = {}  # Diccionario para guardar huellas simuladas {id: "fingerprint_data"}

    def verifyPassword(self):
        return True

    def getImage(self):
        # Simula que siempre hay dedo
        return self.FINGERPRINT_OK

    def image2Tz(self, slot=1):
        # Simula conversión de imagen, siempre OK
        return self.FINGERPRINT_OK

    def fingerSearch(self):
        # Simula búsqueda, devuelve el primer ID si hay alguna huella guardada
        if self.templates:
            # Devuelve la primera huella guardada arbitrariamente
            self.fingerID = list(self.templates.keys())[0]
            self.confidence = 100  # confianza alta
            return self.FINGERPRINT_OK
        else:
            return 2  # Simula que no encontró coincidencia

    def getParameters(self):
        self.status_reg = 0x00
        self.system_id = 0x0001
        self.capacity = 127
        self.security_level = 5

    def getTemplateCount(self):
        self.templateCount = len(self.templates)

    def createModel(self):
        return self.FINGERPRINT_OK

    def storeModel(self, id):
        if 1 <= id <= 127:
            self.templates[id] = "fingerprint_data"
            return self.FINGERPRINT_OK
        else:
            return 3  # Error simulada

    def deleteModel(self, id):
        if id in self.templates:
            del self.templates[id]
            return self.FINGERPRINT_OK
        else:
            return 4  # No encontrada


# Funciones simuladas para enrolar, buscar y eliminar

def enrolarHuella(finger):
    print("\n=== MODO ENROLAMIENTO ===")
    id = int(input("Ingrese ID para registrar (1-127): "))
    if id < 1 or id > 127:
        print("ID inválido. Debe estar entre 1 y 127.")
        return
    print(f"Enrolando ID #{id}...")
    print("Coloque su dedo en el sensor (simulado)...")
    while finger.getImage() != finger.FINGERPRINT_OK:
        print(".", end="", flush=True)
    if finger.image2Tz(1) != finger.FINGERPRINT_OK:
        print("Error al procesar la imagen")
        return
    print("Retire el dedo (simulado)")
    # Simula espera
    input("Presione Enter para continuar...")
    print("Coloque el mismo dedo nuevamente (simulado)...")
    while finger.getImage() != finger.FINGERPRINT_OK:
        print(".", end="", flush=True)
    if finger.image2Tz(2) != finger.FINGERPRINT_OK:
        print("Error al procesar la segunda imagen")
        return
    print("Creando modelo de huella...")
    if finger.createModel() != finger.FINGERPRINT_OK:
        print("Error al crear el modelo. Las huellas no coinciden")
        return
    print(f"Guardando modelo en ID #{id}...")
    if finger.storeModel(id) == finger.FINGERPRINT_OK:
        print("¡Huella guardada exitosamente!")
    else:
        print("Error al guardar la huella")

def eliminarHuella(finger):
    print("\n=== MODO ELIMINACIÓN ===")
    id = int(input("Ingrese ID a eliminar (1-127): "))
    if id < 1 or id > 127:
        print("ID inválido. Debe estar entre 1 y 127.")
        return
    print(f"Eliminando ID #{id}...")
    if finger.deleteModel(id) == finger.FINGERPRINT_OK:
        print("¡Huella eliminada exitosamente!")
    else:
        print("Error al eliminar la huella o ID no encontrada")

def buscarHuella(finger):
    print("\n=== MODO BÚSQUEDA ===")
    print("Coloque su dedo en el sensor (simulado)...")
    while finger.getImage() != finger.FINGERPRINT_OK:
        print(".", end="", flush=True)
    if finger.image2Tz() != finger.FINGERPRINT_OK:
        print("Error al procesar la imagen")
        return
    if finger.fingerSearch() == finger.FINGERPRINT_OK:
        print(f"¡Huella encontrada! ID #{finger.fingerID} con nivel de confianza: {finger.confidence}")
    else:
        print("No se encontró coincidencia")


def main():
    finger = FingerprintSimulator()
    if finger.verifyPassword():
        print("Simulador de sensor listo.\n")
    else:
        print("Error en simulador.")
        return

    finger.getParameters()
    finger.getTemplateCount()
    print(f"Capacidad: {finger.capacity}")
    print(f"Huellas almacenadas: {finger.templateCount}")

    while True:
        print("\n--- COMANDOS DISPONIBLES ---")
        print("E - Enrolar una nueva huella")
        print("D - Eliminar una huella")
        print("B - Buscar una huella")
        print("Q - Salir")
        cmd = input("Ingrese comando: ").strip().upper()

        if cmd == 'E':
            enrolarHuella(finger)
        elif cmd == 'D':
            eliminarHuella(finger)
        elif cmd == 'B':
            buscarHuella(finger)
        elif cmd == 'Q':
            print("Saliendo...")
            break
        else:
            print("Comando no válido.")

if __name__ == "__main__":
    main()
