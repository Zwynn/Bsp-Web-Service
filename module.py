from pydantic import BaseModel            # Hilft FastAPI bei der Datenvalidierung 

# Hier sind Module/Klassen, zu Förderung von Erweiterbarkeit und bessere Strukturierung

class Stock(BaseModel):
    quantity: int

class Product(BaseModel):
    id: int
    name: str
    price: float
    short_description: str
    detailed_description: str
    stock: Stock                #hier kommt pydantic ins Spiel

