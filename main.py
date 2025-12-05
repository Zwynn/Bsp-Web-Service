from fastapi import FastAPI, HTTPException
from pathlib import Path
from typing import List             #Damit FastAPI automatisch Doku erstellt
import json
from module import Product, ProductCreate



DATA_FILE = Path(__file__).with_name("products.json")

app = FastAPI(
    title="Beispiel-Web-Service",
    description="Ein einfaches Beispiel für einen Web-Service mit FastAPI.",
    version="1.0.0",    
)

def load_products():
    """
    Lädt die Produktdaten aus der JSON-Datei.
    """
    if not DATA_FILE.exists():
        # Falls die Datei nicht existiert, wird eine leere Liste erstellt
        with open(DATA_FILE, encoding="utf-8", mode="w") as file:
            json.dump([], file) 
        return []

    with open(DATA_FILE, mode="r", encoding="utf-8") as file:
        return json.load(file)

def save_products(products):
    """
    Speichert die Produktdaten in der JSON-Datei.
    """
    with open(DATA_FILE, encoding="utf-8", mode="w") as file:
        json.dump(products, file, indent=2, ensure_ascii=False)


@app.get("/api/products", response_model=List[Product])
def get_products():
    """
    API-Endpunkt zum Abrufen der Produktliste.
    """
    products=load_products()
    return [Product(**product) for product in products]     #Umwandlung der dicts in Product-Objekte

@app.get("/api/products/{product_id}", response_model=Product)   #Damit man auch per ID filtern kann
def get_product(product_id: int):
    """
    API-Endpunkt zum Abrufen eines einzelnen Produkts anhand der ID.
    """
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            return Product(**product)
    raise HTTPException(status_code=404, detail="Product not found")

def next_id(products):
    """
    Hilft zur Bestimmung der nächsten freien ID.
    """
    products=load_products()                #Vermutlich überflüssig
    id_counter=0
    if not products:
        id_counter = 1
        return id_counter, {"Info! vergebene ID": id_counter}    
    id_counter=max(product["id"] for product in products) +1
    return id_counter, {"Info! Vergebene ID": id_counter}

@app.post("/api/products/create", response_model=Product, status_code=201)     #standardcode für etwas Neues anlegen
def create_product(product: ProductCreate):
    """
    API-Endpunkt zum anheften eines neuen Produkts.
    Die ID wird automatisch vergeben.
    Daten kommen im JSON-Format im Request-Body.
    """
    products = load_products()
    new_product = product.dict() #JSON kennt kein Pydantic, also in dict umwandeln 
                                 #ältere Pydantic Version, deshalb kein model_dump()
                                        
    new_product["id"] = next_id(products)
    products.append(new_product)
    save_products(products)
    return Product(**new_product), 

if __name__ == "__main__":
    print(load_products()) 