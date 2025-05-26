# controlador/doctor_controller.py
from typing import List, Optional
from Interface.crud_interface import CrudInterface
from Model.doctor import Doctor
from Controller.hospital_controller import HospitalController

class DoctorController(CrudInterface):
    def __init__(self, hospital_controller: HospitalController):
        self.doctores = {}
        self.next_id = 1
        self.hospital_controller = hospital_controller
    
    def crear(self, doctor: Doctor) -> int:
        doctor.id = self.next_id
        self.doctores[self.next_id] = doctor
        self.next_id += 1
        return doctor.id
    
    def obtener_todos(self) -> List[Doctor]:
        return list(self.doctores.values())
    
    def obtener_por_id(self, id: int) -> Optional[Doctor]:
        return self.doctores.get(id)
    
    def obtener_por_id_y_hospital(self, doctor_id: int, hospital_nombre: str) -> Optional[Doctor]:
        """
        Obtiene un doctor por su ID y el nombre del hospital.
        
        Args:
            doctor_id: ID del doctor a buscar
            hospital_nombre: Nombre del hospital al que pertenece el doctor
            
        Returns:
            Optional[Doctor]: El doctor encontrado o None si no existe
        """
        doctor = self.obtener_por_id(doctor_id)
        if doctor and doctor.hospital and doctor.hospital.nombre.lower() == hospital_nombre.lower():
            return doctor
        return None
    
    def actualizar(self, id: int, doctor: Doctor) -> bool:
        if id not in self.doctores:
            return False
        
        doctor.id = id
        self.doctores[id] = doctor
        return True
    
    def eliminar(self, id: int) -> bool:
        if id not in self.doctores:
            return False
        
        del self.doctores[id]
        return True
