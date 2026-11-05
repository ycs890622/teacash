from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import csv
import os
from datetime import datetime

# 销售记录文件
SALE_FILE = "sales.csv"
# 商品库
goods_list = [
    {"name": "九月黄秋茶", "price": 180},
    {"name": "绿茶", "price": 120},
    {"name": "红茶", "price": 150},
    {"name": "茶叶礼盒", "price": 260},
    {"name": "香烟", "price": 25},
    {"name": "饮料", "price": 5},
    {"name": "茶具", "price": 88},
    {"name": "茶样", "price": 10},
]

class CashierLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 8
        self.padding = 10
        self.cart = []

        # 标题
        title = Label(text="茶叶收银系统", font_size=32, size_hint_y=0.08)
        self.add_widget(title)

        # 商品区域
        goods_box = GridLayout(cols=4, spacing=6, size_hint_y=0.35)
        for g in goods_list:
            btn = Button(text=f"{g['name']}\n{g['price']}元", font_size=16)
            btn.bind(on_press=lambda x, gd=g: self.add_goods(gd))
            goods_box.add_widget(btn)
        self.add_widget(goods_box)

        # 购物车
        self.cart_label = Label(text="购物车：\n", size_hint_y=0.3, font_size=18)
        scroll = ScrollView(size_hint_y=0.3)
        scroll.add_widget(self.cart_label)
        self.add_widget(scroll)

        # 金额行
        money_box = BoxLayout(size_hint_y=0.12, spacing=10)
        money_box.add_widget(Label(text="应收：", font_size=20))
        self.total_label = Label(text="0.00", font_size=20)
        money_box.add_widget(self.total_label)
        money_box.add_widget(Label(text="实付：", font_size=20))
        self.pay_input = TextInput(text="", input_filter="float", font_size=20, halign="center")
        money_box.add_widget(self.pay_input)
        money_box.add_widget(Label(text="找零：", font_size=20))
        self.change_label = Label(text="0.00", font_size=20)
        money_box.add_widget(self.change_label)
        self.add_widget(money_box)

        # 按钮行
        btn_box = BoxLayout(size_hint_y=0.15, spacing=8)
        btn_calc = Button(text="计算找零", font_size=20)
        btn_calc.bind(on_press=self.calc_change)
        btn_pay = Button(text="收款保存", font_size=20, background_color=(0.2,0.7,0.2,1))
        btn_pay.bind(on_press=self.save_sale)
        btn_clear = Button(text="清空购物车", font_size=20, background_color=(0.8,0.2,0.2,1))
        btn_clear.bind(on_press=self.clear_cart)
        btn_credit = Button(text="赊账", font_size=20, background_color=(0.8,0.7,0.1,1))
        btn_credit.bind(on_press=self.credit_sale)
        btn_box.add_widget(btn_calc)
        btn_box.add_widget(btn_pay)
        btn_box.add_widget(btn_clear)
        btn_box.add_widget(btn_credit)
        self.add_widget(btn_box)

    def add_goods(self, goods):
        self.cart.append(goods)
        self.refresh_cart()

    def refresh_cart(self):
        text = ""
        total = 0
        for item in self.cart:
            text += f"{item['name']}  {item['price']}元\n"
            total += item["price"]
        self.cart_label.text = text
        self.total_label.text = f"{total:.2f}"
        self.change_label.text = "0.00"
        self.pay_input.text = ""

    def calc_change(self, instance):
        try:
            total = float(self.total_label.text)
            pay = float(self.pay_input.text)
            change = pay - total
            if change < 0:
                self.change_label.text = "钱不够！"
            else:
                self.change_label.text = f"{change:.2f}"
        except:
            self.change_label.text = "输入金额"

    def save_sale(self, instance):
        if not self.cart:
            return
        total = float(self.total_label.text)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        goods_name = ",".join([i["name"] for i in self.cart])
        with open(SALE_FILE, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow([now, goods_name, total, "正常收款"])
        self.clear_cart()

    def credit_sale(self, instance):
        if not self.cart:
            return
        total = float(self.total_label.text)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        goods_name = ",".join([i["name"] for i in self.cart])
        with open(SALE_FILE, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow([now, goods_name, total, "赊账"])
        self.clear_cart()

    def clear_cart(self, instance):
        self.cart = []
        self.refresh_cart()

class TeaCashApp(App):
    def build(self):
        Window.orientation = "portrait"
        return CashierLayout()

if __name__ == "__main__":
    if not os.path.exists(SALE_FILE):
        with open(SALE_FILE, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["时间","商品","金额","类型"])
    TeaCashApp().run()
