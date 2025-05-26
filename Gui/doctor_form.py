# vista/doctor_form.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QHBoxLayout, QHeaderView, QMessageBox, QComboBox)
from Model.doctor import Doctor
from Controller.doctor_controller import DoctorController
from Controller.hospital_controller import HospitalController

class DoctorForm(QWidget):
    def __init__(self, doctor_controller: DoctorController, hospital_controller: HospitalController):
        super().__init__()
        
        self.doctor_controller = doctor_controller
        self.hospital_controller = hospital_controller
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)
        
        # Campos de entrada
        self.nombre_input = QLineEdit()
        form_layout.addRow("Nombre:", self.nombre_input)
        
        self.especialidad_input = QLineEdit()
        form_layout.addRow("Especialidad:", self.especialidad_input)
        
        self.hospital_combo = QComboBox()
        form_layout.addRow("Hospital:", self.hospital_combo)
        self.actualizar_hospitales_combo()
        
        # Botones
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.guardar_doctor)
        button_layout.addWidget(self.save_button)
        
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.clicked.connect(self.limpiar_formulario)
        button_layout.addWidget(self.clear_button)
        
        # Tabla de doctores
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Especialidad", "Hospital"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)
        
        # Botones de acción para la tabla
        action_layout = QHBoxLayout()
        main_layout.addLayout(action_layout)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.editar_doctor)
        action_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.eliminar_doctor)
        action_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Actualizar Lista")
        self.refresh_button.clicked.connect(self.actualizar_tabla)
        action_layout.addWidget(self.refresh_button)
        
        # Inicializar tabla
        self.actualizar_tabla()
        
        # Variable para seguimiento del doctor en edición
        self.doctor_en_edicion = None
    
    def actualizar_hospitales_combo(self):
        self.hospital_combo.clear()
        hospitales = self.hospital_controller.obtener_todos()
        for hospital in hospitales:
            self.hospital_combo.addItem(hospital.nombre)
    
    def guardar_doctor(self):
        nombre = self.nombre_input.text().strip()
        especialidad = self.especialidad_input.text().strip()
        hospital_nombre = self.hospital_combo.currentText()
        
        if not nombre:
            QMessageBox.critical(self, "Error", "El nombre del doctor es obligatorio")
            return
        
        if not hospital_nombre:
            QMessageBox.critical(self, "Error", "Debe seleccionar un hospital")
            return
        
        hospital = self.hospital_controller.obtener_por_nombre(hospital_nombre)
        if not hospital:
            QMessageBox.critical(self, "Error", "El hospital seleccionado no existe")
            return
        
        doctor = Doctor(nombre=nombre, especialidad=especialidad)
        
        if self.doctor_en_edicion:
            # Actualizar doctor existente
            doctor_actual = self.doctor_controller.obtener_por_id(self.doctor_en_edicion)
            if doctor_actual and doctor_actual.hospital:
                # Remover de hospital anterior si cambió
                if doctor_actual.hospital.id != hospital.id:
                    if doctor_actual.hospital.doctores and doctor_actual in doctor_actual.hospital.doctores:
                        doctor_actual.hospital.doctores.remove(doctor_actual)
            
            doctor.id = self.doctor_en_edicion
            exito = self.doctor_controller.actualizar(self.doctor_en_edicion, doctor)
            hospital.agregar_doctor(doctor)
            mensaje = "Doctor actualizado correctamente" if exito else "Error al actualizar el doctor"
            self.doctor_en_edicion = None
        else:
            # Crear nuevo doctor
            doctor_id = self.doctor_controller.crear(doctor)
            hospital.agregar_doctor(doctor)
            mensaje = f"Doctor creado correctamente con ID: {doctor_id}"
        
        QMessageBox.information(self, "Información", mensaje)
        self.limpiar_formulario()
        self.actualizar_tabla()
    
    def limpiar_formulario(self):
        self.nombre_input.clear()
        self.especialidad_input.clear()
        self.doctor_en_edicion = None
    
    def actualizar_tabla(self):
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Obtener todos los doctores y agregarlos a la tabla
        doctores = self.doctor_controller.obtener_todos()
        
        for doctor in doctores:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            hospital_nombre = doctor.hospital.nombre if doctor.hospital else "No asignado"
            
            self.table.setItem(row_position, 0, QTableWidgetItem(str(doctor.id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(doctor.nombre))
            self.table.setItem(row_position, 2, QTableWidgetItem(doctor.especialidad))
            self.table.setItem(row_position, 3, QTableWidgetItem(hospital_nombre))
    
    def editar_doctor(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un doctor para editar")
            return
        
        row = selected_rows[0].row()
        doctor_id = int(self.table.item(row, 0).text())
        
        doctor = self.doctor_controller.obtener_por_id(doctor_id)
        if doctor:
            self.nombre_input.setText(doctor.nombre)
            self.especialidad_input.setText(doctor.especialidad)
            
            if doctor.hospital:
                index = self.hospital_combo.findText(doctor.hospital.nombre)
                if index >= 0:
                    self.hospital_combo.setCurrentIndex(index)
            
            self.doctor_en_edicion = doctor_id
        else:
            QMessageBox.critical(self, "Error", "No se pudo cargar el doctor seleccionado")
    
    def eliminar_doctor(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un doctor para eliminar")
            return
        
        row = selected_rows[0].row()
        doctor_id = int(self.table.item(row, 0).text())
        
        confirmacion = QMessageBox.question(self, "Confirmar", "¿Está seguro de eliminar este doctor?",
                                          QMessageBox.Yes | QMessageBox.No)
        
        if confirmacion == QMessageBox.Yes:
            doctor = self.doctor_controller.obtener_por_id(doctor_id)
            if doctor and doctor.hospital:
                if doctor.hospital.doctores and doctor in doctor.hospital.doctores:
                    doctor.hospital.doctores.remove(doctor)
            
            exito = self.doctor_controller.eliminar(doctor_id)
            if exito:
                QMessageBox.information(self, "Información", "Doctor eliminado correctamente")
                self.actualizar_tabla()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el doctor")
