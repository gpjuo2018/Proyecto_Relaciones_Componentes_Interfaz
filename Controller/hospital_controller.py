# controlador/hospital_controller.py
from typing import List, Optional
from Interface.crud_interface import CrudInterface
from Model.hospital import Hospital

class HospitalController(CrudInterface):
    def __init__(self):
        self.hospitales = {}
        self.next_id = 1
    
    def crear(self, hospital: Hospital) -> int:
        hospital.id = self.next_id
        self.hospitales[self.next_id] = hospital
        self.next_id += 1
        return hospital.id
    
    def obtener_todos(self) -> List[Hospital]:
        return list(self.hospitales.values())
    
    def obtener_por_id(self, id: int) -> Optional[Hospital]:
        return self.hospitales.get(id)
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Hospital]:
        """
        Obtiene un hospital por su nombre.
        
        Args:
            nombre: Nombre del hospital a buscar
            
        Returns:
            Optional[Hospital]: El hospital encontrado o None si no existe
        """
        for hospital in self.hospitales.values():
            if hospital.nombre.lower() == nombre.lower():
                return hospital
        return None
    
    def actualizar(self, id: int, hospital: Hospital) -> bool:
        if id not in self.hospitales:
            return False
        
        hospital.id = id
        self.hospitales[id] = hospital
        return True
    
    def eliminar(self, id: int) -> bool:
        if id not in self.hospitales:
            return False
        
        del self.hospitales[id]
        return True
