from fastapi import FastAPI
from pathlib import Path
from typing import List             #Damit FastAPI automatisch Doku erstellt
import json
from module import Stock, Product



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


if __name__ == "__main__":
    print (load_products())