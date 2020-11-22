import json
from requests import get, head, post, delete
from enum import Enum, auto


class CloseApproachBodies(Enum):
    """
    Supported Close Approach Bodies
    """
    Merc = auto()  # Mercury
    Venus = auto()  # Venus
    Earth = auto()  # Earth
    Mars = auto()  # Mars
    Juptr = auto()  # Jupiter
    Satrn = auto()  # Saturn
    Urnus = auto()  # Uranus
    Neptn = auto()  # Neptune
    Pluto = auto()  # Pluto
    Moon = auto()  # Moon
    ALL = auto()  # ALL


class SDBDOrbitClass(Enum):
    """
    Supported SBDB Orbit Class Values
    """
    IEO = auto()  # Atira An asteroid orbit contained entirely within the orbit of the Earth (Q < 0.983 AU). # Also known as an Interior Earth Object.
    ATE = auto()  # Aten Near-Earth asteroid orbits similar to that of 2062 Aten (a < 1.0 AU; Q > 0.983 AU).
    APO = auto()  # Apollo Near-Earth asteroid orbits which cross the Earth’s orbit similar to that of 1862 Apollo (a > 1.0 AU; q < 1.017 AU).
    AMO = auto()  # Amor Near-Earth asteroid orbits similar to that of 1221 Amor (1.017 AU < q < 1.3 AU).
    MCA = auto()  # Mars-crossing Asteroid Asteroids that cross the orbit of Mars constrained by (1.3 AU < q < 1.666 AU; a < 3.2 AU).
    IMB = auto()  # Inner Main-belt Asteroid Asteroids with orbital elements constrained by (a < 2.0 AU; q > 1.666 AU).
    MBA = auto()  # Main-belt Asteroid Asteroids with orbital elements constrained by (2.0 AU < a < 3.2 AU; q > 1.666 AU).
    OMB = auto()  # Outer Main-belt Asteroid Asteroids with orbital elements constrained by (3.2 AU < a < 4.6 AU).
    TJN = auto()  # Jupiter Trojan Asteroids trapped in Jupiter’s L4/L5 Lagrange points (4.6 AU < a < 5.5 AU; e < 0.3).
    CEN = auto()  # Centaur Objects with orbits between Jupiter and Neptune (5.5 AU < a < 30.1 AU).
    TNO = auto()  # TransNeptunian Object Objects with orbits outside Neptune (a > 30.1 AU).
    PAA = auto()  # Parabolic Asteroid Asteroids on parabolic orbits (e = 1.0).
    HYA = auto()  # Hyperbolic Asteroid Asteroids on hyperbolic orbits (e > 1.0).
    HYP = auto()  # Hyperbolic Comet Comets on hyperbolic orbits (e > 1.0).
    PAR = auto()  # Parabolic Comet Comets on parabolic orbits (e = 1.0).
    COM = auto()  # Comet Comet orbit not matching any defined orbit class.
    JFC = auto()  # Jupiter-family Comet* Jupiter-family comet, classical definition (P < 20 y).
    HTC = auto()  # Halley-type Comet* Halley-type comet, classical definition (20 y < P < 200 y).
    ETc = auto()  # Encke-type Comet Encke-type comet, as defined by Levison and Duncan (Tj > 3; a < aJ).
    CTc = auto()  # Chiron-type Comet Chiron-type comet, as defined by Levison and Duncan (Tj > 3; a > aJ).
    JFc = auto()  # Jupiter-family Comet Jupiter-family comet, as defined by Levison and Duncan (2 < Tj < 3).


class Response:
    """
    Encapsulation http status code and http content as json
    """

    def __init__(self, api_response):
        self.code = api_response.status_code
        self.raw_content = api_response.content.decode()
        self.__content_decoded = '{}' if self.raw_content == '' else self.raw_content
        self.json_content = json.loads(self.__content_decoded)

    def get_value_for_key(self, key):
        if type(self.json_content) is dict:
            if key in self.json_content.keys():
                return self.json_content[key]

    def get_count(self):
        return int(self.get_value_for_key('count'))

    def get_fields(self):
        return self.get_value_for_key('fields')

    def get_data(self):
        return self.get_value_for_key('data')


class APIClient:
    """
    Encapsulating URL, API & Endpoints into client
    """

    def __init__(self, endpoint="cad.api"):
        """
        :param endpoint: rest endpoint
        """
        self.endpoint = endpoint
        self._validate_endpoint()
        self.base_url = "https://ssd-api.jpl.nasa.gov/"
        self.endpoint_url = self.base_url + endpoint

    def _validate_endpoint(self):
        # check endpoint is supported
        valid_endpoints = ["cad.api"]
        if self.endpoint not in valid_endpoints:
            raise ValueError(f'Check your endpoint, {self.endpoint} does not seems to be part of utils')

    def head(self, params=None):
        """
        a http call to check stats of endpoint
        """
        res = head(self.endpoint_url, params=params)
        return Response(res)

    def get(self, params=None):
        """
        a http call to retrieve data for  endpoint
        """
        res = get(self.endpoint_url, params=params)
        return Response(res)

    def post(self, data=None, params=None):
        """
        a http call to create resource on endpoint
        """
        res = post(self.endpoint_url, data=data, params=params)
        return Response(res)

    def delete(self, params=None):
        """
        a http call to delete resource on endpoint
        """
        res = delete(self.endpoint_url, params=params)
        return Response(res)

