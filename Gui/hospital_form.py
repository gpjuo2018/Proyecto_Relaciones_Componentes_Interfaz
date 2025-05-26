# vista/hospital_form.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QHBoxLayout, QHeaderView, QMessageBox)
from Model.hospital import Hospital
from Controller.hospital_controller import HospitalController

class HospitalForm(QWidget):
    def __init__(self, hospital_controller: HospitalController):
        super().__init__()
        
        self.hospital_controller = hospital_controller
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)
        
        # Campos de entrada
        self.nombre_input = QLineEdit()
        form_layout.addRow("Nombre:", self.nombre_input)
        
        
        # Botones
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.guardar_hospital)
        button_layout.addWidget(self.save_button)
        
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.clicked.connect(self.limpiar_formulario)
        button_layout.addWidget(self.clear_button)
        
        # Tabla de hospitales
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Doctores"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)
        
        # Botones de acción para la tabla
        action_layout = QHBoxLayout()
        main_layout.addLayout(action_layout)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.editar_hospital)
        action_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.eliminar_hospital)
        action_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Actualizar Lista")
        self.refresh_button.clicked.connect(self.actualizar_tabla)
        action_layout.addWidget(self.refresh_button)
        
        # Inicializar tabla
        self.actualizar_tabla()
        
        # Variable para seguimiento del hospital en edición
        self.hospital_en_edicion = None
    
    def guardar_hospital(self):
        nombre = self.nombre_input.text().strip()
        
        if not nombre:
            QMessageBox.critical(self, "Error", "El nombre del hospital es obligatorio")
            return
        
        hospital = Hospital(nombre=nombre)
        
        if self.hospital_en_edicion:
            # Actualizar hospital existente
            exito = self.hospital_controller.actualizar(self.hospital_en_edicion, hospital)
            mensaje = "Hospital actualizado correctamente" if exito else "Error al actualizar el hospital"
            self.hospital_en_edicion = None
        else:
            # Crear nuevo hospital
            hospital_id = self.hospital_controller.crear(hospital)
            mensaje = f"Hospital creado correctamente con ID: {hospital_id}"
        
        QMessageBox.information(self, "Información", mensaje)
        self.limpiar_formulario()
        self.actualizar_tabla()
    
    def limpiar_formulario(self):
        self.nombre_input.clear()
        self.hospital_en_edicion = None
    
    def actualizar_tabla(self):
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Obtener todos los hospitales y agregarlos a la tabla
        hospitales = self.hospital_controller.obtener_todos()
        
        for hospital in hospitales:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(str(hospital.id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(hospital.nombre))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(len(hospital.doctores))))
    
    def editar_hospital(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un hospital para editar")
            return
        
        row = selected_rows[0].row()
        hospital_id = int(self.table.item(row, 0).text())
        
        hospital = self.hospital_controller.obtener_por_id(hospital_id)
        if hospital:
            self.nombre_input.setText(hospital.nombre)
            self.hospital_en_edicion = hospital_id
        else:
            QMessageBox.critical(self, "Error", "No se pudo cargar el hospital seleccionado")
    
    def eliminar_hospital(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un hospital para eliminar")
            return
        
        row = selected_rows[0].row()
        hospital_id = int(self.table.item(row, 0).text())
        
        confirmacion = QMessageBox.question(self, "Confirmar", "¿Está seguro de eliminar este hospital?",
                                          QMessageBox.Yes | QMessageBox.No)
        
        if confirmacion == QMessageBox.Yes:
            exito = self.hospital_controller.eliminar(hospital_id)
            if exito:
                QMessageBox.information(self, "Información", "Hospital eliminado correctamente")
                self.actualizar_tabla()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el hospital")
