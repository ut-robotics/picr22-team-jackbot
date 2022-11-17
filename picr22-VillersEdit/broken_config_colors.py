
    colors_lookup	= np.zeros(0x1000000, dtype=np.uint8)

#camera instance for normal web cameras
try:
    with open('colors/colors.pkl', 'rb') as fh:
        colors_lookup = pickle.load(fh)
except:
    colors_lookup	= np.zeros(0x1000000, dtype=np.uint8)

#camera instance for normal web cameras
cap = camera.OpenCVCamera(id = 2)
# camera instance for realsense cameras
cap = camera.RealsenseCamera(exposure = 100)

processor = image_processor.ImageP
    colors_lookup	= np.zeros(0x1000000, dtype=np.uint8)

#camera instance for normal web cameras
try:
    with open('colors/colors.pkl', 'rb') as fh:
        colors_lookup = pickle.load(fh)
except:
    colors_lookup	= np.zeros(0x1000000, dtype=np.uint8)

#camera instance for normal web cameras
cap = camera.OpenCVCamera(id = 2)
# camera instance for realsense cameras
cap = camera.RealsenseCamera(exposure = 100)

processor = image_processor.ImageP
cv2.namedWindow('rgb')
cv2.setMouseCallback('rgb', choose_color)
cv2.setMouseCallback('mask', choose_color)

print("Quit: 'q', Save 's', Erase selected color 'e'")
print("Balls 'g', Magenta basket='m', Blue basket='b', Field='f', White='w', Black='d', Other='o'")

cap.open()

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
cap.open()

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    , Field='f', White='w', Black='d', Other='o'")

cap.open()

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
    fragmented	= colors_lookup[rgb[:,:,0] + rgb[:,:,1] * 0x100 + rgb[:,:,2] * 0x10000]
    frame = np.zeros((cap.rgb_height, cap.rgb_width, 3), dtype=np.uint8)

    for color in Color:
        frame[fragmented == int(color)] = color.color

    cv2.imshow('mask', frame)
    
    k = cv2.waitKey(1) & 0xff

    if k == ord('q'):
        break
    elif k in keyDict:
        col = keyDict[k]
        print(col)
        p = int(col)
    elif k == ord('s'):
        with open('colors/colors.pkl', 'wb') as fh:
            pickle.dump(colors_lookup, fh, -1)
        print('saved')
    elif k == ord('e'):
        print('erased')
        colors_lookup[colors_lookup == p]	= 0

# When everything done, release the capture

cap.close()

cv2.destroyAllWindows()
)
except:
    colors_lookup	= np.zeros(0x1000000, dtype=np.uint8)

#camera instance for normal web cameras
cap = camera.OpenCVCamera(id = 2)
# camera instance for realsense cameras
cap = camera.RealsenseCamera(exposure = 100)

processor = image_processor.ImageP
cv2.namedWindow('rgb')
cv2.setMouseCallback('rgb', choose_color)
cv2.setMouseCallback('mask', choose_color)

print("Quit: 'q', Save 's', Erase selected color 'e'")
print("Balls 'g', Magenta basket='m', Blue basket='b', Field='f', White='w', Black='d', Other='o'")

cap.open()

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
cap.open()

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    , Field='f', White='w', Black='d', Other='o'")

cap.open()

while(True):
    processedData = processor.process_frame()

    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
    rgb = processedData.color_frame

    cv2.imshow('rgb', rgb)
    
    fragmented	= colors_lookup[rgb[:,:,0] + rgb[:,:,1] * 0x100 + rgb[:,:,2] * 0x10000]
    frame = np.zeros((cap.rgb_height, cap.rgb_width, 3), dtype=np.uint8)

    for color in Color:
        frame[fragmented == int(color)] = color.color

    cv2.imshow('mask', frame)
    
    k = cv2.waitKey(1) & 0xff

    if k == ord('q'):
        break
    elif k in keyDict:
        col = keyDict[k]
        print(col)
        p = int(col)
    elif k == ord('s'):
        with open('colors/colors.pkl', 'wb') as fh:
            pickle.dump(colors_lookup, fh, -1)
        print('saved')
    elif k == ord('e'):
        print('erased')
        colors_lookup[colors_lookup == p]	= 0

# When everything done, release the capture

cap.close()

cv2.destroyAllWindows()
