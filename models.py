from dataclasses import dataclass

@dataclass
class Order:
    zone: int
    shipping_company: str
    origin: str
    order_number: str
    product: str
    pallets: int
    customer: str
    destination: str
    warehouse_location: str
    temperature: str
    notes: str
    status: str = "Available"
    
@dataclass
class Trailer:

    trailer_number: str
    trailer_type: str
    owner: str
    status: str
    temperature: str
    current_door: int = 0
    current_order: str = ""
    location: str = ""
    notes: str = ""
    
    
from dataclasses import dataclass, field

@dataclass
class Route:

    trip_name: str = ""

    zone: int = 0

    orders: list = field(default_factory=list)

    total_pallets: int = 0

    total_stops: int = 0

    total_miles: int = 0

    trailer_type: str = ""

    temperature: str = ""

    export_ready: bool = False
    
@dataclass
class WarehouseSlot:

    location: str          # e.g. "1-Frozen"

    position: int          # Position within that location

    order: Order | None

    trailer: str = ""

    trip: str = ""

    occupied: bool = False    
    
    
class Route:

    def __init__(self):

        self.orders = []

        self.total_pallets = 0

        self.temperature = None

        self.zone = None

        self.start = "ZaTransport Aurora"

        self.stops = []

    def add_order(self, order):

        self.orders.append(order)

        self.total_pallets += order.pallets

        self.stops.append(order.destination)
        
    