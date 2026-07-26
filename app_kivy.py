#Pydroid run kivy

from __future__ import annotations

from functools import partial
from typing import Iterable

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class WrappedLabel(Label):
    """
    Label that automatically wraps text to its available width.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.halign = kwargs.get("halign", "left")
        self.valign = kwargs.get("valign", "middle")

        self.bind(
            width=self.update_text_size
        )

    def update_text_size(self, *_):
        self.text_size = (
            self.width - dp(12),
            None
        )

        self.texture_update()

        if self.texture_size:
            self.height = self.texture_size[1] + dp(14)


class OrderCard(BoxLayout):
    """
    One mobile-friendly order card.
    """

    def __init__(
        self,
        order,
        route_callback=None,
        details_callback=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.order = order

        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(350)
        self.spacing = dp(8)
        self.padding = dp(14)

        order_number = self.safe(
            getattr(order, "order_number", "")
        )

        shipping_company = self.safe(
            getattr(order, "shipping_company", "")
        )

        origin = self.safe(
            getattr(order, "origin", "")
        )

        customer = self.safe(
            getattr(order, "customer", "")
        )

        destination = self.safe(
            getattr(order, "destination", "")
        )

        product = self.safe(
            getattr(order, "product", "")
        )

        pallets = self.safe(
            getattr(order, "pallets", "")
        )

        temperature = self.safe(
            getattr(order, "temperature", "")
        )

        title = WrappedLabel(
            text=f"[b]Order #{order_number}[/b]",
            markup=True,
            font_size="20sp",
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title)

        route_text = WrappedLabel(
            text=(
                f"[b]{origin}[/b]\n"
                f"        ↓\n"
                f"[b]{destination}[/b]"
            ),
            markup=True,
            font_size="18sp",
            halign="center",
            size_hint_y=None,
            height=dp(85)
        )
        self.add_widget(route_text)

        information = WrappedLabel(
            text=(
                f"[b]Shipper:[/b] {shipping_company}\n"
                f"[b]Customer:[/b] {customer}\n"
                f"[b]Product:[/b] {product}\n"
                f"[b]Pallets:[/b] {pallets}\n"
                f"[b]Temperature:[/b] {temperature}"
            ),
            markup=True,
            font_size="15sp",
            size_hint_y=None,
            height=dp(125)
        )
        self.add_widget(information)

        button_row = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        details_button = Button(
            text="View Details"
        )

        route_button = Button(
            text="Build Route"
        )

        if details_callback is not None:
            details_button.bind(
                on_release=partial(
                    details_callback,
                    order
                )
            )

        if route_callback is not None:
            route_button.bind(
                on_release=partial(
                    route_callback,
                    order
                )
            )

        button_row.add_widget(details_button)
        button_row.add_widget(route_button)

        self.add_widget(button_row)

    @staticmethod
    def safe(value):
        if value is None:
            return ""

        return str(value)


class SwipeScreenManager(ScreenManager):
    """
    Lets the user swipe left and right between screens.
    """

    swipe_distance = NumericProperty(dp(70))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.touch_start_x = None
        self.touch_start_y = None

    def on_touch_down(self, touch):
        self.touch_start_x = touch.x
        self.touch_start_y = touch.y

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if (
            self.touch_start_x is None
            or self.touch_start_y is None
        ):
            return super().on_touch_up(touch)

        horizontal_distance = (
            touch.x - self.touch_start_x
        )

        vertical_distance = (
            touch.y - self.touch_start_y
        )

        # Only treat the gesture as a page swipe when it
        # is mostly horizontal.
        is_horizontal_swipe = (
            abs(horizontal_distance)
            > self.swipe_distance
            and abs(horizontal_distance)
            > abs(vertical_distance) * 1.3
        )

        if is_horizontal_swipe:
            if horizontal_distance < 0:
                self.show_next_screen()
            else:
                self.show_previous_screen()

            self.touch_start_x = None
            self.touch_start_y = None
            return True

        self.touch_start_x = None
        self.touch_start_y = None

        return super().on_touch_up(touch)

    def show_next_screen(self):
        screens = self.screen_names

        current_index = screens.index(
            self.current
        )

        if current_index < len(screens) - 1:
            self.transition.direction = "left"

            self.current = screens[
                current_index + 1
            ]

    def show_previous_screen(self):
        screens = self.screen_names

        current_index = screens.index(
            self.current
        )

        if current_index > 0:
            self.transition.direction = "right"

            self.current = screens[
                current_index - 1
            ]


class MobileHeader(BoxLayout):
    """
    Header displayed at the top of every page.
    """

    def __init__(self, title, subtitle="", **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(82)
        self.padding = (
            dp(12),
            dp(8)
        )

        title_label = Label(
            text=f"[b]{title}[/b]",
            markup=True,
            font_size="24sp",
            halign="left",
            valign="middle"
        )

        title_label.bind(
            size=title_label.setter("text_size")
        )

        subtitle_label = Label(
            text=subtitle,
            font_size="13sp",
            halign="left",
            valign="middle"
        )

        subtitle_label.bind(
            size=subtitle_label.setter(
                "text_size"
            )
        )

        self.add_widget(title_label)
        self.add_widget(subtitle_label)


class BottomNavigation(BoxLayout):
    """
    Navigation buttons shown along the bottom.
    """

    def __init__(
        self,
        screen_manager,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.screen_manager = screen_manager

        self.orientation = "horizontal"
        self.spacing = dp(4)
        self.padding = dp(4)
        self.size_hint_y = None
        self.height = dp(62)

        buttons = [
            ("Home", "home"),
            ("Orders", "orders"),
            ("Routes", "routes"),
            ("Warehouse", "warehouse")
        ]

        for button_text, screen_name in buttons:
            button = Button(
                text=button_text,
                font_size="13sp"
            )

            button.bind(
                on_release=partial(
                    self.open_screen,
                    screen_name
                )
            )

            self.add_widget(button)

    def open_screen(
        self,
        screen_name,
        *_args
    ):
        current_index = (
            self.screen_manager.screen_names.index(
                self.screen_manager.current
            )
        )

        new_index = (
            self.screen_manager.screen_names.index(
                screen_name
            )
        )

        if new_index > current_index:
            self.screen_manager.transition.direction = (
                "left"
            )
        else:
            self.screen_manager.transition.direction = (
                "right"
            )

        self.screen_manager.current = screen_name


class HomeScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)

        self.engine = engine

        main_layout = BoxLayout(
            orientation="vertical"
        )

        main_layout.add_widget(
            MobileHeader(
                "ZaTransport",
                "Logistics and Dispatch Center"
            )
        )

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(12),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter(
                "height"
            )
        )

        welcome_card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(180),
            padding=dp(16),
            spacing=dp(8)
        )

        welcome_card.add_widget(
            WrappedLabel(
                text=(
                    "[b]Welcome to ZaTransport[/b]\n\n"
                    "View freight orders, build routes, "
                    "and manage warehouse operations."
                ),
                markup=True,
                font_size="18sp",
                halign="center"
            )
        )

        content.add_widget(welcome_card)

        quick_actions = [
            (
                "View Orders",
                "Browse freight by delivery zone"
            ),
            (
                "Build Route",
                "Create a multi-stop dispatch"
            ),
            (
                "Warehouse",
                "View warehouse inventory and docks"
            )
        ]

        for title, description in quick_actions:
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(125),
                padding=dp(14)
            )

            card.add_widget(
                WrappedLabel(
                    text=(
                        f"[b]{title}[/b]\n"
                        f"{description}"
                    ),
                    markup=True,
                    font_size="17sp"
                )
            )

            content.add_widget(card)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)


class OrdersScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)

        self.engine = engine
        self.selected_zone = 1

        self.main_layout = BoxLayout(
            orientation="vertical"
        )

        self.header = MobileHeader(
            "Orders",
            "Swipe vertically to browse orders"
        )

        self.main_layout.add_widget(
            self.header
        )

        zone_buttons = BoxLayout(
            orientation="horizontal",
            spacing=dp(5),
            padding=dp(5),
            size_hint_y=None,
            height=dp(55)
        )

        for zone_number in range(1, 5):
            button = Button(
                text=f"Zone {zone_number}",
                font_size="13sp"
            )

            button.bind(
                on_release=partial(
                    self.load_zone,
                    zone_number
                )
            )

            zone_buttons.add_widget(button)

        self.main_layout.add_widget(
            zone_buttons
        )

        self.scroll_view = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(6),
            scroll_type=[
                "bars",
                "content"
            ]
        )

        self.card_container = GridLayout(
            cols=1,
            spacing=dp(12),
            padding=dp(10),
            size_hint_y=None
        )

        self.card_container.bind(
            minimum_height=self.card_container.setter(
                "height"
            )
        )

        self.scroll_view.add_widget(
            self.card_container
        )

        self.main_layout.add_widget(
            self.scroll_view
        )

        self.add_widget(
            self.main_layout
        )

        self.load_zone(1)

    def load_zone(
        self,
        zone_number,
        *_args
    ):
        self.selected_zone = zone_number

        self.card_container.clear_widgets()

        try:
            orders = self.engine.get_zone(
                zone_number
            )
        except Exception as error:
            self.show_error(
                "Zone Error",
                str(error)
            )
            return

        orders = list(orders)

        self.header.children[0].text = (
            f"Zone {zone_number} • "
            f"{len(orders)} Orders"
        )

        if not orders:
            self.card_container.add_widget(
                WrappedLabel(
                    text="No orders found.",
                    font_size="18sp",
                    halign="center",
                    size_hint_y=None,
                    height=dp(100)
                )
            )
            return

        for order in orders:
            card = OrderCard(
                order=order,
                details_callback=self.open_details,
                route_callback=self.build_route
            )

            self.card_container.add_widget(card)

        # Return to the top whenever a new zone is selected.
        self.scroll_view.scroll_y = 1

    def open_details(
        self,
        order,
        *_args
    ):
        order_number = getattr(
            order,
            "order_number",
            ""
        )

        notes = getattr(
            order,
            "notes",
            ""
        )

        warehouse_location = getattr(
            order,
            "warehouse_location",
            ""
        )

        message = (
            f"Order: {order_number}\n\n"
            f"Shipper: "
            f"{getattr(order, 'shipping_company', '')}\n"
            f"Origin: "
            f"{getattr(order, 'origin', '')}\n"
            f"Customer: "
            f"{getattr(order, 'customer', '')}\n"
            f"Destination: "
            f"{getattr(order, 'destination', '')}\n"
            f"Product: "
            f"{getattr(order, 'product', '')}\n"
            f"Pallets: "
            f"{getattr(order, 'pallets', '')}\n"
            f"Temperature: "
            f"{getattr(order, 'temperature', '')}\n"
            f"Warehouse: {warehouse_location}\n"
            f"Notes: {notes}"
        )

        self.show_popup(
            f"Order #{order_number}",
            message
        )

    def build_route(
        self,
        order,
        *_args
    ):
        order_number = getattr(
            order,
            "order_number",
            ""
        )

        try:
            route = self.engine.create_route(
                str(order_number)
            )
        except Exception as error:
            self.show_error(
                "Route Error",
                str(error)
            )
            return

        app = App.get_running_app()

        routes_screen = (
            app.root.screen_manager.get_screen(
                "routes"
            )
        )

        routes_screen.display_route(route)

        app.root.screen_manager.transition.direction = (
            "left"
        )

        app.root.screen_manager.current = "routes"

    def show_error(
        self,
        title,
        message
    ):
        self.show_popup(
            title,
            f"Error:\n{message}"
        )

    @staticmethod
    def show_popup(
        title,
        message
    ):
        popup_layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        scroll = ScrollView()

        label = WrappedLabel(
            text=message,
            font_size="15sp",
            size_hint_y=None
        )

        scroll.add_widget(label)
        popup_layout.add_widget(scroll)

        close_button = Button(
            text="Close",
            size_hint_y=None,
            height=dp(48)
        )

        popup_layout.add_widget(
            close_button
        )

        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.92, 0.82),
            auto_dismiss=False
        )

        close_button.bind(
            on_release=lambda *_:
            popup.dismiss()
        )

        popup.open()


class RoutesScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)

        self.engine = engine

        main_layout = BoxLayout(
            orientation="vertical"
        )

        main_layout.add_widget(
            MobileHeader(
                "Routes",
                "Build or review a dispatch"
            )
        )

        controls = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(6),
            padding=dp(6)
        )

        self.order_input = TextInput(
            hint_text="Starting order number",
            multiline=False,
            font_size="16sp"
        )

        build_button = Button(
            text="Build",
            size_hint_x=None,
            width=dp(100)
        )

        build_button.bind(
            on_release=self.build_manual_route
        )

        controls.add_widget(
            self.order_input
        )
        controls.add_widget(
            build_button
        )

        main_layout.add_widget(
            controls
        )

        self.scroll_view = ScrollView(
            do_scroll_x=False
        )

        self.route_container = GridLayout(
            cols=1,
            spacing=dp(12),
            padding=dp(10),
            size_hint_y=None
        )

        self.route_container.bind(
            minimum_height=self.route_container.setter(
                "height"
            )
        )

        self.scroll_view.add_widget(
            self.route_container
        )

        main_layout.add_widget(
            self.scroll_view
        )

        self.add_widget(main_layout)

        self.show_empty_route()

    def show_empty_route(self):
        self.route_container.clear_widgets()

        self.route_container.add_widget(
            WrappedLabel(
                text=(
                    "Enter an order number or select "
                    "Build Route from an order card."
                ),
                font_size="17sp",
                halign="center",
                size_hint_y=None,
                height=dp(140)
            )
        )

    def build_manual_route(self, *_args):
        order_number = self.order_input.text.strip()

        if not order_number:
            return

        try:
            route = self.engine.create_route(
                order_number
            )
        except Exception as error:
            OrdersScreen.show_popup(
                "Route Error",
                str(error)
            )
            return

        self.display_route(route)

    def display_route(self, route):
        self.route_container.clear_widgets()

        if route is None:
            self.show_empty_route()
            return

        orders = list(
            getattr(route, "orders", [])
        )

        start_location = getattr(
            route,
            "start",
            "ZaTransport"
        )

        total_pallets = getattr(
            route,
            "total_pallets",
            sum(
                int(
                    getattr(order, "pallets", 0)
                    or 0
                )
                for order in orders
            )
        )

        summary_card = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            size_hint_y=None,
            height=dp(150)
        )

        summary_card.add_widget(
            WrappedLabel(
                text=(
                    "[b]Current Dispatch[/b]\n\n"
                    f"Starting Location: {start_location}\n"
                    f"Stops: {len(orders)}\n"
                    f"Total Pallets: {total_pallets}"
                ),
                markup=True,
                font_size="17sp"
            )
        )

        self.route_container.add_widget(
            summary_card
        )

        for stop_number, order in enumerate(
            orders,
            start=1
        ):
            stop_card = BoxLayout(
                orientation="vertical",
                padding=dp(14),
                size_hint_y=None,
                height=dp(220)
            )

            stop_card.add_widget(
                WrappedLabel(
                    text=(
                        f"[b]Stop {stop_number}[/b]\n\n"
                        f"{getattr(order, 'origin', '')}\n"
                        "↓\n"
                        f"{getattr(order, 'destination', '')}\n\n"
                        f"Customer: "
                        f"{getattr(order, 'customer', '')}\n"
                        f"Product: "
                        f"{getattr(order, 'product', '')}\n"
                        f"Pallets: "
                        f"{getattr(order, 'pallets', '')}"
                    ),
                    markup=True,
                    font_size="16sp",
                    halign="center"
                )
            )

            self.route_container.add_widget(
                stop_card
            )

        self.scroll_view.scroll_y = 1


class WarehouseScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)

        self.engine = engine

        main_layout = BoxLayout(
            orientation="vertical"
        )

        main_layout.add_widget(
            MobileHeader(
                "Warehouse",
                "Swipe vertically through warehouse orders"
            )
        )

        refresh_button = Button(
            text="Refresh Warehouse",
            size_hint_y=None,
            height=dp(50)
        )

        refresh_button.bind(
            on_release=self.load_warehouse
        )

        main_layout.add_widget(
            refresh_button
        )

        self.scroll_view = ScrollView()

        self.card_container = GridLayout(
            cols=1,
            spacing=dp(12),
            padding=dp(10),
            size_hint_y=None
        )

        self.card_container.bind(
            minimum_height=self.card_container.setter(
                "height"
            )
        )

        self.scroll_view.add_widget(
            self.card_container
        )

        main_layout.add_widget(
            self.scroll_view
        )

        self.add_widget(main_layout)

        self.load_warehouse()

    def load_warehouse(self, *_args):
        self.card_container.clear_widgets()

        warehouse = getattr(
            self.engine,
            "warehouse",
            None
        )

        if warehouse is None:
            self.card_container.add_widget(
                WrappedLabel(
                    text=(
                        "Warehouse data is not "
                        "connected to the engine."
                    ),
                    font_size="17sp",
                    halign="center",
                    size_hint_y=None,
                    height=dp(120)
                )
            )
            return

        try:
            orders = list(
                warehouse.get_orders()
            )
        except Exception as error:
            self.card_container.add_widget(
                WrappedLabel(
                    text=f"Warehouse error:\n{error}",
                    font_size="16sp",
                    halign="center",
                    size_hint_y=None,
                    height=dp(130)
                )
            )
            return

        for order in orders:
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(210),
                padding=dp(14)
            )

            card.add_widget(
                WrappedLabel(
                    text=(
                        f"[b]Order "
                        f"#{getattr(order, 'order_number', '')}"
                        "[/b]\n\n"
                        f"Location: "
                        f"{getattr(order, 'location', '')}\n"
                        f"Trailer: "
                        f"{getattr(order, 'trailer', '')}\n"
                        f"Product: "
                        f"{getattr(order, 'product', '')}\n"
                        f"Pallets: "
                        f"{getattr(order, 'pallets', '')}\n"
                        f"Status: "
                        f"{getattr(order, 'status', '')}"
                    ),
                    markup=True,
                    font_size="16sp"
                )
            )

            self.card_container.add_widget(
                card
            )

        self.scroll_view.scroll_y = 1


class ZaTransportMobileRoot(BoxLayout):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)

        self.engine = engine
        self.orientation = "vertical"

        self.screen_manager = SwipeScreenManager(
            transition=SlideTransition(
                duration=0.18
            )
        )

        self.screen_manager.add_widget(
            HomeScreen(
                name="home",
                engine=engine
            )
        )

        self.screen_manager.add_widget(
            OrdersScreen(
                name="orders",
                engine=engine
            )
        )

        self.screen_manager.add_widget(
            RoutesScreen(
                name="routes",
                engine=engine
            )
        )

        self.screen_manager.add_widget(
            WarehouseScreen(
                name="warehouse",
                engine=engine
            )
        )

        self.add_widget(
            self.screen_manager
        )

        self.add_widget(
            BottomNavigation(
                self.screen_manager
            )
        )


class ZaTransportApp(App):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)

        self.engine = engine

    def build(self):
        self.title = (
            "ZaTransport Logistics Engine"
        )

        return ZaTransportMobileRoot(
            self.engine
        )