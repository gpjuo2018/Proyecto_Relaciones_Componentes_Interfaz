# modelo/interfaces/crud_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class CrudInterface(ABC):
    @abstractmethod
    def crear(self, entidad: Any) -> int:
        """
        Crea una nueva entidad en el sistema.
        
        Args:
            entidad: La entidad a crear
            
        Returns:
            int: El ID de la entidad creada
        """
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Any]:
        """
        Obtiene todas las entidades.
        
        Returns:
            List[Any]: Lista de entidades
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Any]:
        """
        Obtiene una entidad por su ID.
        
        Args:
            id: ID de la entidad a buscar
            
        Returns:
            Optional[Any]: La entidad encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def actualizar(self, id: int, entidad: Any) -> bool:
        """
        Actualiza una entidad existente.
        
        Args:
            id: ID de la entidad a actualizar
            entidad: Nueva información de la entidad
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina una entidad del sistema.
        
        Args:
            id: ID de la entidad a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        pass
