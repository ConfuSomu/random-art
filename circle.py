import pygame, random, sys
from pygame.locals import *
from guizero import App, PushButton, Text, TextBox, Combo, Slider, yesno, info

def sliUpd(b):
    global brightness
    brightness = int(b)

def save_prompt():
    app.destroy()
    
    if yesno("Save","Save generated drawing?"):
        pygame.image.save(screen, fname + "." + ftype)
        info("Saved", "Saved drawing (app will be closed)")
        sys.exit(0)
        
    info("Close", "Press OK to close app")
    sys.exit(0)

def gen():
    button.disable()
    button.set_text("Generating...")
    app.set_title("Generating drawing...")
    
    global x_size, y_size,fname, ftype
    
    circles = int(circles_input.get())
    fname = fname_input.get()
    ftype = ftype_input.get()
    size = int(size_input.get())
    x_size = int(x_input.get())
    y_size = int(y_input.get())
    
    run(circles, brightness, size)

def run(circles, brightness = 255, size = 50):
    global screen
    screen = pygame.display.set_mode([x_size, y_size])
    
    pygame.display.set_caption("Drawing")
    screen.fill(white)
    
    
    def randCircle(surface):
        def randBright():
            c = ["r", "g", "b"]
            
            prim = random.choice(c)#primary color (R, G or B)to set to 255
            c.remove(prim) #remove it from the list to not change it by accident
            edit = random.choice(c) #choose the color to change to an random value (0-255)
            c.remove(edit) #only keep the remainting color
            
            color = {prim: brightness, edit: random.randint(0, brightness), c[0]: 0} #brightness = 255 for bright colors
            print(color) #debug
            print(color["r"], color["g"], color["b"]) #debug
            return [color["r"], color["g"], color["b"]]
        
        x = random.randrange(0, x_size)#, 0.25)
        y = random.randrange(0, y_size)#, 0.25)
        color = randBright()
        
        pygame.draw.circle(screen, color, [x, y], size, 0)
    
    
    #pygame.draw.circle(screen, [111, 33, 33], [500, 500], 50, 0)
    for i in range(0, circles):
        randCircle(screen)
    
    #while True:
    pygame.display.flip()
    
    save_prompt()
    

white = (255,255,255)

app = App(title="Abstract Art - Circle")


Text(app, text="Number of circles:", size=16)
circles_input = TextBox(app, text="500")

Text(app, text="File Saving", size=16)

Text(app, text="Filename with full path:")
fname_input = TextBox(app, text="/home/pi/Desktop/circle", width=20)

Text(app, text="File type:")
ftype_input = Combo(app, options=["png","jpeg","bmp","tga"])

Text(app, text="Advanced", size=16)

Text(app, text="Color brightness (255 is brightest):")
Slider(app, start=0, end=255, command=sliUpd)

Text(app, text="Circle size:")
size_input = TextBox(app, text="50")

Text(app, text="Screen size (x):")
x_input = TextBox(app, text="1092")

Text(app, text="Screen size (y):")
y_input = TextBox(app, text="749")

Text(app, text="NOTE: After image generation, options to save file will be present\nSizes are in pixels", size=8, color="red")

button = PushButton(app, text="Generate!", command=gen)
app.display()