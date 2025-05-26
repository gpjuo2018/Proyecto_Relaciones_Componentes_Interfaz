# main.py
import sys
from PyQt5.QtWidgets import QApplication
from Controller.hospital_controller import HospitalController
from Controller.doctor_controller import DoctorController
from Gui.main_window import MainWindow
from Model.hospital import Hospital
from Model.doctor import Doctor

def main():
    # Inicializar controladores
    hospital_controller = HospitalController()
    doctor_controller = DoctorController(hospital_controller)
    
    # Crear algunos datos de ejemplo
    hospital1 = Hospital(nombre="Hospital General")
    hospital2 = Hospital(nombre="Clínica San José")
    
    hospital_controller.crear(hospital1)
    hospital_controller.crear(hospital2)
    
    doctor1 = Doctor(nombre="Dr. Juan Pérez", especialidad="Cardiología")
    doctor2 = Doctor(nombre="Dra. María López", especialidad="Pediatría")
    doctor3 = Doctor(nombre="Dr. Carlos Rodríguez", especialidad="Neurología")
    
    doctor_controller.crear(doctor1)
    doctor_controller.crear(doctor2)
    doctor_controller.crear(doctor3)
    
    hospital1.agregar_doctor(doctor1)
    hospital1.agregar_doctor(doctor2)
    hospital2.agregar_doctor(doctor3)
    
    # Inicializar aplicación PyQt5
    app = QApplication(sys.argv)
    window = MainWindow(hospital_controller, doctor_controller)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

