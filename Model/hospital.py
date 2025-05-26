class Hospital:
    def __init__(self, id: int = None, nombre: str = ""):
        self.id = id
        self.nombre = nombre
        self.doctores = []
    
    def agregar_doctor(self, doctor):
        """
        Agrega un doctor al hospital.
        
        Args:
            doctor: Doctor a agregar
        """
        self.doctores.append(doctor)
        doctor.hospital = self
    
    def __str__(self) -> str:
        return f"Hospital(id={self.id}, nombre='{self.nombre}', doctores={len(self.doctores)})"
