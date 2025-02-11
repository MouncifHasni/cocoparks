import requests
import json
import time

url= "https://datahub.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/st_park_p/records?limit=10&offset=0&timezone=UTC"

def getParkingData():
    #Récupère les données
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print("Erreur lors de la récupération des données :", e)
        return None
    return data

def getfreeparkingspaces(data):
    parking_minus_200 = [] # ≤ 200 places
    parking_plus_200 = []  # > 200 places

    results = data["results"]
    for element in results:
        libres = element.get("libres")
        total_places = element.get("np_total")
        #supprimer les lignes avec None
        if libres is not None and total_places is not None and total_places > 0:
            percentage = (libres / total_places) * 100
            if total_places <= 200:
                parking_minus_200.append(percentage)
            else:
                parking_plus_200.append(percentage)

    # calcul moyenne des places disponibles
    avg_minus_200 = sum(parking_minus_200) / len(parking_minus_200) if parking_minus_200 else 0
    avg_plus_200 = sum(parking_plus_200) / len(parking_plus_200) if parking_plus_200 else 0

    result = {
        'parking_minus_200': avg_minus_200,
        'parking_plus_200': avg_plus_200
    }
    return result

if __name__ == "__main__":
    while True:
        parking_data = getParkingData()
        if parking_data:
            results  = getfreeparkingspaces(parking_data)
            if results:
                print(f"Pourcentage moyen de places disponibles :")
                print(f"Parkings ≤ 200 places: {results['parking_minus_200']:.2f}%")
                print(f"Parkings > 200 places: {results['parking_plus_200']:.2f}%")
            else:
                print("Impossible d'analyser les données")
        time.sleep(60)