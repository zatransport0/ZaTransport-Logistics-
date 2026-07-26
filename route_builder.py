from models import Route

from route_scoring import score_order


class RouteBuilder:

    MAX_STOPS = 5

    MAX_PALLETS = 53

    def __init__(self, engine):

        self.engine = engine

    def build(self, order, candidates):

        route = Route()
        
        route = builder.build(order)
        
        trailers = trailer_manager.available_trailers(route.orders[0].temperature
    )

    if trailers:

        trailer = trailers[0]

        trailer_manager.assign_trailer(route, trailer)

        dock_manager.assign_door(trailer)

        route.orders.append(order)

        route.zone = order.zone

        route.total_pallets = order.pallets

        current = order

        while len(route.orders) < self.MAX_STOPS:

            best = None

            best_score = -999

            for order in candidates:

                if order in route.orders:
                    continue

                score = score_order(current, order, route)

                if score > best_score:

                    best = order

                    best_score = score

            if best is None:
                break

            route.orders.append(best)

            route.total_pallets += best.pallets

            current = best

        return route