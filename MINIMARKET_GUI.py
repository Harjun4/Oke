import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog

class User:
    def __init__(self, username, password, role, cashier_name=None):
        self.username = username
        self.password = password
        self.role = role
        self.cashier_name = cashier_name

class Minimarket:
    def __init__(self):
        self.users = []
        self.items = []
        self.sales = []
        self.cart = []  

    def register(self, username, password, role, cashier_name=None):
        new_user = User(username, password, role, cashier_name)
        self.users.append(new_user)

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user.role, user.cashier_name
        return None, None
    
    def add_item(self, name, price, discount, stock):
        self.items.append({"name": name, "price": price, "discount": discount, "stock": stock})

    def record_sale(self, cart, total_price, cashier_name):
        self.sales.append({"cart": cart, "total_price": total_price, "cashier_name": cashier_name})

    def view_sales_history(self):
        total_accumulated_sales = 0
        for idx, sale in enumerate(self.sales, start=1):
            print(f"Sale {idx}:")
            cart = sale["cart"]
            total_price = sale["total_price"]
            cashier_name = sale["cashier_name"]
            total_accumulated_sales += total_price
            print(f"Nama Kasir: {cashier_name}")
            print("Item:")
            for item in cart:
                print(f"{item['item']['name']} x{item['quantity']} - Rp. {item['item']['price'] * item['quantity']:.2f}")
            print(f"Total Harga: Rp. {total_price:.2f}")
            print("-----------------------------------")
        print(f"Total Penjualan: Rp. {total_accumulated_sales:.2f}")

    def delete_item(self, item_name):
        for i, item in enumerate(self.items):
            if item['name'] == item_name:
                del self.items[i]
                return True
        return False

    def edit_item(self, item_name, new_name, new_price, new_discount, new_stock):
        for item in self.items:
            if item['name'] == item_name:
                item['name'] = new_name
                item['price'] = new_price
                item['discount'] = new_discount
                item['stock'] = new_stock
                return True
        return False

class MinimarketGUI(tk.Tk):
    def __init__(self, market):
        super().__init__()
        self.market = market
        self.current_user_role = None
        self.current_cashier_name = None

        self.title("Minimarket System")
        self.geometry("500x400")

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register).grid(row=3, columnspan=2, pady=10)

    def create_cashier_frame(self):
        self.cashier_frame = tk.Frame(self)
        self.cashier_frame.pack(pady=20)

        self.cart_items_label = tk.Label(self.cashier_frame, text="Cart Items:")
        self.cart_items_label.pack()

        self.cart_listbox = tk.Listbox(self.cashier_frame, width=40, height=5)
        self.cart_listbox.pack(pady=5)

        self.total_price_label = tk.Label(self.cashier_frame, text="Total Price: Rp. 0.00")
        self.total_price_label.pack()

        self.item_list_label = tk.Label(self.cashier_frame, text="Available Items:")
        self.item_list_label.pack()

        self.item_list = ttk.Treeview(self.cashier_frame, columns=("Name", "Price", "Discount", "Stock"), show="headings")
        self.item_list.heading("Name", text="Name")
        self.item_list.heading("Price", text="Price")
        self.item_list.heading("Discount", text="Discount")
        self.item_list.heading("Stock", text="Stock")
        self.item_list.pack(pady=5)

        for item in self.market.items:
            self.item_list.insert("", tk.END, values=(item["name"], item["price"], item["discount"], item["stock"]))

        self.add_item_button = tk.Button(self.cashier_frame, text="Add Item to Cart", command=self.add_item_to_cart)
        self.add_item_button.pack(pady=5)

        self.checkout_button = tk.Button(self.cashier_frame, text="Checkout", command=self.checkout)
        self.checkout_button.pack(pady=5)

        self.logout_button = tk.Button(self.cashier_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=5)

    def create_manager_frame(self):
        self.manager_frame = tk.Frame(self)
        self.manager_frame.pack(pady=20)

        self.item_list_label = tk.Label(self.manager_frame, text="Available Items:")
        self.item_list_label.pack()

        self.item_list = ttk.Treeview(self.manager_frame, columns=("Name", "Price", "Discount", "Stock"), show="headings")
        self.item_list.heading("Name", text="Name")
        self.item_list.heading("Price", text="Price")
        self.item_list.heading("Discount", text="Discount")
        self.item_list.heading("Stock", text="Stock")
        self.item_list.pack(pady=5)

        for item in self.market.items:
            self.item_list.insert("", tk.END, values=(item["name"], item["price"], item["discount"], item["stock"]))

        self.add_item_button = tk.Button(self.manager_frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=5)

        self.delete_item_button = tk.Button(self.manager_frame, text="Delete Item", command=self.delete_item)
        self.delete_item_button.pack(pady=5)

        self.edit_item_button = tk.Button(self.manager_frame, text="Edit Item", command=self.edit_item)
        self.edit_item_button.pack(pady=5)

        self.view_sales_history_button = tk.Button(self.manager_frame, text="View Sales History", command=self.view_sales_history)
        self.view_sales_history_button.pack(pady=5)

        self.logout_button = tk.Button(self.manager_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        role, cashier_name = self.market.login(username, password)

        if role is None:
            messagebox.showerror("Error", "Invalid username or password")
            return

        self.current_user_role = role
        self.current_cashier_name = cashier_name

        self.login_frame.destroy()

        if role == "1":  # Cashier
            self.create_cashier_frame()
        elif role == "2":  # Manager
            self.create_manager_frame()

    def register(self):
        def register_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            cashier_name = cashier_name_entry.get() if role == "1" else None
            self.market.register(username, password, role, cashier_name)
            register_window.destroy()
            messagebox.showinfo("Registration", "User registered successfully!")

        register_window = tk.Toplevel(self)
        register_window.title("Registration")

        username_label = tk.Label(register_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(register_window)
        username_entry.pack()

        password_label = tk.Label(register_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack()

        role_label = tk.Label(register_window, text="Role:")
        role_label.pack()
        role_var = tk.StringVar(register_window)
        role_var.set("1")
        role_radio_1 = tk.Radiobutton(register_window, text="Cashier", variable=role_var, value="1")
        role_radio_1.pack()
        role_radio_2 = tk.Radiobutton(register_window, text="Manager", variable=role_var, value="2")
        role_radio_2.pack()

        cashier_name_label = tk.Label(register_window, text="Cashier Name:")
        cashier_name_label.pack()
        cashier_name_entry = tk.Entry(register_window)
        cashier_name_entry.pack()

        register_button = tk.Button(register_window, text="Register", command=register_user)
        register_button.pack()

    def add_item_to_cart(self):
        selected_item = self.item_list.selection()
        if selected_item:
            item_values = self.item_list.item(selected_item[0], "values")
            item_name = item_values[0]
            stock = int(item_values[3])

            if stock > 0:
                quantity = simpledialog.askinteger("Quantity", "Enter quantity for " + item_name + ":")

                if quantity is not None and 0 < quantity <= stock:
                    item = next((x for x in self.market.items if x['name'] == item_name), None)
                    self.market.cart.append({"item": item, "quantity": quantity})
                    item['stock'] -= quantity

                    self.cart_listbox.delete(0, tk.END)
                    for item in self.market.cart:
                        self.cart_listbox.insert(tk.END, f"{item['item']['name']} x{item['quantity']}")
                    self.update_total_price()

                    self.item_list.item(selected_item[0], values=(item_name, item_values[1], item_values[2], item['stock']))
                else:
                    messagebox.showwarning("Warning", "Invalid quantity.")
            else:
                messagebox.showwarning("Warning", "Item out of stock.")
        else:
            messagebox.showwarning("Warning", "Please select an item from the list.")

    def checkout(self):
        if self.market.cart:
            total_price = sum(item['item']['price'] * item['quantity'] for item in self.market.cart)

            payment = simpledialog.askfloat("Payment", "Enter payment amount:")
            if payment is not None and payment >= total_price:
                change = payment - total_price

                self.market.record_sale(self.market.cart, total_price, self.current_cashier_name)

                messagebox.showinfo("Checkout", f"Total price: Rp. {total_price:.2f}\nPayment: Rp. {payment:.2f}\nChange: Rp. {change:.2f}")

                self.market.cart = []
                self.cart_listbox.delete(0, tk.END)
                self.update_total_price()

            else:
                messagebox.showerror("Error", "Invalid payment amount.")
        else:
            messagebox.showwarning("Warning", "Your cart is empty.")

    def add_item(self):
        def add_item_to_market():
            name = name_entry.get()
            price = float(price_entry.get())
            discount = float(discount_entry.get())
            stock = int(stock_entry.get())
            self.market.add_item(name, price, discount, stock)
            self.item_list.insert("", tk.END, values=(name, price, discount, stock))
            add_item_window.destroy()
            messagebox.showinfo("Add Item", "Item added successfully!")

        add_item_window = tk.Toplevel(self)
        add_item_window.title("Add Item")

        name_label = tk.Label(add_item_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(add_item_window)
        name_entry.pack()

        price_label = tk.Label(add_item_window, text="Price:")
        price_label.pack()
        price_entry = tk.Entry(add_item_window)
        price_entry.pack()

        discount_label = tk.Label(add_item_window, text="Discount:")
        discount_label.pack()
        discount_entry = tk.Entry(add_item_window)
        discount_entry.pack()

        stock_label = tk.Label(add_item_window, text="Stock:")
        stock_label.pack()
        stock_entry = tk.Entry(add_item_window)
        stock_entry.pack()

        add_button = tk.Button(add_item_window, text="Add", command=add_item_to_market)
        add_button.pack()

    def delete_item(self):
        selected_item = self.item_list.selection()
        if selected_item:
            item_values = self.item_list.item(selected_item[0], "values")
            item_name = item_values[0]
            if messagebox.askyesno("Delete Item", f"Are you sure you want to delete {item_name}?"):
                if self.market.delete_item(item_name):
                    self.item_list.delete(selected_item[0])
                    messagebox.showinfo("Delete Item", f"{item_name} deleted successfully!")
                else:
                    messagebox.showerror("Error", f"Item {item_name} not found.")
        else:
            messagebox.showwarning("Warning", "Please select an item from the list.")

    def edit_item(self):
        selected_item = self.item_list.selection()
        if selected_item:
            item_values = self.item_list.item(selected_item[0], "values")
            item_name = item_values[0]

            def save_edit():
                new_name = name_entry.get()
                new_price = float(price_entry.get())
                new_discount = float(discount_entry.get())
                new_stock = int(stock_entry.get())
                if self.market.edit_item(item_name, new_name, new_price, new_discount, new_stock):
                    self.item_list.item(selected_item[0], values=(new_name, new_price, new_discount, new_stock))
                    edit_window.destroy()
                    messagebox.showinfo("Edit Item", "Item edited successfully!")
                else:
                    messagebox.showerror("Error", "Item not found.")

            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Item")

            name_label = tk.Label(edit_window, text="Name:")
            name_label.pack()
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, item_values[0])
            name_entry.pack()

            price_label = tk.Label(edit_window, text="Price:")
            price_label.pack()
            price_entry = tk.Entry(edit_window)
            price_entry.insert(0, item_values[1])
            price_entry.pack()

            discount_label = tk.Label(edit_window, text="Discount:")
            discount_label.pack()
            discount_entry = tk.Entry(edit_window)
            discount_entry.insert(0, item_values[2])
            discount_entry.pack()

            stock_label = tk.Label(edit_window, text="Stock:")
            stock_label.pack()
            stock_entry = tk.Entry(edit_window)
            stock_entry.insert(0, item_values[3])
            stock_entry.pack()

            save_button = tk.Button(edit_window, text="Save", command=save_edit)
            save_button.pack()

        else:
            messagebox.showwarning("Warning", "Please select an item from the list.")

    def view_sales_history(self):
        sales_window = tk.Toplevel(self)
        sales_window.title("Sales History")

        sales_text = tk.Text(sales_window, wrap=tk.WORD)
        sales_text.pack(expand=1, fill='both')

        total_accumulated_sales = 0
        for idx, sale in enumerate(self.market.sales, start=1):
            sales_text.insert(tk.END, f"Sale {idx}:\n")
            cart = sale["cart"]
            total_price = sale["total_price"]
            cashier_name = sale["cashier_name"]
            total_accumulated_sales += total_price
            sales_text.insert(tk.END, f"Nama Kasir: {cashier_name}\n")
            sales_text.insert(tk.END, "Items:\n")
            for item in cart:
                sales_text.insert(tk.END, f"{item['item']['name']} x{item['quantity']} - Rp. {item['item']['price'] * item['quantity']:.2f}\n")
            sales_text.insert(tk.END, f"Total Harga: Rp. {total_price:.2f}\n")
            sales_text.insert(tk.END, "-----------------------------------\n")
        sales_text.insert(tk.END, f"Total Penjualan: Rp. {total_accumulated_sales:.2f}\n")

    def logout(self):
        self.current_user_role = None
        self.current_cashier_name = None
        
        if hasattr(self, 'cashier_frame'):
            self.cashier_frame.destroy()
        elif hasattr(self, 'manager_frame'):
            self.manager_frame.destroy()

        self.create_login_frame()

    def update_total_price(self):
        total_price = sum(item['item']['price'] * item['quantity'] for item in self.market.cart)
        self.total_price_label.config(text=f"Total Price: Rp. {total_price:.2f}")

if __name__ == "__main__":
    market = Minimarket()
    gui = MinimarketGUI(market)
    gui.mainloop()
