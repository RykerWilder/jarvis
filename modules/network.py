import urllib.request
import socket
import requests
import speedtest
import webbrowser
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

class Network: 
    def check_connection(self, input_text=""):
        """
        Testing internet connection
        """
        try:
            urllib.request.urlopen("http://www.google.com", timeout=5)
            return True
        except (urllib.error.URLError, socket.timeout):
            return "I don't have access to the internet."

    def execute_speedtest(self, input_text=""):
        if self.check_connection():
            st = speedtest.Speedtest()
            
            # download
            download_speed = st.download() / 1_000_000  
            
            # upload
            upload_speed = st.upload() / 1_000_000 

            result = f"Speed test completed. Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps"
            return result
        else:
            return "I don't have access to the internet."

    def riproduci_musica(self, canzone, artista):
        """
        Riproduce automaticamente una canzone su YouTube cercando per nome canzone e artista.
        
        Args:
            canzone: Il nome della canzone da riprodurre
            artista: Il nome dell'artista
            
        Returns:
            Messaggio di conferma
        """
        try:
            # Crea la query di ricerca
            query = f"{canzone} {artista}"
            query_encoded = quote_plus(query)
            
            # URL di ricerca YouTube
            search_url = f"https://www.youtube.com/results?search_query={query_encoded}"
            
            # Fai una richiesta alla pagina di ricerca
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(search_url, headers=headers)
            
            # Cerca il primo video ID nella pagina
            if 'watch?v=' in response.text:
                # Estrai il primo video ID
                start = response.text.find('watch?v=') + 8
                video_id = response.text[start:start+11]
                
                # Costruisci l'URL del video
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Apre il video direttamente
                webbrowser.open(video_url)
                
                return f"Riproduzione di: {canzone} - {artista}"
            else:
                return f"Nessun risultato trovato per: {canzone} - {artista}"
        
        except Exception as e:
            return f"Errore durante la riproduzione: {str(e)}"

if __name__ == "__main__":
    # Test della funzione
    net = Network()
    risultato = net.riproduci_musica("Capo Status", "Emis Killa")
    print(risultato)