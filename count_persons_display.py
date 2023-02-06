import sensor, image, lcd, time
import KPU as kpu
import gc, sys
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=(224,224))
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

def mostrar(per):

        fm.register(33,fm.fpioa.GPIO1)
        led_A = GPIO(GPIO.GPIO1,GPIO.OUT)
        fm.register(32,fm.fpioa.GPIO0)
        led_B = GPIO(GPIO.GPIO0,GPIO.OUT)
        fm.register(2,fm.fpioa.GPIO5)
        led_C = GPIO(GPIO.GPIO5,GPIO.OUT)
        fm.register(1,fm.fpioa.GPIO6)
        led_D = GPIO(GPIO.GPIO6,GPIO.OUT)
        fm.register(0,fm.fpioa.GPIO7)
        led_E = GPIO(GPIO.GPIO7,GPIO.OUT)
        fm.register(34,fm.fpioa.GPIO2)
        led_F = GPIO(GPIO.GPIO2,GPIO.OUT)
        fm.register(35,fm.fpioa.GPIO3)
        led_G = GPIO(GPIO.GPIO3,GPIO.OUT)
        fm.register(3,fm.fpioa.GPIO4)
        led_DP = GPIO(GPIO.GPIO4,GPIO.OUT)
        if per == 0:
            led_A.value(1) # A
            led_B.value(1) # B
            led_C.value(1) # C
            led_D.value(1) # D
            led_E.value(1) # E
            led_F.value(1) # F
            led_G.value(0) # G
            led_DP.value(0) # DP
        if per == 1:
            led_A.value(0) # A
            led_B.value(1) # B
            led_C.value(1) # C
            led_D.value(0) # D
            led_E.value(0) # E
            led_F.value(0) # F
            led_G.value(0) # G
            led_DP.value(0) # DP
        if per == 2:
            led_A.value(1) # A
            led_B.value(1) # B
            led_C.value(0) # C
            led_D.value(1) # D
            led_E.value(1) # E
            led_F.value(0) # F
            led_G.value(1) # G
            led_DP.value(0) # DP
        if per == 3:
            led_A.value(1) # A
            led_B.value(1) # B
            led_C.value(1) # C
            led_D.value(1) # D
            led_E.value(0) # E
            led_F.value(0) # F
            led_G.value(1) # G
            led_DP.value(0) # DP
        if per == 4:
            led_A.value(0) # A
            led_B.value(1) # B
            led_C.value(1) # C
            led_D.value(0) # D
            led_E.value(0) # E
            led_F.value(1) # F
            led_G.value(1) # G
            led_DP.value(0) # DP
        if per == 5:
            led_A.value(1) # A
            led_B.value(0) # B
            led_C.value(1) # C
            led_D.value(1) # D
            led_E.value(0) # E
            led_F.value(1) # F
            led_G.value(1) # G
            led_DP.value(0) # DP
        if per == 6:
            led_A.value(1) # A
            led_B.value(0) # B
            led_C.value(1) # C
            led_D.value(1) # D
            led_E.value(1) # E
            led_F.value(1) # F
            led_G.value(1) # G
            led_DP.value(0) # DP
        if per == 7:
            led_A.value(1) # A
            led_B.value(1) # B
            led_C.value(1) # C
            led_D.value(0) # D
            led_E.value(0) # E
            led_F.value(0) # F
            led_G.value(0) # G
            led_DP.value(0) # DP
        if per == 8:
            led_A.value(1) # A
            led_B.value(1) # B
            led_C.value(1) # C
            led_D.value(1) # D
            led_E.value(1) # E
            led_F.value(1) # F
            led_G.value(1) # G
            led_DP.value(0) # DP
        if per == 9:
            led_A.value(1) # A
            led_B.value(1) # B
            led_C.value(1) # C
            led_D.value(1) # D
            led_E.value(1) # E
            led_F.value(1) # F
            led_G.value(1) # G
            led_DP.value(0) # DP



def main(model_addr=0x300000, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    try:
        sensor.reset()
    except Exception as e:
        raise Exception("sensor reset fail, please check hardware connection, or hardware damaged! err: {}".format(e))
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    anchors = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    try:
        task = None
        task = kpu.load(model_addr)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]
        while(True):
            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            per = 0
            t = time.ticks_ms() - t
            if objects:
                for obj in objects:
                    img.draw_rectangle(obj.rect())
                    per += 1
            img=img.draw_string(0, 0, "personas: %d" %(per), scale=3)
            lcd.display(img)
            mostrar(per)
    except Exception as e:
        raise e
    finally:
        if not task is None:
            kpu.deinit(task)


if __name__ == "__main__":
    try:
        main( model_addr=0x300000, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False)
        # main(model_addr="/sd/m.kmodel")
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
