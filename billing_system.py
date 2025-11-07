from tkinter import *
import random
import os
from tkinter import messagebox

class Bill_App:
    def __init__(self, root):  # ✅ Fixed constructor
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Billing Software")
        self.bg_color = "#badc57"

        os.makedirs("bills", exist_ok=True)

        title = Label(self.root, text="Billing Software", font=('times new roman', 30, 'bold'),
                      pady=2, bd=12, bg=self.bg_color, fg="Black", relief=GROOVE)
        title.pack(fill=X)

        self.price_list = {
            "Sanitizer": 50, "Mask": 10, "Hand Gloves": 20, "Dettol": 60, "Newsprin": 40, "Thermal Gun": 1000,
            "Rice": 40, "Food Oil": 120, "Wheat": 50, "Daal": 60, "Flour": 30, "Maggi": 20,
            "Sprite": 30, "Limka": 30, "Mazza": 30, "Coke": 30, "Fanta": 30, "Mountain Duo": 40
        }

        self.init_variables()
        self.setup_ui()
        self.welcome_bill()
        self.bind_arrow_navigation()

    def init_variables(self):
        self.sanitizer = StringVar()
        self.mask = StringVar()
        self.hand_gloves = StringVar()
        self.dettol = StringVar()
        self.newsprin = StringVar()
        self.thermal_gun = StringVar()
        self.rice = StringVar()
        self.food_oil = StringVar()
        self.wheat = StringVar()
        self.daal = StringVar()
        self.flour = StringVar()
        self.maggi = StringVar()
        self.sprite = StringVar()
        self.limka = StringVar()
        self.mazza = StringVar()
        self.coke = StringVar()
        self.fanta = StringVar()
        self.mountain_duo = StringVar()

        self.medical_price = StringVar()
        self.grocery_price = StringVar()
        self.cold_drinks_price = StringVar()
        self.medical_tax = StringVar()
        self.grocery_tax = StringVar()
        self.cold_drinks_tax = StringVar()

        self.c_name = StringVar()
        self.c_phone = StringVar()
        self.search_bill = StringVar()
        self.bill_no = StringVar(value=str(random.randint(1000, 9999)))

    def setup_ui(self):
        F1 = LabelFrame(self.root, text="Customer Details", font=('times new roman', 15, 'bold'),
                        bd=10, bg=self.bg_color)
        F1.place(x=0, y=80, relwidth=1)

        Label(F1, text="Customer Name", bg=self.bg_color, font=('times new roman', 15)).grid(row=0, column=0)
        Entry(F1, textvariable=self.c_name, bd=7, relief=GROOVE, font='arial 15', width=15).grid(row=0, column=1, padx=8)

        Label(F1, text="Phone No.", bg=self.bg_color, font=('times new roman', 15)).grid(row=0, column=2)
        Entry(F1, textvariable=self.c_phone, bd=7, relief=GROOVE, font='arial 15', width=15).grid(row=0, column=3, padx=8)

        Label(F1, text="Bill No.", bg=self.bg_color, font=('times new roman', 15)).grid(row=0, column=4)
        Entry(F1, textvariable=self.search_bill, bd=7, relief=GROOVE, font='arial 15', width=15).grid(row=0, column=5, padx=8)

        Button(F1, text="Search", width=10, bd=7, font='arial 12 bold', command=self.find_bill).grid(row=0, column=6)

        self.create_items_section("Medical Purpose", self.medical_items(), 5)
        self.create_items_section("Grocery Items", self.grocery_items(), 340)
        self.create_items_section("Cold Drinks", self.drink_items(), 670)

        F5 = Frame(self.root, bd=10, relief=GROOVE)
        F5.place(x=1010, y=180, width=350, height=380)
        Label(F5, text="Bill Area", font='arial 15 bold', bd=7, relief=GROOVE).pack(fill=X)
        scroll_y = Scrollbar(F5, orient=VERTICAL)
        self.txtarea = Text(F5, yscrollcommand=scroll_y.set, state='disabled')
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)

        F6 = LabelFrame(self.root, text="Bill Summary", font=('times new roman', 14, 'bold'),
                        bd=10, bg=self.bg_color)
        F6.place(x=0, y=560, relwidth=1, height=140)

        labels = [
            ("Total Medical Price", self.medical_price),
            ("Total Grocery Price", self.grocery_price),
            ("Total Cold Drink Price", self.cold_drinks_price),
            ("Medical Tax", self.medical_tax),
            ("Grocery Tax", self.grocery_tax),
            ("Cold Drink Tax", self.cold_drinks_tax),
        ]

        for i, (text, var) in enumerate(labels):
            Label(F6, text=text, font=('times new roman', 14, 'bold'), bg=self.bg_color).grid(row=i//2, column=(i%2)*2, padx=20, pady=1, sticky='w')
            Entry(F6, textvariable=var, bd=7, relief=GROOVE, width=18).grid(row=i//2, column=(i%2)*2+1, padx=10, pady=1)

        btn_f = Frame(F6, bd=7, relief=GROOVE, bg=self.bg_color)
        btn_f.place(x=760, width=580, height=105)
        Button(btn_f, text="Total", command=self.total, width=12, bd=2, pady=15, font='arial 13 bold', bg="#535C68", fg="white").grid(row=0, column=0, padx=5, pady=5)
        Button(btn_f, text="Generate Bill", command=self.bill_area, width=12, bd=2, pady=15, font='arial 13 bold', bg="#535C68", fg="white").grid(row=0, column=1, padx=5, pady=5)
        Button(btn_f, text="Clear", command=self.clear_data, width=12, bd=2, pady=15, font='arial 13 bold', bg="#535C68", fg="white").grid(row=0, column=2, padx=5, pady=5)
        Button(btn_f, text="Exit", command=self.exit_app, width=12, bd=2, pady=15, font='arial 13 bold', bg="#535C68", fg="white").grid(row=0, column=3, padx=5, pady=5)

    def create_items_section(self, title, items, x):
        F = LabelFrame(self.root, text=title, font=('times new roman', 15, 'bold'), bd=10, bg=self.bg_color)
        F.place(x=x, y=180, width=325, height=380)
        for i, (name, var) in enumerate(items):
            Label(F, text=name, font=('times new roman', 16, 'bold'), bg=F['bg']).grid(row=i, column=0, padx=10, pady=10, sticky='w')
            Entry(F, textvariable=var, font=('times new roman', 16, 'bold'), bd=5, relief=GROOVE, width=10).grid(row=i, column=1, padx=10, pady=10)

    def medical_items(self):
        return [("Sanitizer", self.sanitizer), ("Mask", self.mask), ("Hand Gloves", self.hand_gloves),
                ("Dettol", self.dettol), ("Newsprin", self.newsprin), ("Thermal Gun", self.thermal_gun)]

    def grocery_items(self):
        return [("Rice", self.rice), ("Food Oil", self.food_oil), ("Wheat", self.wheat),
                ("Daal", self.daal), ("Flour", self.flour), ("Maggi", self.maggi)]

    def drink_items(self):
        return [("Sprite", self.sprite), ("Limka", self.limka), ("Mazza", self.mazza),
                ("Coke", self.coke), ("Fanta", self.fanta), ("Mountain Duo", self.mountain_duo)]

    def get_qty(self, var):
        try:
            return int(var.get()) if var.get() else 0
        except:
            return 0

    def total(self):
        medical_total = sum(self.get_qty(var) * self.price_list[name] for name, var in self.medical_items())
        grocery_total = sum(self.get_qty(var) * self.price_list[name] for name, var in self.grocery_items())
        drinks_total = sum(self.get_qty(var) * self.price_list[name] for name, var in self.drink_items())

        self.medical_price.set(f"{medical_total:.2f}")
        self.grocery_price.set(f"{grocery_total:.2f}")
        self.cold_drinks_price.set(f"{drinks_total:.2f}")
        self.medical_tax.set(f"{medical_total * 0.05:.2f}")
        self.grocery_tax.set(f"{grocery_total * 0.1:.2f}")
        self.cold_drinks_tax.set(f"{drinks_total * 0.05:.2f}")

    def welcome_bill(self):
        self.txtarea.config(state='normal')
        self.txtarea.delete('1.0', END)
        self.txtarea.config(state='disabled')

    def bill_area(self):
        if self.c_name.get() == "" or self.c_phone.get() == "":
            messagebox.showerror("Error", "Customer details are required")
            return
        if self.medical_price.get() == "" and self.grocery_price.get() == "" and self.cold_drinks_price.get() == "":
            messagebox.showerror("Error", "No product selected")
            return

        self.txtarea.config(state='normal')
        self.txtarea.delete('1.0', END)
        self.txtarea.insert(END, "\tWelcome to the Billing Software\n")
        self.txtarea.insert(END, f"\nBill Number: {self.bill_no.get()}")
        self.txtarea.insert(END, f"\nCustomer Name: {self.c_name.get()}")
        self.txtarea.insert(END, f"\nPhone Number: {self.c_phone.get()}")
        self.txtarea.insert(END, "\n=====================================")
        self.txtarea.insert(END, "\nProduct\t\tQty\tPrice")
        self.txtarea.insert(END, "\n=====================================\n")

        for name, var in self.medical_items() + self.grocery_items() + self.drink_items():
            qty = self.get_qty(var)
            if qty > 0:
                price = qty * self.price_list[name]
                self.txtarea.insert(END, f"{name}\t\t{qty}\t{price:.2f}\n")

        self.txtarea.insert(END, "-------------------------------------\n")
        self.txtarea.insert(END, f"Medical Tax\t\t\t{self.medical_tax.get()}\n")
        self.txtarea.insert(END, f"Grocery Tax\t\t\t{self.grocery_tax.get()}\n")
        self.txtarea.insert(END, f"Cold Drinks Tax\t\t\t{self.cold_drinks_tax.get()}\n")

        total = sum(float(x.get() or 0) for x in [self.medical_price, self.grocery_price, self.cold_drinks_price])
        tax = sum(float(x.get() or 0) for x in [self.medical_tax, self.grocery_tax, self.cold_drinks_tax])

        self.txtarea.insert(END, f"Total Amount\t\t\t{total + tax:.2f}\n")
        self.txtarea.insert(END, "=====================================\n")
        self.txtarea.config(state='disabled')

        self.save_bill_prompt()

    def save_bill_prompt(self):
        if messagebox.askyesno("Save Bill", "Do you want to save the bill?"):
            self.save_bill()
            self.clear_data()

    def save_bill(self):
        try:
            bill_data = self.txtarea.get('1.0', END)
            with open(f"bills/{self.bill_no.get()}.txt", "w") as f:
                f.write(bill_data)
            messagebox.showinfo("Saved", f"Bill No: {self.bill_no.get()} saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {e}")

    def find_bill(self):
        try:
            for file in os.listdir("bills"):
                if file.split('.')[0] == self.search_bill.get():
                    with open(f"bills/{file}", "r") as f:
                        self.txtarea.config(state='normal')
                        self.txtarea.delete('1.0', END)
                        self.txtarea.insert(END, f.read())
                        self.txtarea.config(state='disabled')
                    return
            messagebox.showerror("Error", "Invalid Bill Number")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

    def clear_data(self):
        for var in [self.sanitizer, self.mask, self.hand_gloves, self.dettol, self.newsprin, self.thermal_gun,
                    self.rice, self.food_oil, self.wheat, self.daal, self.flour, self.maggi,
                    self.sprite, self.limka, self.mazza, self.coke, self.fanta, self.mountain_duo,
                    self.medical_price, self.grocery_price, self.cold_drinks_price,
                    self.medical_tax, self.grocery_tax, self.cold_drinks_tax,
                    self.c_name, self.c_phone, self.search_bill]:
            var.set("")
        self.bill_no.set(str(random.randint(1000, 9999)))
        self.welcome_bill()

    def bind_arrow_navigation(self):
        self.entry_list = [w for f in self.root.winfo_children() for w in f.winfo_children() if isinstance(w, Entry)]
        for entry in self.entry_list:
            entry.bind("<Up>", self.focus_previous)
            entry.bind("<Down>", self.focus_next)

    def focus_next(self, event):
        idx = self.entry_list.index(event.widget)
        self.entry_list[(idx + 1) % len(self.entry_list)].focus_set()
        return "break"

    def focus_previous(self, event):
        idx = self.entry_list.index(event.widget)
        self.entry_list[(idx - 1) % len(self.entry_list)].focus_set()
        return "break"

    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            self.root.destroy()


# ✅ Fixed the entry point
if __name__ == "__main__":
    root = Tk()
    app = Bill_App(root)
    root.mainloop()
