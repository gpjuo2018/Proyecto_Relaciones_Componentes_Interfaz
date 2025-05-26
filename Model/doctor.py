class Doctor:
    def __init__(self, id: int = None, nombre: str = "", especialidad: str = "", hospital = None):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
        self.hospital = hospital
    
    def __str__(self) -> str:
        hospital_nombre = self.hospital.nombre if self.hospital else "No asignado"
        return f"Doctor(id={self.id}, nombre='{self.nombre}', especialidad='{self.especialidad}', hospital='{hospital_nombre}')"
