from kivy.clock import Clock  # for changing screens
from kivy.lang import Builder  # for camera
from kivy.uix.button import Button  # for buttons
from kivy.uix.camera import Camera
from kivy.uix.image import Image  # for images
from kivy.uix.label import Label  # for labels
from kivy.uix.filechooser import FileChooserListView  # for selecting photo from files in a device
from kivy.uix.image import AsyncImage  # for images in the background
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition  # for changing screens
from kivy.app import App  # for developing an app
import time
import shutil  # for copy an image instead of moving it
import os  # for using the operating system

# from yolov5.custom_yolo import DetectClass

Builder.load_string('''
<CameraScreen>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 640)
        play: True
    RoundedButton:
        text: 'Take Picture'
        color: '#04c9a3'
        bold: True
        pos_hint: {'center_x': 0.5, 'center_y': 0.18}
        size_hint: (0.2, 0.08)
        on_press: root.capture_image()
    RoundedButton:
        text: 'Rotate Camera'
        color: '#04c9a3'
        bold: True
        pos_hint: {'center_x': 0.5, 'center_y': 0.08}
        size_hint: (0.2, 0.08)
        on_press: root.rotate_camera()
          
<RoundedButton@Button>
    background_color: (0, 0, 0, 0)
    background_normal: ''
    canvas.before:
        Color:
            rgba: (0.05, 0.45, 0.35, 0.8) # color of button
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [40] 
''')

flag = 0  # flag to change screens
class_of_image = 0  # classification of the photo
current_image_filename = ""  # name for the selected image


class StartScreen(Screen):  # opening screen
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo1_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.opening = Label(text="Hello", font_size=20, bold=True, color='#04c9a3', size_hint=(0.5, 0.1),
                             pos_hint={'center_x': 0.5, 'center_y': 0.39})
        self.label = Label(text="Please enter one product at a time", bold=True, font_size=20, color='#046b57',
                           size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})
        self.button1 = Button(text='lets start', font_size=20, color='#04c7a1', bold=True,
                              background_color='#00FFCE', size_hint=(0.4, 0.1),
                              pos_hint={'center_x': 0.5, 'center_y': 0.25})
        self.button1.bind(on_press=self.changeFlag)
        self.add_widget(self.background)
        self.add_widget(self.opening)
        self.add_widget(self.label)
        self.add_widget(self.button1)

    def changeFlag(self, *args):  # change to main screen
        global flag, class_of_image
        flag = 1


class MainScreen(Screen):  # main screen  (flag = 1)
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source="Images\\logo2_2.jpeg",
                                     allow_stretch=True, keep_ratio=False)
        self.Label1 = Label(text="Take a picture", font_size=20, bold=True, color='#046b57',
                            size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.72})
        self.button1 = Button(background_normal='Images\\camera.jpeg', size_hint=(0.38, 0.18),
                              pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.button1.bind(on_press=self.changeFlag)
        self.Label2 = Label(text="picture from gallery", font_size=20, bold=True, color='#046b57',
                            size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.42})
        self.button2 = Button(background_normal='Images\\gallery.jpeg', size_hint=(0.38, 0.18),
                              pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.button2.bind(on_press=self.changeFlag1)
        self.add_widget(self.background)
        self.add_widget(self.Label1)
        self.add_widget(self.button1)
        self.add_widget(self.Label2)
        self.add_widget(self.button2)

    def changeFlag(self, *args):  # chang screen to cameraScreen
        # before the screen change the program checks if there is a pic named "image.png", if there is then delete it
        if current_image_filename != "":
            if os.path.exists(f"{current_image_filename}"):
                os.remove(f"{current_image_filename}")
                print("photo deleted")  # self check
            else:
                print("can't find photo")
        global flag
        flag = 2  # chang screen to cameraScreen

    def changeFlag1(self, *args):  # change screen to choose a picture from gallery
        # before the screen change the program checks if there is a pic named "image.png", if there is then delete it
        if current_image_filename != "":
            os.remove(f"{current_image_filename}")
            print("photo deleted")  # self check
        else:
            print("can't find photo")
        global flag
        flag = 3  # change screen to choose a picture from gallery


class CameraScreen(Screen):  # camera screen  (flag = 2)
    def capture_image(self):  # take a picture
        global current_image_filename
        camera = self.ids.camera
        timestamp = str(int(time.time()))  # Generate a unique timestamp
        current_image_filename = f"image_{timestamp}.png"  # Save image with unique filename
        camera.export_to_png(current_image_filename)
        # camera = self.ids.camera
        # if os.path.exists("image.png"):
        #     os.remove("image.png")
        # camera.export_to_png("image.png")
        print("Image captured!")  # self check
        global flag
        flag = 4   # chang screen to Image screen

    def rotate_camera(self):   # rotate camera  front <=> back
        camera = self.ids.camera
        camera.play = False  # stop the camera
        camera.resolution = (camera.resolution[1], camera.resolution[0])  # change the cameras
        camera.play = True  # reopen the camera


class FileChooserScreen(Screen):  # Choose picture from files screen  (flag = 3)
    def __init__(self, **kwargs):
        super(FileChooserScreen, self).__init__(**kwargs)
        self.file_chooser = FileChooserListView()  # open files in the device
        self.file_chooser.bind(on_submit=self.load_selected)  # chooses a picture
        self.add_widget(self.file_chooser)

    def load_selected(self, instance, value, *args):  # chooses a picture
        if value:
            chosen_image_path = value[0]  # path of the selected picture
            timestamp = str(int(time.time()))  # Generate a unique timestamp
            global current_image_filename
            current_image_filename = f"image_{timestamp}.png"  # New unique filename
            # new_image_path = "image.png"  # path and name that picture needs to be
            shutil.copy(chosen_image_path, current_image_filename)  # copy the name and path to the selected picture
            # os.rename(chosen_image_path, new_image_path)  # not good, move the pic to app and not copy
            global flag
            flag = 4   # chang screen to Image screen


class PhotoScreen(Screen):  # show the selected picture to classify and classify  (flag = 4)
    def __init__(self, **kwargs):
        super(PhotoScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.photo = Image(size_hint=(0.8, 0.82), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                           allow_stretch=False, keep_ratio=False)
        self.back_button = Button(text="Back", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.3, 0.1), pos_hint={'x': 0.18, 'y': 0.09})
        self.back_button.bind(on_press=self.changeFlag)
        self.continue_button = Button(text="Next", font_size=20, color='#04c7a1', bold=True,
                                      background_color='#00FFCE', size_hint=(0.3, 0.1), pos_hint={'x': 0.52, 'y': 0.09})
        self.continue_button.bind(on_press=self.image_to_yolo)
        self.add_widget(self.background)
        self.add_widget(self.photo)
        self.add_widget(self.back_button)
        self.add_widget(self.continue_button)

    def on_enter(self):
        self.photo.source = ''  # Clear the previous image
        self.photo.source = current_image_filename  # Display the current image

    def changeFlag(self, *args):  # chang screen to main screen
        global flag
        flag = 1

    def image_to_yolo(self, ds, *args):  # classify the selected picture with yolov5
        global flag, class_of_image
        # detection command for yolov5
        os.system(f"python yolov5/detect.py --source {current_image_filename} --weights yolov5/custom_yolo/best.pt --img-size 416 --conf 0.4 --save-txt --exist-ok --nosave")
        base_name, extension = os.path.splitext(current_image_filename)
        label_path = f'yolov5\\runs\\detect\\exp\\labels\\{base_name}.txt'
        content = []
        with open(label_path, 'r') as file:
            content = file.read()
        class_of_image = int(content[0])
        os.remove(label_path)
        print(class_of_image)  # self check
        time.sleep(1)
        flag = 5


class BatteryScreen(Screen):  # battery -> electronics bin  (flag = 5 & class_of_image = 0)
    def __init__(self, **kwargs):
        super(BatteryScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.bin = Image(source="Images\\BatteryBin.jpg", size_hint=(0.7, 0.55), pos_hint={'x': 0.1, 'y': 0.2},
                         allow_stretch=True, keep_ratio=False)
        self.classification_label = Label(text="Batteries recycling bin",
                                          color='#192e29', font_size=20, size_hint=(None, None), bold=True,
                                          pos_hint={'x': 0.4, 'y': 0.8})
        self.add_widget(self.background)
        self.add_widget(self.bin)
        self.add_widget(self.classification_label)
        self.button = Button(text="recycle \n more", font_size=20, color='#04c7a1', bold=True,
                             background_color='#00FFCE', size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.3, 'center_y': 0.1})
        self.button.bind(on_press=self.changeFlag)
        self.add_widget(self.button)
        self.exit_button = Button(text="Exit", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.2, 0.1),
                                  pos_hint={'center_x': 0.7, 'center_y': 0.1})
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def exit_app(self, *args):  # close the app
        App.get_running_app().stop()

    def changeFlag(self, *args):
        global flag  # change screen to main screen
        flag = 1


class PurpleScreen(Screen):  # glass -> purple bin  (flag = 5 & class_of_image = 1,8,11)
    def __init__(self, **kwargs):
        super(PurpleScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.bin = Image(source="Images\\PurpleRecyclingBin.jpg", size_hint=(0.7, 0.55), pos_hint={'x': 0.1, 'y': 0.2},
                         allow_stretch=True, keep_ratio=False)
        self.classification_label = Label(text="Purple recycling bin",
                                          color='#192e29', font_size=20, size_hint=(None, None), bold=True,
                                          pos_hint={'x': 0.4, 'y': 0.8})
        self.add_widget(self.background)
        self.add_widget(self.bin)
        self.add_widget(self.classification_label)
        self.button = Button(text="recycle \n more", font_size=20, color='#04c7a1', bold=True,
                             background_color='#00FFCE', size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.3, 'center_y': 0.1})
        self.button.bind(on_press=self.changeFlag)
        self.add_widget(self.button)
        self.exit_button = Button(text="Exit", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.2, 0.1),
                                  pos_hint={'center_x': 0.7, 'center_y': 0.1})
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def exit_app(self, *args):  # close the app
        App.get_running_app().stop()

    def changeFlag(self, *args):
        global flag  # change screen to main screen
        flag = 1


class ClothesScreen(Screen):  # clothes and shoes -> clothes bin  (flag = 5 & class_of_image = 2,10)
    def __init__(self, **kwargs):
        super(ClothesScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.bin = Image(source="Images\\ClothesShoesBin.jpg", size_hint=(0.7, 0.55), pos_hint={'x': 0.1, 'y': 0.2},
                         allow_stretch=True, keep_ratio=False)
        self.classification_label = Label(text="Clothes recycling bin",
                                          color='#192e29', font_size=20, size_hint=(None, None), bold=True,
                                          pos_hint={'x': 0.4, 'y': 0.8})
        self.add_widget(self.background)
        self.add_widget(self.bin)
        self.add_widget(self.classification_label)
        self.button = Button(text="recycle \n more", font_size=20, color='#04c7a1', bold=True,
                             background_color='#00FFCE', size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.3, 'center_y': 0.1})
        self.button.bind(on_press=self.changeFlag)
        self.add_widget(self.button)
        self.exit_button = Button(text="Exit", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.2, 0.1),
                                  pos_hint={'center_x': 0.7, 'center_y': 0.1})
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def exit_app(self, *args):  # close the app
        App.get_running_app().stop()

    def changeFlag(self, *args):
        global flag  # change screen to main screen
        flag = 1


class OrangeScreen(Screen):  # metal and plastic -> orange bin (flag = 5 & class_of_image = 3,4)
    def __init__(self, **kwargs):
        super(OrangeScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.bin = Image(source="Images\\OrangeRecyclingBin.jpg", size_hint=(0.7, 0.55), pos_hint={'x': 0.1, 'y': 0.2},
                         allow_stretch=True, keep_ratio=False)
        self.classification_label = Label(text="Orange recycling bin",
                                          color='#192e29', font_size=20, size_hint=(None, None), bold=True,
                                          pos_hint={'x': 0.4, 'y': 0.8})
        self.add_widget(self.background)
        self.add_widget(self.bin)
        self.add_widget(self.classification_label)
        self.button = Button(text="recycle \n more", font_size=20, color='#04c7a1', bold=True,
                             background_color='#00FFCE', size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.3, 'center_y': 0.1})
        self.button.bind(on_press=self.changeFlag)
        self.add_widget(self.button)
        self.exit_button = Button(text="Exit", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.2, 0.1),
                                  pos_hint={'center_x': 0.7, 'center_y': 0.1})
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def exit_app(self, *args):  # close the app
        App.get_running_app().stop()

    def changeFlag(self, *args):
        global flag  # change screen to main screen
        flag = 1


class BlueScreen(Screen):  # paper and cardboard -> blue bin  (flag = 5 & class_of_image = 7,9)
    def __init__(self, **kwargs):
        super(BlueScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.bin = Image(source="Images\\BlueRecyclingBin.jpg", size_hint=(0.7, 0.55), pos_hint={'x': 0.1, 'y': 0.2},
                         allow_stretch=True, keep_ratio=False)
        self.classification_label = Label(text="Blue recycling bin",
                                          color='#192e29', font_size=20, size_hint=(None, None), bold=True,
                                          pos_hint={'x': 0.4, 'y': 0.8})
        self.add_widget(self.background)
        self.add_widget(self.bin)
        self.add_widget(self.classification_label)
        self.button = Button(text="recycle \n more", font_size=20, color='#04c7a1', bold=True,
                             background_color='#00FFCE', size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.3, 'center_y': 0.1})
        self.button.bind(on_press=self.changeFlag)
        self.add_widget(self.button)
        self.exit_button = Button(text="Exit", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.2, 0.1),
                                  pos_hint={'center_x': 0.7, 'center_y': 0.1})
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def exit_app(self, *args):  # close the app
        App.get_running_app().stop()

    def changeFlag(self, *args):
        global flag  # change screen to main screen
        flag = 1


class BottleScreen(Screen):  # bottles -> bottles bin  (flag = 5 & class_of_image = 12)
    def __init__(self, **kwargs):
        super(BottleScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.bin = Image(source="Images\\BottlesRecyclingBin.jpg", size_hint=(0.7, 0.55), pos_hint={'x': 0.1, 'y': 0.2},
                         allow_stretch=True, keep_ratio=False)
        self.classification_label = Label(text="Can be recycled at supermarkets",
                                          color='#192e29', font_size=20, size_hint=(None, None), bold=True,
                                          pos_hint={'x': 0.4, 'y': 0.8})
        self.add_widget(self.background)
        self.add_widget(self.bin)
        self.add_widget(self.classification_label)
        self.button = Button(text="recycle \n more", font_size=20, color='#04c7a1', bold=True,
                             background_color='#00FFCE', size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.3, 'center_y': 0.1})
        self.button.bind(on_press=self.changeFlag)
        self.add_widget(self.button)
        self.exit_button = Button(text="Exit", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.2, 0.1),
                                  pos_hint={'center_x': 0.7, 'center_y': 0.1})
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def exit_app(self, *args):  # close the app
        App.get_running_app().stop()

    def changeFlag(self, *args):
        global flag  # change screen to main screen
        flag = 1


class GreenScreen(Screen):  # trash and biological -> green bin  (flag = 5 & class_of_image = 5,6)
    def __init__(self, **kwargs):
        super(GreenScreen, self).__init__(**kwargs)
        self.background = AsyncImage(source='Images\\logo2_2.jpeg', allow_stretch=True, keep_ratio=False)
        self.bin = Image(source="Images\\GreenBin.jpg", size_hint=(0.7, 0.55), pos_hint={'x': 0.1, 'y': 0.2},
                         allow_stretch=True, keep_ratio=False)
        self.classification_label = Label(text="Green recycling bin",
                                          color='#192e29', font_size=20, size_hint=(None, None), bold=True,
                                          pos_hint={'x': 0.4, 'y': 0.8})
        self.add_widget(self.background)
        self.add_widget(self.bin)
        self.add_widget(self.classification_label)
        self.button = Button(text="recycle \n more", font_size=20, color='#04c7a1', bold=True,
                             background_color='#00FFCE', size_hint=(0.3, 0.1),
                             pos_hint={'center_x': 0.25, 'center_y': 0.1})
        self.button.bind(on_press=self.changeFlag)
        self.add_widget(self.button)
        self.exit_button = Button(text="Exit", font_size=20, color='#04c7a1', bold=True,
                                  background_color='#00FFCE', size_hint=(0.3, 0.1),
                                  pos_hint={'center_x': 0.75, 'center_y': 0.1})
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def exit_app(self, *args):  # close the app
        App.get_running_app().stop()

    def changeFlag(self, *args):
        global flag  # change screen to main screen
        flag = 1


class RecyclingApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(StartScreen(name='start_screen'))
        sm.add_widget(MainScreen(name='main_Screen'))
        sm.add_widget(CameraScreen(name='camera_screen'))
        sm.add_widget(FileChooserScreen(name='choose_a_picture'))
        sm.add_widget(PhotoScreen(name='photo_to_classify'))
        # bin screens:
        sm.add_widget(BatteryScreen(name='battery_screen'))
        sm.add_widget(PurpleScreen(name='purple_Screen'))
        sm.add_widget(ClothesScreen(name='clothes_screen'))
        sm.add_widget(OrangeScreen(name='orange_screen'))
        sm.add_widget(BlueScreen(name='blue_screen'))
        sm.add_widget(BottleScreen(name='bottle_screen'))
        sm.add_widget(GreenScreen(name='green_screen'))
        Clock.schedule_interval(self.check_flag, 1)  # Check the flag every second to change the screens
        return sm

    def check_flag(self, dt):  # func to change the screens
        if flag == 1:
            self.root.current = 'main_Screen'
        elif flag == 2:
            self.root.current = 'camera_screen'
        elif flag == 3:
            self.root.current = 'choose_a_picture'
        elif flag == 4:
            self.root.current = 'photo_to_classify'
        elif flag == 5:
            global class_of_image
            if class_of_image == 0:
                self.root.current = 'battery_screen'
            elif class_of_image in [1, 8, 11]:
                self.root.current = 'purple_Screen'
            elif class_of_image in [2, 10]:
                self.root.current = 'clothes_screen'
            elif class_of_image in [3, 4]:
                self.root.current = 'orange_screen'
            elif class_of_image in [7, 9]:
                self.root.current = 'blue_screen'
            elif class_of_image == 12:
                self.root.current = 'bottle_screen'
            else:
                self.root.current = 'green_screen'


if __name__ == '__main__':
    RecyclingApp().run()
