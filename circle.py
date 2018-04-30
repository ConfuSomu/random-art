import pygame, random, sys
from pygame.locals import *
from guizero import App, PushButton, Text, TextBox, Combo, Slider, yesno, info

def brightUpdate(b): #update circle brightness
    global brightness
    brightness = int(b)

def save_prompt():
    app.destroy() #close the main setup window
    
    if yesno("Save","Save generated drawing?"):
        pygame.image.save(canvas, fname + "." + ftype)
        info("Saved", "Saved drawing (app will be closed)")
        sys.exit(0)
        
    info("Close", "Press OK to close app")
    sys.exit(0)

def read(): #read input data
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

def run(circles, brightness = 255, size = 50): #generate
    #create canvas
    global canvas
    canvas = pygame.display.set_mode([x_size, y_size])
    
    pygame.display.set_caption("Drawing")
    canvas.fill(white)
    
    
    def randCircle(surface):
        def randBright():
            c = ["r", "g", "b"]
            
            prim = random.choice(c)#primary color (R, G or B)to set to the specified brightness. This is used to control the brightness
            c.remove(prim) #remove it from the list to not change it again
            edit = random.choice(c) #choose the color to change to an random value (0-255)
            c.remove(edit) #only keep the remainting color
            
            color = {prim: brightness, edit: random.randint(0, brightness), c[0]: 0} #the last color is at 0 brightness to have a secendary[?]/simple color. This should be changed to have more control over the colors.
            print(color) #debug
            print(color["r"], color["g"], color["b"]) #debug
            return [color["r"], color["g"], color["b"]]
        
        x = random.randrange(0, x_size)#, 0.25)
        y = random.randrange(0, y_size)#, 0.25)
        color = randBright()
        
        pygame.draw.circle(canvas, color, [x, y], size, 0)
    
    
    #draw the specified number of circles
    for i in range(0, circles):
        randCircle(canvas)
    
    #while True:
    pygame.display.flip() #update the display
    
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
Slider(app, start=0, end=255, command=brightUpdate)

Text(app, text="Circle size:")
size_input = TextBox(app, text="50")

Text(app, text="Canvas size (x):")
x_input = TextBox(app, text="1092")

Text(app, text="Canvas size (y):")
y_input = TextBox(app, text="749")

Text(app, text="NOTE: After image generation, options to save file will be present\nSizes are in pixels", size=8, color="red")

button = PushButton(app, text="Generate!", command=read)
app.display()