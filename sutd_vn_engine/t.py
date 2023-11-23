    import turtle

    h, w, s = 20, 20, 10
    dino_rle = [
        "11:w,8:b,1:w",
        "10:w,10:b",
        "10:w,2:b,1:w,7:b",
        "10:w,10:b",
        "10:w,10:b",
        "10:w,10:b",
        "10:w,5:b,5:w",
        "10:w,8:b,2:w",
        "1:b,8:w,5:b,6:w",
        "1:b,7:w,6:b,6:w",
        "2:b,4:w,10:b,4:w",
        "3:b,2:w,9:b,1:w,1:b,4:w",
        "14:b,6:w",
        "14:b,6:w",
        "1:w,12:b,7:w",
        "2:w,11:b,7:w",
    ]

    def draw_pixel(turt, x, y, s=50):
        turt.penup()
        turt.goto(x, y)
        turt.pendown()
        turt.begin_fill()
        for _ in range(4):
            turt.forward(s)
            turt.left(90)
        turt.end_fill()
        turt.penup()

    window = turtle.Screen()
    window.bgcolor("white")

    turt = turtle.Turtle()
    turt.speed(0)

    for y, row in enumerate(dino_rle):
        x = 0
        for cell in row.split(","):
            n, c = cell.split(":")
            if c == "b":
                turt.color("black")
                for _ in range(int(n)):
                    draw_pixel(turt, x * s - 200, h - (y * s) + 200, s)
                    x += 1
            elif c == "w":
                x += int(n)

    window.mainloop()
