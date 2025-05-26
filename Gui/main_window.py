# vista/main_window.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                            QVBoxLayout, QWidget, QLabel, QLineEdit, 
                            QPushButton, QTextEdit, QFormLayout, QMessageBox)
from Gui.hospital_form import HospitalForm
from Gui.doctor_form import DoctorForm
from Controller.hospital_controller import HospitalController
from Controller.doctor_controller import DoctorController

class MainWindow(QMainWindow):
    def __init__(self, hospital_controller: HospitalController, doctor_controller: DoctorController):
        super().__init__()
        
        self.hospital_controller = hospital_controller
        self.doctor_controller = doctor_controller
        
        self.setWindowTitle("Sistema de Información Hospitalaria")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Crear pestañas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Pestaña de Hospitales
        self.hospital_form = HospitalForm(self.hospital_controller)
        self.tab_widget.addTab(self.hospital_form, "Hospitales")
        
        # Pestaña de Doctores
        self.doctor_form = DoctorForm(self.doctor_controller, self.hospital_controller)
        self.tab_widget.addTab(self.doctor_form, "Doctores")
        
        # Pestaña de Búsqueda
        self.search_tab = QWidget()
        self.tab_widget.addTab(self.search_tab, "Búsqueda")
        self.setup_search_tab()
    
    def setup_search_tab(self):
        # Layout para la pestaña de búsqueda
        search_layout = QVBoxLayout(self.search_tab)
        
        # Formulario de búsqueda
        form_layout = QFormLayout()
        search_layout.addLayout(form_layout)
        
        # Campos de entrada
        self.doctor_id_input = QLineEdit()
        form_layout.addRow("ID del Doctor:", self.doctor_id_input)
        
        self.hospital_name_input = QLineEdit()
        form_layout.addRow("Nombre del Hospital:", self.hospital_name_input)
        
        # Botón de búsqueda
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_doctor)
        search_layout.addWidget(search_button)
        
        # Área de resultados
        result_label = QLabel("Resultados:")
        search_layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        search_layout.addWidget(self.result_text)
    
    def search_doctor(self):
        try:
            doctor_id = int(self.doctor_id_input.text())
            hospital_name = self.hospital_name_input.text()
            
            doctor = self.doctor_controller.obtener_por_id_y_hospital(doctor_id, hospital_name)
            
            self.result_text.clear()
            
            if doctor:
                self.result_text.append(f"Doctor encontrado:\n")
                self.result_text.append(f"ID: {doctor.id}")
                self.result_text.append(f"Nombre: {doctor.nombre}")
                self.result_text.append(f"Especialidad: {doctor.especialidad}")
                self.result_text.append(f"Hospital: {doctor.hospital.nombre}")
            else:
                self.result_text.append("No se encontró ningún doctor con el ID y hospital especificados.")
        except ValueError:
            self.result_text.clear()
            self.result_text.append("Por favor, ingrese un ID de doctor válido (número entero).")
