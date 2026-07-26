import customtkinter as ctk
from tkinter import simpledialog


class MainMenu:

    def __init__(self, root, engine):
    
        
            self.root = root
            self.engine = engine

            # Left navigation frame
            self.menu_frame = ctk.CTkFrame(self.root, width=260)
            self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)

            # Title
            title = ctk.CTkLabel(
                self.menu_frame,
                text="ZaTransport\nDispatch Center",
                font=("Arial", 22, "bold")
            )
            title.pack(pady=20)

            # Main content area
            self.content = ctk.CTkFrame(self.root)
            
           
            
            

            # Buttons
            self.create_buttons()
            
            self.content = ctk.CTkFrame(self.root)
            
            self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)
            
    def create_buttons(self):

            self.orders_btn = ctk.CTkButton(
                self.menu_frame,
                text="📦 View Orders",
                width=220,
                height=45,
                command=self.view_orders
            )
            self.orders_btn.pack(pady=5)
            
            self.order_entry = ctk.CTkEntry(
                self.content,
                width=250,
                placeholder_text="Enter Order Number"
            )

          
            
            self.route_btn = ctk.CTkButton(
                self.menu_frame,
                text="🚛 Route Planner",
                width=220,
                height=45,
                command=self.show_route_planner
            )
            self.route_btn.pack(pady=5)

            self.warehouse_btn = ctk.CTkButton(
                self.menu_frame,
                text="🏢 Warehouse",
                width=220,
                height=45,
                command=self.warehouse
            )
            self.warehouse_btn.pack(pady=5)

            self.drivers_btn = ctk.CTkButton(
                self.menu_frame,
                text="👤 Drivers",
                width=220,
                height=45,
                command=self.drivers
            )
            self.drivers_btn.pack(pady=5)

            self.settings_btn = ctk.CTkButton(
                self.menu_frame,
                text="⚙ Settings",
                width=220,
                height=45,
                command=self.settings
            )
            self.settings_btn.pack(pady=5)

            self.exit_btn = ctk.CTkButton(
                self.menu_frame,
                text="Exit",
                width=220,
                height=45,
                fg_color="firebrick",
                command=self.root.destroy
            )
            self.exit_btn.pack(side="bottom", pady=20)  
            
            search_order_btn = ctk.CTkButton(
                self.menu_frame,
                text="Search Order Number",
                width=220,
                height=45,
                command=self.search_orders
            )
            search_order_btn.pack(pady=5, padx=10, fill="x")


            search_customer_btn = ctk.CTkButton(
                self.menu_frame,
                text="Search Customer",
                 width=220,
                height=45,
                command=self.search_customer
            )
            search_customer_btn.pack(pady=5, padx=10, fill="x")


            search_destination_btn = ctk.CTkButton(
                self.menu_frame,
                text="Search Destination",
                 width=220,
                height=45,
                command=self.search_destination
            )
            search_destination_btn.pack(pady=5, padx=10, fill="x")
            
    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.output = None
        self.order_entry = None

        self.content.update_idletasks()          
        
    def ask(self, message):

        return simpledialog.askstring(
            "ZaTransport Logistics",
            message
        )
 
    
    def view_orders(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Orders by Zone",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=15)

        zone_frame = ctk.CTkFrame(self.content)
        zone_frame.pack(pady=10)

        ctk.CTkButton(
            zone_frame,
            text="Zone 1:\n West, West Coast, Southwest",
            width=120,
            command=lambda: self.show_zone(1)
        ).grid(row=0,column=0,padx=5)

        ctk.CTkButton(
            zone_frame,
            text="Zone 2:\n Northwest",
            width=120,
            command=lambda: self.show_zone(2)
        ).grid(row=0,column=1,padx=5)

        ctk.CTkButton(
            zone_frame,
            text="Zone 3:\n Midwest",
            width=120,
            command=lambda: self.show_zone(3)
        ).grid(row=0,column=2,padx=5)

        ctk.CTkButton(
            zone_frame,
            text="Zone 4:\n Ohio Valley, South",
            width=120,
            command=lambda: self.show_zone(4)
        ).grid(row=0,column=3,padx=5)

        self.output = ctk.CTkTextbox(
            self.content,
            width=1000,
            height=650,
            font=("Consolas",12)
        )

        self.output.pack(fill="both",expand=True,padx=10,pady=10)
        
    def search_orders(self):

        order_number = self.ask(
            "Enter Order Number"
        )

        if not order_number:
            return

        order = self.engine.find_order(
            order_number
        )

        if order is None:

            self.display_orders(
                [],
                "Order Search"
            )

            return

        self.display_orders(
            [order],
            "Order Search"
        )
            
    def search_customer(self):

        customer = self.ask(
            "Enter Customer"
        )

        if not customer:
            return

        orders = self.engine.find_customer(
            customer
        )

        self.display_orders(
            orders,
            f"Customer: {customer}"
        )

    def search_destination(self):

        destination = self.ask(
            "Enter Destination"
        )

        if not destination:
            return

        orders = self.engine.find_destination(
            destination
        )

        self.display_orders(
            orders,
            f"Destination: {destination}"
        )
    
    def show_zone(self, zone):

        self.output.delete("1.0","end")

        orders = self.engine.get_zone(zone)

        self.output.insert(
            "end",
            f"ZONE {zone}\n\n"
        )

        self.output.insert(
            "end",
            f"{'Order #':<12}"
            f"{'Shipper':<20}"
            f"{'Origin':<20}"
            f"{'Customer':<20}"
            f"{'Destination':<20}"
            f"{'Product':<20}"
            f"{'Pallets':^10}"
            f"{'Temp':<10}\n"
        )

        self.output.insert(
            "end",
            "-"*120 + "\n"
        )

        for order in orders:

            self.output.insert(
                "end",
                f"{order.order_number:<12}"
                f"{order.shipping_company:<20}"
                f"{order.origin:<20}"
                f"{order.customer:<20}"
                f"{order.destination:<20}"
                f"{order.product:<20}"
                f"{str(order.pallets):^10}"
                f"{order.temperature:<10}\n"
            )

        self.output.insert(
            "end",
            f"\nTotal Orders : {len(orders)}"
        )
            
    
    def show_route_planner(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Route Planner",
            font=("Arial", 26, "bold")
        ).pack(pady=(20, 10))

        controls = ctk.CTkFrame(
            self.content
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.order_entry = ctk.CTkEntry(
            controls,
            width=300,
            placeholder_text="Enter starting order number"
        )

        self.order_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        ctk.CTkButton(
            controls,
            text="Build Route",
            command=self.route_planner
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        self.output = ctk.CTkTextbox(
            self.content,
            font=("Consolas", 12)
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.output.insert(
            "end",
            "Enter an order number and click Build Route."
        )
    
    
    def route_planner(self):

        if self.order_entry is None:
            self.show_route_planner()
            return

        order_number = self.order_entry.get().strip()

        if not order_number:
            self.output.delete("1.0", "end")
            self.output.insert(
                "end",
                "Enter an order number."
            )
            return

        route = self.engine.create_route(
            order_number
        )

        self.display_route(route)
    
        order = self.engine.find_order(order_number)

        if order is None:
            self.output.insert("end", "Order not found.")
            return

        route = self.engine.route_planner(order)

        self.display_route(route)
        
    def display_route(self, route):

        self.output.delete("1.0", "end")

        self.output.insert("end", "ZaTransport Dispatch\n\n")

        self.output.insert("end", f"Origin: {route.start}\n\n")

        for stop in route.orders:
            
                        
            self.output.insert(
                "end",
                f"{stop.order_number}   "
                f"{stop.shipping_company}   "
                f"{stop.origin}   "
                f"{stop.destination}   "
                f"{stop.product}   "
                f"{stop.pallets}   "
                f"{stop.temperature}  "
            )

        self.output.insert(
            "end",
            f"\nTotal Pallets: {route.total_pallets}"
        )    
    
    
    def display_route(self, route):

        self.output.delete("1.0","end")

        if route is None:
            self.output.insert("end","Unable to build route.")
            return

        self.output.insert("end","ZaTransport Dispatch\n\n")
        
        self.output.insert(
            "end",
            f"{'Order #':<12}"
            f"{'Shipper':<15}"
            f"{'Origin':<15}"
            f"{'Customer':<15}"
            f"{'Destination':<15}"
            f"{'Product':<15}"
            f"{'Pallets':^5}"
            f"{'Temp':>10}\n"
        )

        self.output.insert(
            "end",
            "-"*120 + "\n"
        )                
        
        
        for stop in route.orders:
                           
            self.output.insert(
               "end",
                f"{stop.order_number:<12}   "
                f"{stop.shipping_company:<7}   "
                f"{stop.origin:<7}   "
                f"{stop.customer:<7}   "
                f"{stop.destination:<7}   "
                f"{stop.product:<7}   "
                f"{stop.pallets:^5}   "
                f"{stop.temperature:<12}  "
            )
    
    def display_orders(self, orders, title="Order Search Results"):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text=title,
            font=("Arial", 24, "bold")
        ).pack(pady=(20, 10))

        self.output = ctk.CTkTextbox(
            self.content,
            width=1000,
            height=650,
            font=("Consolas", 12)
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(10, 20)
        )

        if not orders:

            self.output.insert(
                "end",
                "No matching orders found."
            )

            return

        self.output.insert(
            "end",
            f"{'Order #':<12}"
            f"{'Origin':<20}"
            f"{'Customer':<20}"
            f"{'Destination':<20}"
            f"{'Product':<20}"
            f"{'Pallets':^10}"
            f"{'Temp':<12}\n"
        )

        self.output.insert(
            "end",
            "-" * 120 + "\n"
        )

        for order in orders:

            self.output.insert(
                "end",
                f"{order.order_number:<12}"
                f"{order.origin:<20}"
                f"{order.customer:<20}"
                f"{order.destination:<20}"
                f"{order.product:<20}"
                f"{order.pallets:^10}"
                f"{order.temperature:<12}\n"
            )

        self.output.insert(
            "end",
            f"\nTotal Orders: {len(orders)}"
        )


    #########################################################
    # Warehouse Screen
    #########################################################

    def warehouse(self):

        self.clear_content()

        warehouse = self.engine.warehouse
        orders = warehouse.get_orders()
        locations = warehouse.get_locations()

        ctk.CTkLabel(
            self.content,
            text="Warehouse Operations",
            font=("Arial", 26, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.content,
            text="Inventory from WarehouseData",
            font=("Arial", 14)
        ).pack(pady=(0, 15))

        summary_frame = ctk.CTkFrame(
            self.content
        )

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.create_summary_card(
            summary_frame,
            "Warehouse Orders",
            len(orders),
            0
        )

        self.create_summary_card(
            summary_frame,
            "Locations",
            len(locations),
            1
        )

        self.create_summary_card(
            summary_frame,
            "Dock Doors",
            len(warehouse.doors),
            2
        )

        self.create_summary_card(
            summary_frame,
            "Trailers",
            len(warehouse.trailers),
            3
        )

        location_frame = ctk.CTkScrollableFrame(
            self.content,
            label_text="Warehouse Locations",
            height=110,
            orientation="horizontal"
        )

        location_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            location_frame,
            text="All Locations",
            width=140,
            command=self.show_all_warehouse_orders
        ).pack(
            side="left",
            padx=5,
            pady=10
        )

        for location in locations:

            ctk.CTkButton(
                location_frame,
                text=location,
                width=140,
                command=lambda selected=location:
                    self.show_warehouse_location(selected)
            ).pack(
                side="left",
                padx=5,
                pady=10
            )

        ctk.CTkButton(
            self.content,
            text="Refresh WarehouseData",
            command=self.reload_warehouse
        ).pack(pady=5)

        self.output = ctk.CTkTextbox(
            self.content,
            font=("Consolas", 13)
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(10, 20)
        )

        self.display_warehouse_orders(
            orders,
            "All Warehouse Locations"
        )


    def create_summary_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=10
        )

        card.grid(
            row=0,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14)
        ).pack(pady=(12, 3))

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 12))


    def show_all_warehouse_orders(self):

        orders = self.engine.warehouse.get_orders()

        self.display_warehouse_orders(
            orders,
            "All Warehouse Locations"
        )


    def show_warehouse_location(
        self,
        location
    ):

        orders = self.engine.warehouse.get_location(
            location
        )

        self.display_warehouse_orders(
            orders,
            location
        )


    def display_warehouse_orders(
        self,
        orders,
        heading
    ):

        if self.output is None:
            return

        self.output.delete(
            "1.0",
            "end"
        )

        self.output.insert(
            "end",
            f"{heading.upper()}\n\n"
        )

        self.output.insert(
            "end",
            f"{'Order #':<14}"
            f"{'Trailer':<14}"
            f"{'Location':<18}"
            f"{'Product':<25}"
            f"{'Pallets':>9}"
            f"{'Status':>15}"           
        )

        self.output.insert(
            "end",
            "-" * 107 + "\n"
        )

        total_pallets = 0

        for order in orders:

            total_pallets += order.pallets

            self.output.insert(
                "end",
                f"{order.order_number:<14}"
                f"{order.trailer:<14}"
                f"{order.location:<18}"
                f"{order.product:<25}"
                f"{order.pallets:>9}"
                f"{order.status:>15}"
            )

        self.output.insert(
            "end",
            "\n"
            f"Orders: {len(orders)}\n"
            f"Total Pallets: {total_pallets}\n"
        )


    def reload_warehouse(self):

        loaded = self.engine.warehouse.reload()

        if loaded:
            self.warehouse()

        else:
            self.output.delete(
                "1.0",
                "end"
            )

            self.output.insert(
                "end",
                "Unable to reload WarehouseData."
            )


    #########################################################
    # Other Placeholder Screens
    #########################################################

    def view_all_orders(self):
        print("Display all orders")


    def view_zone(self, zone):
        print(f"Display Zone {zone}")


    def search_order(self):
        print("Search order")


    def dispatch_planner(self):
        print("Route Planner")


    def drivers(self):
        print("Drivers")


    def settings(self):
        print("Settings")    