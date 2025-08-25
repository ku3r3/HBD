import turtle
import random

# Fungsi untuk menggambar kue
def draw_cake():
    turtle.fillcolor("pink")
    turtle.begin_fill()
    turtle.forward(200)
    turtle.left(90)
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(200)
    turtle.left(90)
    turtle.forward(50)
    turtle.left(90)
    turtle.end_fill()

# Fungsi untuk menggambar lilin
def draw_candle(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor("yellow")
    turtle.begin_fill()
    turtle.setheading(90)  # Menghadap ke atas
    turtle.forward(20)  # Tinggi lilin
    turtle.right(90)
    turtle.forward(10)  # Lebar lilin
    turtle.right(90)
    turtle.forward(20)  # Kembali ke bawah
    turtle.right(90)
    turtle.forward(10)  # Kembali ke posisi awal
    turtle.end_fill()

# Fungsi untuk menggambar api
def draw_flame(x, y):
    turtle.penup()
    turtle.goto(x, y + 20)  # Posisi api di atas lilin
    turtle.pendown()
    turtle.fillcolor("orange")
    turtle.begin_fill()
    turtle.circle(5)  # Api berbentuk lingkaran
    turtle.end_fill()

# Fungsi untuk menggambar kue ulang tahun dengan lilin dan api
def draw_birthday_cake():
    turtle.speed(1)
    draw_cake()
    
    # Menggambar beberapa lilin
    for i in range(-80, 100, 40):  # Posisi lilin
        draw_candle(i, 50)
        draw_flame(i, 50)

# Fungsi untuk membuat api berkelip
def flicker_flame():
    for _ in range(10):  # Jumlah kedipan
        turtle.clear()
        draw_birthday_cake()
        if random.choice([True, False]):
            turtle.fillcolor("yellow")
        else:
            turtle.fillcolor("orange")
        turtle.update()
        turtle.delay(200)  # Delay antara kedipan

# Setup turtle
turtle.bgcolor("lightblue")
turtle.title("Kue Ulang Tahun")
turtle.tracer(0)  # Mematikan animasi turtle untuk kecepatan

draw_birthday_cake()
flicker_flame()

turtle.done()
