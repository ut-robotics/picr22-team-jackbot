import camera
import segment
import _pickle as pickle
import numpy as np
import cv2
import Color as c
import numpy as np



class Object():
    def __init__(self, x = -1, y = -1, size = -1, distance = -1, exists = False):
        self.x = x
        self.y = y
        self.size = size
        self.distance = distance
        self.exists = exists

    def __str__(self) -> str:
        return "[Object: x={}; y={}; size={}; distance={}; exists={}]".format(self.x, self.y, self.size, self.distance, self.exists)

    def __repr__(self) -> str:
        return "[Object: x={}; y={}; size={}; distance={}; exists={}]".format(self.x, self.y, self.size, self.distance, self.exists)


# results object of image processing. contains coordinates of objects and frame data used for these results
class ProcessedResults():

    def __init__(self, 
                balls=[], 
                basket_b = Object(exists = False), 
                basket_m = Object(exists = False), 
                color_frame = [],
                depth_frame = [],
                fragmented = [],
                debug_frame = []) -> None:


        self.balls = balls
        self.basket_b = basket_b
        self.basket_m = basket_m
        self.color_frame = color_frame
        self.depth_frame = depth_frame
        self.fragmented = fragmented

        # can be used to illustrate things in a separate frame buffer
        self.debug_frame = debug_frame



#Main processor class. processes segmented information
class ImageProcessor():
    def __init__(self, camera, color_config = "colors/colors.pkl", debug = False):
        self.camera = camera
        
#         ###
#         while True:
#             depth_frame = camera.align.get_depth_frame()###
#             aligned_color_frame = aligned_frames.get_color_frame()###
#             if not depth_frame or not aligned_color_frame: continue###
#             
#             ### over here            
#             color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics
#             depth_image = np.asanyarray(depth_frame.get_data())
#             color_image = np.asanyarray(aligned_color_frame.get_data())
#             #Use pixel value of  depth-aligned color image to get 3D axes
#         ###

        
        blobparams = cv2.SimpleBlobDetector_Params()
        blobparams.filterByArea = True
        blobparams.minArea = 100
        blobparams.maxArea = 80000
        blobparams.filterByCircularity = False
        #blobparams.minCircularity = 0.1
        blobparams.minDistBetweenBlobs = 50
        blobparams.filterByInertia = False
        #blobparams.minInertiaRatio = 0.5
        blobparams.filterByConvexity = False
        #blobparams.minConvexity = 0.5

        self.detector = cv2.SimpleBlobDetector_create(blobparams)

        self.color_config = color_config
        with open(self.color_config, 'rb') as conf:
            self.colors_lookup = pickle.load(conf)
            self.set_segmentation_table(self.colors_lookup)

        self.fragmented	= np.zeros((self.camera.rgb_height, self.camera.rgb_width), dtype=np.uint8)

        self.t_balls = np.zeros((self.camera.rgb_height, self.camera.rgb_width), dtype=np.uint8)
        self.t_basket_b = np.zeros((self.camera.rgb_height, self.camera.rgb_width), dtype=np.uint8)
        self.t_basket_m = np.zeros((self.camera.rgb_height, self.camera.rgb_width), dtype=np.uint8)

        self.debug = debug
        self.debug_frame = np.zeros((self.camera.rgb_height, self.camera.rgb_width), dtype=np.uint8)

    def set_segmentation_table(self, table):
        segment.set_table(table)

    def start(self):
        self.camera.open()

    def stop(self):
        self.camera.close()

    def analyze_balls(self, t_balls, fragments) -> list:
# #         cv2.imshow('Debugger', t_balls)
# #         #t_balls = cv2.bilateralFilter(t_balls,9,75,75)
#         keypoint_balls = self.detector.detect(t_balls)
#         cv2.imshow('Debugger2', t_balls)
# #         contours, hierarchy = cv2.findContours(t_balls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 
#         balls = []
#         
#         for contour in keypoint_balls:
#             print(contour)
#             
#             # ball filtering logic goes here. Example includes filtering by size and an example how to get pixels from
#             # the bottom center of the fram to the ball
# 
# #             size = cv2.contourArea(contour)
# #             
# #             #size filtration
# #             print(contour.size, contour.pt[0], contour.pt[1])
#             if contour.size < 3:
#                 continue
# #             
# #             #print(size)
# #             x, y, w, h = cv2.boundingRect(contour)
# # 
# #             ys	= np.array(np.arange(y + h, self.camera.rgb_height), dtype=np.uint16)
# #             xs	= np.array(np.linspace(x + w/2, self.camera.rgb_width / 2, num=len(ys)), dtype=np.uint16)
# # 
# #             obj_x = int(x + (w/2))
# #             obj_y = int(y + (h/2))
# #             obj_dst = obj_y
# # 
#             if self.debug:
# #                 size2 = cv2.contourArea(contour)
# #                 self.debug_frame[ys, xs] = [0, 0, 0]
#                 cv2.circle(self.debug_frame,(int(contour.pt[0]), int(contour.pt[1])), 10, (0,255,0), 2)
# # 	
#             balls.append(Object(x = contour.pt[0], y = contour.pt[1], size = contour.size, distance = contour.pt[1], exists = True))
# #             
# 
#         balls.sort(key= lambda x: x.distance)
# 
#         return balls
#     
        contours, hierarchy = cv2.findContours(t_balls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        balls = []
        
        for contour in contours:
            
            # basket filtering logic goes here. Example includes size filtering of the basket

            size = cv2.contourArea(contour)

            if size < 15:
                continue

            x, y, w, h = cv2.boundingRect(contour)

            obj_x = int(x + (w/2))
            obj_y = int(y + (h/2))
            obj_dst = obj_y

            balls.append(Object(x = obj_x, y = obj_y, size = size, distance = obj_dst, exists = True))

        balls.sort(key= lambda x: x.size)
        try:
            if self.debug:
                if balls[0].exists == True:
                    cv2.circle(self.debug_frame,(balls[0].x, balls[0].y), int((balls[0].size/120)+12), 255, -1)
        except:
            pass
        return balls
        # #         cv2.imshow('Debugger', t_balls)
# #         #t_balls = cv2.bilateralFilter(t_balls,9,75,75)
#         keypoint_balls = self.detector.detect(t_balls)
#         cv2.imshow('Debugger2', t_balls)
# #         contours, hierarchy = cv2.findContours(t_balls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 
#         balls = []
#         
#         for contour in keypoint_balls:
#             print(contour)
#             
#             # ball filtering logic goes here. Example includes filtering by size and an example how to get pixels from
#             # the bottom center of the fram to the ball
# 
# #             size = cv2.contourArea(contour)
# #             
# #             #size filtration
# #             print(contour.size, contour.pt[0], contour.pt[1])
#             if contour.size < 3:
#                 continue
# #             
# #             #print(size)
# #             x, y, w, h = cv2.boundingRect(contour)
# # 
# #             ys	= np.array(np.arange(y + h, self.camera.rgb_height), dtype=np.uint16)
# #             xs	= np.array(np.linspace(x + w/2, self.camera.rgb_width / 2, num=len(ys)), dtype=np.uint16)
# # 
# #             obj_x = int(x + (w/2))
# #             obj_y = int(y + (h/2))
# #             obj_dst = obj_y
# # 
#             if self.debug:
# #                 size2 = cv2.contourArea(contour)
# #                 self.debug_frame[ys, xs] = [0, 0, 0]
#                 cv2.circle(self.debug_frame,(int(contour.pt[0]), int(contour.pt[1])), 10, (0,255,0), 2)
# # 	
#             balls.append(Object(x = contour.pt[0], y = contour.pt[1], size = contour.size, distance = contour.pt[1], exists = True))
# #             
# 
#         balls.sort(key= lambda x: x.distance)
# 
#         return balls
    def analyze_baskets(self, t_basket, depth, debug_color = (0, 255, 255)) -> list:
        contours, hierarchy = cv2.findContours(t_basket, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        baskets = []
        for contour in contours:

            # basket filtering logic goes here. Example includes size filtering of the basket

            size = cv2.contourArea(contour)

            if size < 50:
                continue

            x, y, w, h = cv2.boundingRect(contour)

            obj_x = int(x + (w/2))
            obj_y = int(y + (h/2))

            if depth is None:
                obj_dst = obj_y
            else:
                obj_dst = np.average(depth[8-3:8+3, obj_x-2:obj_x+2]) ## changed this

            baskets.append(Object(x = obj_x, y = obj_y, size = size, distance = obj_dst, exists = True))

        baskets.sort(key= lambda x: x.size)

        basket = next(iter(baskets), Object(exists = False))

        if self.debug:
            if basket.exists:
                cv2.circle(self.debug_frame,(basket.x, basket.y), 10, debug_color, -1)

        return basket

    def get_frame_data(self, aligned_depth = False):
        if self.camera.has_depth_capability():
            return self.camera.get_frames(aligned = aligned_depth)
        else:
            return self.camera.get_color_frame(), np.zeros((self.camera.rgb_height, self.camera.rgb_width), dtype=np.uint8)

    def process_frame(self, aligned_depth = True) -> ProcessedResults:
        color_frame, depth_frame = self.get_frame_data(aligned_depth = aligned_depth)
        ###colorfram - cam
        segment.segment(color_frame, self.fragmented, self.t_balls, self.t_basket_m, self.t_basket_b)

        if self.debug:
            self.debug_frame = np.copy(color_frame)

        balls = self.analyze_balls(self.t_balls, self.fragmented)
        basket_b = self.analyze_baskets(self.t_basket_b, depth_frame, debug_color=c.Color.BLUE.color.tolist())
        basket_m = self.analyze_baskets(self.t_basket_m, depth_frame, debug_color=c.Color.MAGENTA.color.tolist())

        return ProcessedResults(balls = balls, 
                                basket_b = basket_b, 
                                basket_m = basket_m, 
                                color_frame=color_frame, 
                                depth_frame=depth_frame, 
                                fragmented=self.fragmented, 
                                debug_frame=self.debug_frame)
