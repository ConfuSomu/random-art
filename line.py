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
    
    global size, fname, ftype
    size = {"x": int(x_input.get()), "y": int(y_input.get())}
    
    amount = int(amount_input.get())
    fname = fname_input.get()
    ftype = ftype_input.get()
    lenght = int(lenght_input.get())
    thickness = int(thickness_input.get())
    
    run(amount, brightness, lenght, thickness)

def run(amount, brightness = 255, lenght = 0, thickness = 0): #generate
    #create canvas
    global canvas
    canvas = pygame.display.set_mode([size["x"], size["y"]])
    
    pygame.display.set_caption("Drawing")
    canvas.fill(white)
    
    
    def randLine(surface):
        def randBright():
            c = ["r", "g", "b"]
            
            prim = random.choice(c)#primary color (R, G or B)to set to the specified brightness. This is used to control the brightness
            c.remove(prim) #remove it from the list to not change it again
            edit = random.choice(c) #choose the color to change to an random value (0-255)
            c.remove(edit) #only keep the remaining color and set it to 0
            
            color = {prim: brightness, edit: random.randint(0, brightness), c[0]: 0} #the last color is at 0 brightness to have a secendary[?]/simple color. This should be changed to have more control over the colors.
            print(color) #debug
            print(color["r"], color["g"], color["b"]) #debug
            return [color["r"], color["g"], color["b"]]
        
        def randPos():
            if lenght == 0:
                coords = {"x": random.randrange(0 + x, size["x"]), "y": random.randrange(0 + y, size["y"])} #What will happen if 0+x? (for exemple)
            else:
                #this is similar to randBright()
                cor = ["x", "y"] #coords
                
                edit = random.choice(cor) #select one of coords to give a random lenght
                cor.remove(edit)
                
                coords = {edit: random.randrange(0, size[edit]), cor[0]: lenght}
                print(coords)
                print(coords["x"], coords["y"])
            
            return [coords["x"], coords["y"]]
        
        if thickness == 0:
            nonlocal thickness
            thickness = random.randrange(10, 20)
        
        #start pos
        x = random.randrange(0, size["x"])
        y = random.randrange(0, size["y"])
        end_pos = randPos()
        color = randBright()
        
        pygame.draw.line(canvas, color, [x, y], end_pos, thickness)
        #pygame.draw.circle(canvas, color, [x, y], size, 0)
    
    
    #draw the specified number of times
    for i in range(0, amount):
        randLine(canvas)
    
    #while True:
    pygame.display.flip() #update the display
    
    save_prompt()
    

white = (255,255,255)

app = App(title="Abstract Art - Line", height=550)


Text(app, text="Number of lines:", size=16)
amount_input = TextBox(app, text="500")

Text(app, text="File Saving", size=16)

Text(app, text="Filename with full path:")
fname_input = TextBox(app, text="/home/pi/Desktop/lines", width=20)

Text(app, text="File type:")
ftype_input = Combo(app, options=["png","jpeg","bmp","tga"])

Text(app, text="Advanced", size=16)

Text(app, text="Color brightness (255 is brightest):")
Slider(app, start=0, end=255, command=brightUpdate)

Text(app, text="Line lenght:")
lenght_input = TextBox(app, text="0")
Text(app, text="0 for random lenght", size=8)

Text(app, text="Line thickness:")
thickness_input = TextBox(app, text="8")
Text(app, text="0 for random thickness", size=8)

Text(app, text="Canvas size (x):")
x_input = TextBox(app, text="1092")

Text(app, text="Canvas size (y):")
y_input = TextBox(app, text="749")

Text(app, text="NOTE: After image generation, options to save file will be present\nSizes are in pixels", size=8, color="red")

button = PushButton(app, text="Generate!", command=read)
app.display()
