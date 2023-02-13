# TFGMaruganK210

Download and install the most recent version of MaixPy IDE
https://dl.sipeed.com/shareURL/MAIX/MaixPy/ide/v0.2.5

Download kflash to burn the models that use the AI and that controls from MaixPy to the Sipeed boards
https://github.com/sipeed/kflash_gui/releases

We have to download the IDE of MaixPy and kflash to our operative system, also we have to download the most recent versions. In my case they are maixpy-ide-windows-0.2.5 to Windows and kflash_gui_v1.8.1 also to Windows.

The tool of MaixPy loads the writing code in micropython to the board, and kflash loads on board memory the controller to communicate with MaixPy also the models training of our AI.

Download the model .bin that controls the K210 board with the IDE
https://dl.sipeed.com/shareURL/MAIX/MaixPy/release/master/maixpy_v0.6.2_84_g8fcd84a58

Now we can start burning the model .bin into the board. Open kflash_gui. Select the model .bin and charge in addr 0x00000. In board settings select your board (auto detect the board automatically) and burn to flash. Then select the port and the baudrate into 1500000.

![image](https://user-images.githubusercontent.com/115635629/217003260-f04346dc-c9fd-4cae-bce5-c31b026b78bb.png)

Click in download and wait

![image](https://user-images.githubusercontent.com/115635629/217004082-42807d74-c48b-48f3-9451-c2cd5e5ae482.png)

Open the MaixPy IDE. In Tools>SelectBoard select the board that you have. Then click into the green clip and select the port where the board is. Then you are connected with the board, now you can load the example code helloworld.py. Open the example that MaixPy brings, go to Archive>Examples>01-Basics>helloworld.py Execute the code and you can see the camera image in your IDE

![Capture](https://user-images.githubusercontent.com/115635629/217007197-ea818108-5eae-42f0-ba6c-f7385d465b9f.png)

If you can't see any image here are some tips:
- Connect your board with a USB-C cable and connect it in a USB 3.0 port
- Connect your board directly with the motherboard (behind the PC) don't connect in the PC box
- View if your board has the correct port, probably you charge the code into other device
- View if the camera sensor is ok, probably don't work or it's not focus correctly (you can rotate the len to focus correctly)

MaixPy has some models and codes that you can use to prove your board. You can download from the github of MaixPy https://github.com/sipeed/MaixPy_scripts
If you download that examples I recommend save it in the directory Documents/MaixPy

![image](https://user-images.githubusercontent.com/115635629/217012406-ffa386a0-35c2-48a2-87be-88f9e23e40f7.png)

Now if we go to machine_vision/models we can find three models that we can burn into the board

# Find Face
Burn the model face_model_at_0x300000.kfpkg using kflash, select the addres 0x300000. Then in the MaixPy IDE load the code machine_vision\face_find/demo_find_face.py

![Capture2](https://user-images.githubusercontent.com/115635629/217023982-c20c48a7-bcad-42c7-a704-a8c3404bcfcb.png)

We see that the code execute the model of face recognition, and identify by the camera if there are somebody. When it recognize somebody it puts a white rectangle around the face. We can see an example in the last capture.

I edit that code to count the number of persons that are in the snapshot. Then it prints the number of persons in the image of the LCD. To make it we put a counter in the function that puts the rectangle in the people. Then we evaluate what number of persons are, if there is anybody we show "There are no persons", if there is somebody we show "1 person" and if there are more than 1 person we show the exact number. We puts some conditionals to evaluate the number of persons to doing the code less dumb.

```
if objects:
  for obj in objects:
  img.draw_rectangle(obj.rect())
  per += 1
if per == 0:
  img=img.draw_string(10, 10, "No person", scale=2)
if per == 1:
  img=img.draw_string(10, 10, "1 person", scale=2)
if per > 1:
  img=img.draw_string(10, 10, "Persons: %d" %(per), scale=2)
```

![image](https://user-images.githubusercontent.com/115635629/217075340-3dc93bed-5872-4957-a726-68cd609fc411.png)

Here is an example of how the IA knows the number of persons and show us. The entire code is in the repository as **count_persons.py** Know we can experiment with some different images or make more things. I show you what I do in my TFG and I explain how did I get it. 

# 8 Segment and FPIO Manager

I put a 8 segment to see that number in a board that doesn't have a LCD. Can see in the image a 8 segment display in a Sipeed Maix Bit board.

![Display](https://user-images.githubusercontent.com/115635629/217081788-0071a141-a736-4fd1-8a7a-58187344ad06.jpg)


To code the 8 segment we have to use the GPIO of the board. FPIOA (Field Programmable Input and Output Array) make a mapping of the physical pins into a type of pin we want to use, for example the traditional GPIO (General Purpose Input Output) or his varient GPIOHS (GPIO High Speed). Using the dependencies from fpio_manager we import fm, to this form we can change the differents pins to use as GPIO or others protocols as I2C, SPI, I2S, or UART, all of them very interesting to communicate with other devices. 

If we want to make the pin 33 into a normal GPIO to put a LED we have to include the dependencies from fpio_manager as we can see in this example code.

```
from fpioa_manager import fm

fm.register(33,fm.fpioa.GPIO1)
led = GPIO(GPIO.GPIO1,GPIO.OUT)
```

In a 8 segment display every segment is like an individual LED, we program each number like a combination of ON and OFF LEDs. Then when we recognise the number of persons with the previous code we can select the correspondent segments ON and OFF to show us the number of persons. 

The Sipeed Maix Bit don't need a LCD if we only wants to know the number of persons that are in the area of the camera sensor. The entire code are in the repository as **count_persons_display.py**

If you want to learn more about the fpioa you can consult the API Reference page of Sipeed https://wiki.sipeed.com/soft/maixpy/en/api_reference/Maix/fpioa.html It's important read the documentation first, because there are pins reserved, like the camera and LCD, or busy by others. Also we have an Appendix with a peripheral table that shows us the differents peripheral functions and his name.

# Arduino and ESP32 (Wi-Fi)
Now we use Arduino to use an antenna Wi-Fi. Why don't use MaixPy IDE? Because don't work the libraries and I prove in Arduino and works perfectly, but it's more difficult and we have to configure well our ArduinoIDE to work correctly.

First of all download and install the ArduinoIDE from https://www.arduino.cc/en/software

We have to install the libraries and configure the IDE to admit the Sipeed boards
* Open ArduinoIDE, select **File** -> **Preferences**
* Add in **Additional Boards Manager URLs**: http://dl.sipeed.com/MAIX/Maixduino/package_Maixduino_k210_index.json
* Select **Tools** -> **Board** -> **Boards Manager**, search Maixduino, click Install
* When we click on **Board** it has to be multiple boards of Sipeed

![image](https://user-images.githubusercontent.com/115635629/218576978-9829c8b6-0a3f-408e-b387-67f3e0947d76.png)

![image](https://user-images.githubusercontent.com/115635629/218577115-9b14701d-daee-4785-8186-0b64d0bb06c5.png)

We have to change board settings to:
* Board: Sipeed Maix Go Board
* Burn Tool Firmware: open-ec
* Burn Baud Rate: 2Mbps
* Port: We select the connected board’s port
* Programmer: k-flash

![image](https://user-images.githubusercontent.com/115635629/218577675-25529f55-de8c-4328-ab10-7f54982a3b0c.png)

We need a Sipeed board that have the WiFi antenna, in my case I have the kit of Sipeed Maix Go, with a LCD, an antenna and a little battery. Actually it's impossible acquire one, I hope in the future we can buy someone

![imagen](https://user-images.githubusercontent.com/115635629/217246419-f917bd4f-a845-4562-9a93-532121ce01c1.png)
