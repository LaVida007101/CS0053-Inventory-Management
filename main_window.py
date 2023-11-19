import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import customtkinter as ctk
import data_base as db

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class salesScrollableFrame:
    def __init__(self, frame) -> None:
        self.frame = ctk.CTkScrollableFrame(frame)
        self.frame.place(rely="0.12", relwidth="1", relheight="0.88")
        self.products = db.get_all_products()

        for item in self.products:
            self.product_frame = ctk.CTkFrame(self.frame)
            self.product_frame.pack(pady=(0,6), expand=True, fill="both")

            self.product_frame.rowconfigure(0, weight=0)
            self.product_frame.columnconfigure(0, minsize=80, weight=1)
            self.product_frame.columnconfigure(1, minsize=120, weight=1)
            self.product_frame.columnconfigure(2, minsize=80, weight=1)
            self.product_frame.columnconfigure(3, minsize=90, weight=1)
            self.product_frame.columnconfigure(4, minsize=90, weight=1)

            self.id_label= ctk.CTkLabel(self.product_frame, text=item["id"]).grid(row=0, column=0)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["name"]).grid(row=0, column=1)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["price"]).grid(row=0, column=2)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["inventoryDate"]).grid(row=0, column=3)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["amount_sold"]).grid(row=0, column=4)
    

class dashScrollableFrame:
    def __init__(self, frame) -> None:
        self.frame = ctk.CTkScrollableFrame(frame)
        self.frame.place(rely="0.12", relwidth="1", relheight="0.88")
        self.low_inventory_products = db.get_low_product_stock()

        for item in self.low_inventory_products:
            self.product_frame = ctk.CTkFrame(self.frame)
            self.product_frame.pack(pady=(0,6), expand=True, fill="both")

            self.product_frame.rowconfigure(0, weight=0)
            self.product_frame.columnconfigure(0, minsize=80, weight=1)
            self.product_frame.columnconfigure(1, minsize=120, weight=1)
            self.product_frame.columnconfigure(2, minsize=80, weight=1)
            self.product_frame.columnconfigure(3, minsize=90, weight=1)
            self.product_frame.columnconfigure(4, minsize=90, weight=1)

            self.id_label= ctk.CTkLabel(self.product_frame, text=item["id"]).grid(row=0, column=0)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["name"]).grid(row=0, column=1)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["stockCount"]).grid(row=0, column=2)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["inventoryDate"]).grid(row=0, column=3)

            self.remarks = None
            if item["stockCount"] == 0:
                self.remarks = "No Stock"
            else:
                self.remarks = "Low Stock"

            self.id_label= ctk.CTkLabel(self.product_frame, text=self.remarks).grid(row=0, column=4)
            

class SaleFrame:
    def __init__(self, window) -> None:

        self.chart_frame = ctk.CTkFrame(window)
        self.chart_frame.pack_propagate(False)
        self.chart_frame.place(relx = 0.22, rely = 0.08, relwidth=0.409, relheight=0.36)

        self.fig = Figure(figsize = (5, 5),
                 dpi = 100)
        self.products = db.get_most_recent_sold()
        self.most_recent_sold_products = []
        self.items_sold = []

        for key, value in self.products:
            if len(self.most_recent_sold_products) < 10:
                self.most_recent_sold_products.append(key)
                self.items_sold.append(value)

        self.plot1 = self.fig.add_subplot(111)

        self.bars = self.plot1.bar(self.most_recent_sold_products, self.items_sold)

        self.plot1.set_title("Most sold products this month")
        self.plot1.set_xticks([])
        self.plot1.set_xticklabels([])

        self.plot1.tick_params(axis='x', which='both', bottom=False, top=False)

        for i, bar in enumerate(self.bars):
            self.plot1.text(bar.get_x() + bar.get_width() / 2,
                    -0.1 * max(self.items_sold),
                    str(self.most_recent_sold_products[i]),
                    ha='center',
                    va='bottom')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack()
  

        self.add_frame = ctk.CTkFrame(window)
        self.add_frame.pack_propagate(False)
        self.add_frame.place(relx = 0.64, rely = 0.08, relwidth=0.35, relheight=0.36)
        
        self.add_frame.rowconfigure((0,1,2,3,4), weight=1)
        self.add_frame.columnconfigure(0, weight = 1)

        self.id_label = ctk.CTkLabel(self.add_frame, text="Product ID")
        self.id_sale = ctk.CTkEntry(self.add_frame)
        self.no_sold_label = ctk.CTkLabel(self.add_frame, text="Amount of Sold Items")
        self.no_sold_sale = ctk.CTkEntry(self.add_frame)

        self.id_label.grid(row=0, column=0, padx=(18,60),pady=(15,0), sticky="w")
        self.id_sale.grid(row=1, column=0, padx=(15,15), sticky="nesw")
        self.no_sold_label.grid(row=2, column=0, padx=(18,0), pady=(40,0), sticky="w")
        self.no_sold_sale.grid(row=3, column=0, padx=(15,15), pady=(0,30), sticky="nesw")

        self.add_sale = ctk.CTkButton(
            self.add_frame,
            text="Add Sale Data",
            font=("Bold", 18),
            corner_radius=5,
            fg_color="#91948e",
            text_color="#262626",
            command=self.add_sales_data
            )
        self.add_sale.grid(row=4, column=0, padx=(0,15), pady=(0, 20), sticky="e")

        self.sales_list = ctk.CTkFrame(window)
        self.sales_list.pack_propagate(False)
        self.sales_list.place(relx = 0.22, rely = 0.46, relwidth=0.769, relheight=0.55)

        self.category_labels = ctk.CTkFrame(self.sales_list, fg_color="transparent")
        self.category_labels.pack_propagate(False)
        self.category_labels.place(relheight=0.12, relwidth=1)

        self.category_labels.rowconfigure(1, weight=0)
        self.category_labels.columnconfigure(0, minsize=80, weight=1)
        self.category_labels.columnconfigure(1, minsize=120, weight=1)
        self.category_labels.columnconfigure(2, minsize=80, weight=1)
        self.category_labels.columnconfigure(3, minsize=80, weight=1)
        self.category_labels.columnconfigure(4, minsize=90, weight=1)

        self.id_category = ctk.CTkLabel(self.category_labels, text="ID")
        self.name_category = ctk.CTkLabel(self.category_labels, text="Name")
        self.stockcount_category = ctk.CTkLabel(self.category_labels, text="Price")
        self.inventorydate_category = ctk.CTkLabel(self.category_labels, text="Last Stock Date")
        self.remarks_category = ctk.CTkLabel(self.category_labels, text="Number Sold")

        self.id_category.grid(row=0, column=0, pady=(20,0))
        self.name_category.grid(row=0, column=1, pady=(20,0))
        self.stockcount_category.grid(row=0, column=2, pady=(20,0))  
        self.inventorydate_category.grid(row=0, column=3, padx=(0,10), pady=(20,0))
        self.remarks_category.grid(row=0, column=4, padx=(0,30), pady=(20,0))

        salesScrollableFrame(self.sales_list)

    def add_sales_data(self):
        db.add_sales(self.id_sale.get(), int(self.no_sold_sale.get()))

class MainDashboardFrame:
    def __init__(self, window) -> None:
        self.frame = ctk.CTkFrame(window)
        dashScrollableFrame(self.frame)
        self.frame.pack_propagate(False)
        self.frame.place(relx = 0.22, rely = 0.27, relwidth = 0.769, relheight = 0.72)


        self.category_labels = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.category_labels.pack_propagate(False)
        self.category_labels.place(relheight=0.12, relwidth=1)

        self.category_labels.rowconfigure(1, weight=0)
        self.category_labels.columnconfigure(0, minsize=80, weight=1)
        self.category_labels.columnconfigure(1, minsize=120, weight=1)
        self.category_labels.columnconfigure(2, minsize=80, weight=1)
        self.category_labels.columnconfigure(3, minsize=80, weight=1)
        self.category_labels.columnconfigure(4, minsize=90, weight=1)

        self.id_category = ctk.CTkLabel(self.category_labels, text="ID")
        self.name_category = ctk.CTkLabel(self.category_labels, text="Name")
        self.stockcount_category = ctk.CTkLabel(self.category_labels, text="Available")
        self.inventorydate_category = ctk.CTkLabel(self.category_labels, text="Last Stock Date")
        self.remarks_category = ctk.CTkLabel(self.category_labels, text="Remark")

        self.id_category.grid(row=0, column=0, pady=(20,0))
        self.name_category.grid(row=0, column=1, pady=(20,0))
        self.stockcount_category.grid(row=0, column=2, pady=(20,0))  
        self.inventorydate_category.grid(row=0, column=3, padx=(0,10), pady=(20,0))
        self.remarks_category.grid(row=0, column=4, padx=(0,30), pady=(20,0))

        self.label_frame = ctk.CTkFrame(window, fg_color="transparent")
        self.label_frame.pack_propagate(False)
        self.label_frame.place(relx = 0.22, rely = 0.215, relwidth = 0.769, relheight=0.05)
        self.inventory_label = ctk.CTkLabel(
            self.label_frame,
            text = "Inventory Notice",
            font = (None, 20)
            ).pack(side = "left", padx = 10)


class productsScrollable:
    def __init__(self, frame) -> None:
        self.frame = ctk.CTkScrollableFrame(frame)
        self.frame.place(rely="0.12", relwidth="1", relheight="0.88")
        self.low_inventory_products = db.get_all_products()

        for item in self.low_inventory_products:
            self.product_frame = ctk.CTkFrame(self.frame)
            self.product_frame.pack(pady=(0,6), expand=True, fill="both")

            self.product_frame.rowconfigure(0, weight=0)
            self.product_frame.columnconfigure(0, minsize=80, weight=1)
            self.product_frame.columnconfigure(1, minsize=120, weight=1)
            self.product_frame.columnconfigure(2, minsize=80, weight=1)
            self.product_frame.columnconfigure(3, minsize=90, weight=1)
            self.product_frame.columnconfigure(4, minsize=90, weight=1)

            self.id_label= ctk.CTkLabel(self.product_frame, text=item["id"]).grid(row=0, column=0)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["name"]).grid(row=0, column=1)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["price"]).grid(row=0, column=2)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["stockCount"]).grid(row=0, column=3)
            self.id_label= ctk.CTkLabel(self.product_frame, text=item["inventoryDate"]).grid(row=0, column=4)
        

class productsList:
    def __init__(self, frame) -> None:
        self.frame = ctk.CTkFrame(frame)
        dashScrollableFrame(self.frame)
        self.frame.pack_propagate(False)
        self.frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)


        self.category_labels = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.category_labels.pack_propagate(False)
        self.category_labels.place(relheight=0.12, relwidth=1)

        self.category_labels.rowconfigure(1, weight=0)
        self.category_labels.columnconfigure(0, minsize=80, weight=1)
        self.category_labels.columnconfigure(1, minsize=120, weight=1)
        self.category_labels.columnconfigure(2, minsize=80, weight=1)
        self.category_labels.columnconfigure(3, minsize=80, weight=1)
        self.category_labels.columnconfigure(4, minsize=90, weight=1)

        self.id_category = ctk.CTkLabel(self.category_labels, text="ID")
        self.name_category = ctk.CTkLabel(self.category_labels, text="Name")
        self.stockcount_category = ctk.CTkLabel(self.category_labels, text="Price")
        self.inventorydate_category = ctk.CTkLabel(self.category_labels, text="Available")
        self.remarks_category = ctk.CTkLabel(self.category_labels, text="Last Stock Date")

        self.id_category.grid(row=0, column=0, pady=(20,0))
        self.name_category.grid(row=0, column=1, pady=(20,0))
        self.stockcount_category.grid(row=0, column=2, pady=(20,0))  
        self.inventorydate_category.grid(row=0, column=3, padx=(0,10), pady=(20,0))
        self.remarks_category.grid(row=0, column=4, padx=(0,30), pady=(20,0))

        productsScrollable(self.frame)

class ProductsFrame:
    def __init__(self, window) -> None:

        self.product_info = None
        
        self.tab_view = ctk.CTkTabview(window, command=self.render_tab)
        self.tab_view.place(relx = 0.22, relwidth = 0.769, relheight = 1)

        self.tab_view.add("Products")
        self.tab_view.add("Add Product")
        self.tab_view.add("Update Product")
        self.tab_view.add("Delete Product")

        self.view_products = ctk.CTkFrame(self.tab_view.tab("Products"), fg_color="transparent")
        self.view_products.place(relx=0.01, rely=0.05, relwidth=1, relheight=0.95)

        productsList(self.view_products)

        self.add_tab_frame = ctk.CTkFrame(self.tab_view.tab("Add Product"), fg_color="transparent")
        self.add_tabtitle_frame = ctk.CTkFrame(self.tab_view.tab("Add Product"), fg_color="transparent")
        self.add_tab_frame.place(relx=0.01, rely=0.05, relwidth=1, relheight=0.95)
        self.add_tabtitle_frame.place(relx=0.01, relwidth=1, relheight=0.05)

        self.add_tab_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight = 0)
        self.add_tab_frame.columnconfigure((0,1), weight = 0)


        self.update_tab_frame = ctk.CTkFrame(self.tab_view.tab("Update Product"), fg_color="transparent")
        self.update_tabtitle_frame = ctk.CTkFrame(self.tab_view.tab("Update Product"), fg_color="transparent")
        self.update_tab_frame.place(relx=0.01, rely=0.05, relwidth=1, relheight=0.95)
        self.update_tabtitle_frame.place(relx=0.01, relwidth=1, relheight=0.05)

        self.update_tabtitle_frame.rowconfigure((0), weight = 0)
        self.update_tabtitle_frame.columnconfigure((0,1), weight = 0)
        self.update_tab_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight = 0)
        self.update_tab_frame.columnconfigure((0,1), weight = 0)

        self.render_tab()



        
    def render_tab(self):
        self.current_tab = self.tab_view.get()
        

        if self.current_tab == "Add Product":
            self.add_label_title = ctk.CTkLabel(self.add_tabtitle_frame,text="Add New Product", font=(None, 25))
            self.add_label_title.pack(side="left")
            self.get_product_info(self.add_tab_frame)
            self.add_submit = ctk.CTkButton(self.add_tab_frame, text="Add Product", width=200, font=(None, 17), command=self.add_new_product)
            self.add_submit.grid(row="12", columnspan=2, pady=(45,0))
        elif self.current_tab == "Update Product":
            self.add_label_title.forget()
            self.add_label_title = ctk.CTkLabel(self.update_tabtitle_frame,text="Update Product", font=(None, 25)).grid(row=0, column=0)
            self.get_product_info(self.update_tab_frame)
            self.add_submit = ctk.CTkButton(self.update_tab_frame, text="Add Product", width=200, font=(None, 17), command=self.update_product)
            self.add_submit.grid(row="12", columnspan=2, pady=(45,0))


        
    def get_product_info(self, frame):
        self.add_label_id = ctk.CTkLabel(frame,text="Product ID")
        self.add_label_id.grid(row=0, column=0, padx=(0,230), pady=(35,0))
        self.add_enter_id = ctk.CTkEntry(frame, width=300)
        self.add_enter_id.grid(row=1, column=0, columnspan=2)

        self.add_label_name = ctk.CTkLabel(frame,text="Product Name")
        self.add_label_name.grid(row=2, column=0, padx=(0,210), pady=(15,0))
        self.add_enter_name = ctk.CTkEntry(frame, width=300)
        self.add_enter_name.grid(row=3, column=0, columnspan=2)

        self.add_label_ini_stock = ctk.CTkLabel(frame,text="Initial Stock Level")
        self.add_label_ini_stock.grid(row=4, column=0, padx=(15,210), pady=(15,0))
        self.add_enter_ini_stock = ctk.CTkEntry(frame, width=300)
        self.add_enter_ini_stock.grid(row=5, column=0, columnspan=2)

        self.add_label_restock = ctk.CTkLabel(frame,text="Initial Reorder Level")
        self.add_label_restock.grid(row=6, column=0, padx=(25,210), pady=(15,0))
        self.add_enter_restock = ctk.CTkEntry(frame, width=300)
        self.add_enter_restock.grid(row=7, column=0, columnspan=2)

        self.add_label_unit_cost = ctk.CTkLabel(frame,text="Cost per Unit")
        self.add_label_unit_cost.grid(row=8, column=0, padx=(25,250), pady=(15,0))
        self.add_enter_unit_cost = ctk.CTkEntry(frame, width=300)
        self.add_enter_unit_cost.grid(row=9, column=0, columnspan=2)

        self.add_label_price = ctk.CTkLabel(frame,text="Product Price")
        self.add_label_price.grid(row=10, column=0, padx=(35,250), pady=(15,0))
        self.add_enter_price = ctk.CTkEntry(frame, width=300)
        self.add_enter_price.grid(row=11, column=0, columnspan=2)



    
    def add_new_product(self):
        self.product_info = [
        int(self.add_enter_id.get()),
        self.add_enter_name.get(),
        int(self.add_enter_ini_stock.get()),
        int(self.add_enter_restock.get()),
        int(self.add_enter_unit_cost.get()),
        int(self.add_enter_price.get()),
        datetime.date.today()
        ]

        db.add_data(self.product_info)

    def update_product(self):
        self.product_info = [
        int(self.add_enter_id.get()),
        self.add_enter_name.get(),
        int(self.add_enter_ini_stock.get()),
        int(self.add_enter_restock.get()),
        int(self.add_enter_unit_cost.get()),
        int(self.add_enter_price.get()),
        ]

        if db.get_product(self.product_info[0]) != -1:
            db.update_data(self.product_info)


class LeftDashboardFrame:
    def __init__(self, window) -> None:
        self.frame = ctk.CTkFrame(window)
        self.frame.pack_propagate(False)
        self.frame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)

        self.frame.rowconfigure((0,1,2), weight = 0)
        self.frame.columnconfigure((0), weight = 1)




class Dashboard:
    def __init__(self) -> None:
        self.sales_frame = None
        self.products_frame = None
        
        self.window = ctk.CTk()
        self.main_frame = MainDashboardFrame(self.window)
        self.left_frame = LeftDashboardFrame(self.window)
        self.products_frame = None
        self.window.geometry("950x660")    
        self.window.minsize(800,660)   

        self.product_label = ctk.CTkButton(
            self.left_frame.frame,
            text = "Add Sale",
            fg_color="transparent",
            command = self.initialize_sales_frame
            ).grid(row = 1, column = 0)

        self.dash_board_label = ctk.CTkButton(
            self.left_frame.frame,
            text = "Dashboard",
            fg_color="transparent",
            command=self.initialize_dashboard
            ).grid(row = 1, column = 0, pady=(50,0))
        
        self.product_label = ctk.CTkButton(
            self.left_frame.frame,
            text = "Product",
            fg_color="transparent",
            command=self.initialize_product_frame
            ).grid(row = 2, column = 0)
        
        
        self.window.mainloop()

    def initialize_product_frame(self):
        self.main_frame.frame.place_forget()
        if self.sales_frame is not None:
                self.sales_frame.chart_frame.place_forget()
                self.sales_frame.add_sale.place_forget()
                self.sales_frame.add_frame.place_forget()
        if self.products_frame is not None:
            self.products_frame.tab_view.place_forget()
        # self.main_frame.label_frame.place_forget
        self.products_frame = ProductsFrame(self.window)

    def initialize_dashboard(self):
        if self.products_frame is not None:
            self.products_frame.tab_view.place_forget()
        if self.sales_frame is not None:
            self.sales_frame.chart_frame.place_forget()
            self.sales_frame.sales_list.place_forget()
            self.sales_frame.add_frame.place_forget()
        if self.main_frame is not None:
            self.main_frame.frame.place_forget()
        self.main_frame = MainDashboardFrame(self.window)

    def initialize_sales_frame(self):
        if self.products_frame is not None:
            self.products_frame.tab_view.place_forget()
        if self.sales_frame is not None:
            self.sales_frame.chart_frame.place_forget()
            self.sales_frame.sales_list.place_forget()
            self.sales_frame.add_frame.place_forget()
        if self.main_frame is not None:
            self.main_frame.frame.place_forget()
        self.sales_frame = SaleFrame(self.window)

def main():
    app_window = Dashboard()

if __name__ == "__main__":
    main()
