import pygame

class Entity:
    _id_counter = 0
    def __init__(self):
        self.id = Entity._id_counter
        Entity._id_counter += 1
        self.components = {}

    def add_component(self, component_name, component):
        self.components[component_name] = component

    def get_component(self, component_name):
        return self.components[component_name]
    
    def has_component(self, component_name):
        if self.components[component_name]:
            return True
        return False
    
    def __repr__(self):
        return f"Id: {self.id}, Components: ({len(self.components)})"

class Component:
    pass

class System:
    def __init__(self):
        self.entities = []

    def add_entity(self, entity):
        if not hasattr(self, "entities"):
            raise AttributeError(f"{self.__class__.__name__} is not instantiated correctly.")
        self.entities.append(entity)

    def update(self, delta_time):
        pass

class TransformNode:
    def __init__(self, position=(0, 0), parent=None):
        self.position = position
        self.children = []
        self.parent = parent
        if parent:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def get_world_position(self):
        if self.parent:
            px, py = self.parent.get_world_position()
            return px + self.position[0], py + self.position[1]
        return self.position
