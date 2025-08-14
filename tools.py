# tools.py
import time
import json
from typing import Dict, List, Optional

import requests


DEFAULT_UA = "yourwayally/1.0 (contact: youremail@example.com)"  # Nominatim için nazik UA

class Tools:
    def __init__(self, otm_key: Optional[str], user_agent: str = DEFAULT_UA, rate_delay: float = 0.6):
        self.otm_key = otm_key
        self.user_agent = user_agent
        self.rate_delay = rate_delay  # nazik oran sınırlama

    # ---------- Low-level HTTP helpers ----------
    def http_get(self, url: str, params: Dict, headers: Optional[Dict] = None) -> Dict:
        time.sleep(self.rate_delay)  # basit rate-limit
        h = {"User-Agent": self.user_agent}
        if headers:
            h.update(headers)
        r = requests.get(url, params=params, headers=h, timeout=30)
        r.raise_for_status()
        return r.json()

    # ---------- Weather ----------
    def weather(self, lat: float, lon: float) -> Dict:
        base = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m",
            "current_weather": True,
            "forecast_days": 1,
            "timezone": "auto",
        }
        return self.http_get(base, params)

    # ---------- Places: autosuggest (metne göre) ----------
    def search_places(self, query: str, limit: int = 5) -> List[Dict]:
        if not self.otm_key:
            return []
        base = "https://api.opentripmap.com/0.1/en/places/autosuggest"
        params = {"name": query, "limit": limit, "apikey": self.otm_key}
        data = self.http_get(base, params)
        return data.get("features", [])

    # ---------- Places: radius (yakınımdakiler, lat/lon'a göre) ----------
    def search_radius(
        self,
        lat: float,
        lon: float,
        radius_m: int = 3000,
        kinds: Optional[str] = None,  # örn: "interesting_places,museums"
        limit: int = 20,
        rate: str = "2h"              # sıralama: "2h" (popülerlik) iyi bir varsayılan
    ) -> List[Dict]:
        """
        OpenTripMap /places/radius: belli yarıçap içinde yerleri döndürür.
        kinds: virgülle ayrılmış kategoriler (None ise tümü)
        rate: popülerlik sıralaması; "2h" pratik
        """
        if not self.otm_key:
            return []
        base = "https://api.opentripmap.com/0.1/en/places/radius"
        params = {
            "lat": lat, "lon": lon,
            "radius": radius_m,
            "limit": limit,
            "apikey": self.otm_key,
            "rate": rate
        }
        if kinds:
            params["kinds"] = kinds
        data = self.http_get(base, params)
        return data.get("features", [])

    # ---------- Place details (xid ile detay) ----------
    def place_details(self, xid: str) -> Dict:
        """
        Tekil yer detayı: adres, wikipedia bağlantısı, foto vb.
        """
        if not self.otm_key:
            return {}
        base = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
        params = {"apikey": self.otm_key}
        return self.http_get(base, params)

    # ---------- Geocoding (opsiyonel, Nominatim) ----------
    def geocode(self, text: str) -> Optional[Dict]:
        """
        Adresten/şehir isminden lat/lon üretir (ücretsiz Nominatim).
        Sonuç: {"lat": float, "lon": float} ya da None
        """
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": text, "format": "json", "limit": 1}
        try:
            data = self.http_get(url, params)
            if isinstance(data, list) and data:
                return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
        except Exception:
            return None
        return None
