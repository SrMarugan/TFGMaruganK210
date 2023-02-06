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
Burn the model face_model_at_0x300000.kfpkg using kflash select the addres 0x300000. Then in the MaixPy IDE load the code machine_vision\face_find/demo_find_face.py

![Capture2](https://user-images.githubusercontent.com/115635629/217023982-c20c48a7-bcad-42c7-a704-a8c3404bcfcb.png)

We see that the code execute the model of face recognition, and identify by the camera if there are somebody. When it recognize somebody it puts a white rectangle around the face. We can see an example in the last capture.

I edit that code to count the number of persons that are in the snapshot. Then it prints the number of persons in the image of the LCD. To make it we put a counter in the function that puts the rectangle in the people. Then we evaluate what number of persons are, if there is anybody we show "There are no persons", if there is somebody we show "1 person" and if there are more tha 1 person we show the exact number. We puts some conditionals to evaluate the number of persons to doing the code less dumb.

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


Also I put a 8 segment to see that number in a board that doesn't have a LCD. You can see this code in the repository.

To code the 8 segment we have to use the GPIO of the board. With the dependencies of function fpio_manager we import fm. Now we can change the differents pins to use as GPIO or others protocols as I2C, SPI, I2S, or UART. Very interesting to communicate with other devices.
