import requests
import os
from dotenv import load_dotenv


class OSRMManager:
    def __init__(self, base_url: str = os.load_dotenv("API_URL")):
        self.base_url = base_url

    def get_average_speed(self, start_coords: tuple[float, float], end_coords: tuple[float, float]) -> float:
        """
        
        : start_coords: Coordenadas de inicio (latitud, longitud)
        : end_coords: Coordenadas de fin (latitud, longitud)
        """
        url = f"{self.base_url}/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=false"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            route = data['routes'][0]
            
            total_distance = route['legs'][0]['distance']
            total_duration = route['legs'][0]['duration']
            
            # Calcula la velocidad promedio
            average_speed = total_distance / total_duration  # La velocidad se obtiene en m/s
            
            return average_speed
        else:
            raise Exception(f"Error in OSRM API request for average speed: {response.status_code}")

    def get_num_maneuvers(self, start_coords: tuple[float, float], end_coords: tuple[float, float]) -> int:
        """
        
        : start_coords: Coordenadas de inicio (latitud, longitud)
        : end_coords: Coordenadas de fin (latitud, longitud)
        """
        url = f"{self.base_url}/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=false&steps=true"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            route = data['routes'][0]
            steps = route['legs'][0]['steps']
            
            # Número de maniobras
            num_maneuvers = len(steps)
            
            return num_maneuvers
        else:
            raise Exception(f"Error in OSRM API request for number of maneuvers: {response.status_code}")


def main():
    start = {
        "x": -118.289,  # Cerca de la Universidad del Sur de California (USC)
        "y": 34.021
    }

    end = {
        "x": -118.281,  # Cerca del Museo de Historia Natural del Condado de Los Ángeles
        "y": 34.018
    }

    osrm_manager = OSRMManager()

    try:
        average_speed = osrm_manager.get_average_speed(
            (start['y'], start['x']),
            (end['y'], end['x'])
        )
        num_maneuvers = osrm_manager.get_num_maneuvers(
            (start['y'], start['x']),
            (end['y'], end['x'])
        )

        print(f"Average Speed: {average_speed:.2f} m/s")
        print(f"Number of Maneuvers: {num_maneuvers}")
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()