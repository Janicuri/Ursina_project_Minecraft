from ursina import *
from time import sleep
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
on = True
blocks = []
positions = []
saved_colors = []
    
dirt = load_texture("assets\Grass_block")
sky = load_texture("assets\sky.png")
bad_sky = load_texture("assets\gg.png")


colors = [color.green,color.lime,color.blue,color.gray,color.red,color.violet,color.rgb(155,118,83)]
curent = color.olive
#rainy_sky = load_texture("assets\rainy_sky.jpg")
class Box(Button):
    def __init__(self, position = (0,0,0),color = color.rgb(155,118,83)):
        self.exists = True
        super().__init__(
            parent = scene,
            texture = dirt,
            color = color,#color.color(0,0,random.uniform(0.9,1)),
            position = position,
            model = "cube",
            origin_y = 0.5,
            scale = 1
        )
    def input(self,key):
        if self.hovered:
            if key == "left mouse down":
                box = Box(position = self.position + mouse.normal,color = curent)
                blocks.append(box)
            if key == "right mouse down":
                self.exists = False
                destroy(self)

a = Audio("assets/rain.mp3",pitch = 1,loop = on,autoplay = True)
a.play()


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "sphere",
            texture = sky,
            scale = 150,
            double_sided = True


        )
class Rsky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "sphere",
            texture = bad_sky,
            scale = 150,
            double_sided = True


        )
        
        
        

def select_color():
    global curent
    if held_keys['1']:
        curent = colors[0]
    if held_keys['2']:
        curent = colors[1]
    if held_keys['3']:
        curent = colors[2]
    if held_keys['4']:
        curent = colors[3]
    if held_keys['5']:
        curent = colors[4]
    if held_keys['6']:
        curent = colors[5]
    if held_keys['7']:
        curent = colors[6]
    if held_keys['m']:
        a.fade_out(duration=4, curve=curve.linear)


def save_position():
    try:
        cwd = os.getcwd()
        file = open(cwd + "/position.txt","w")
        file2 = open(cwd+"/colors.txt","w")
        for i in range(len(blocks)):
            if blocks[i].exists:
                pos = str(int(blocks[i].x))+","+str(int(blocks[i].y))+","+str(int(blocks[i].z))+","
                file.write(str(pos))
                if blocks[i].color == color.green:
                    file2.write("color.green,")
                elif blocks[i].color == color.lime:
                    file2.write("color.lime,")
                elif blocks[i].color == color.blue:
                    file2.write("color.blue,")
                elif blocks[i].color == color.gray:
                    file2.write("color.gray,")
                elif blocks[i].color == color.rgb(155,118,83):
                    file2.write("color.olive,")
                elif blocks[i].color == color.olive:
                    file2.write("color.olive,")
                elif blocks[i].color == color.red:
                    file2.write("color.red,")
                elif blocks[i].color == color.violet:
                    file2.write("color.violet,")
                
        file2.close()
        file.close() 
    except:
        pass



def return_color(col):
    try:
        if col == "color.green":
            return color.green
        elif col == "color.lime":
            return color.lime
        elif col == "color.blue":
            return color.blue
        elif col == "color.gray":
            return color.gray
        elif col == "color.olive":
            return  color.rgb(155,118,83)
        elif col == "color.red":
            return color.red
        elif col == "color.violet":
            return color.violet
    except:
        pass

def die():
    if player.y < -150:
        player.y = 4
        player.x = 2
        player.z = 2
        




def load_position():
    cwd = os.getcwd()
    with open(cwd+"/position.txt","r") as file:
        if file.read() == "":
            file.close()
            return 0
    with open(cwd+"/position.txt","r") as file:
        data = file.read()
        x = ""
        y = ""
        z = ""
        number = 0
        print(data)
        for i in data:
            if i != ",":
                try:
                    
                    if number == 0:
                        x += str(int(i))
                    elif number == 1:
                    
                        y += str(int(i))
                             
                    elif number == 2:
                        z += str(int(i))
                        x = int(x)
                        y = int(y)
                        z = int(z)
                        positions.append((x,y,z))
                        number = -1
                        x = ""
                        y = ""
                        z = ""
                except:
                    pass
            else:
                number +=1
        file.close()
        couleurs = open(cwd+"/colors.txt","r")
        data = couleurs.read()
        temp = ""
        for i in data:
            if i == ",":
                saved_colors.append(temp)
                temp = ""
            else :
                temp += i
        couleurs.close()
    for i in range(len(positions)):
        #print(len(positions),len(saved_colors))
        box = Box(positions[i],color=return_color(saved_colors[i]))
        blocks.append(box)





def create_field():
    if len(blocks) == 0 :
        for i in range(10):
            for j in range (10):
                box = Box(position = (i,0,j))
                blocks.append(box)
                print(box.position)

load_position()

def update():
    select_color()
    save_position()
    die()
    
        

create_field()
player = FirstPersonController()
player.cursor.color = color.black
skydrive = Rsky()

app.run()
