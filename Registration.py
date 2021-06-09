# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 09:44:40 2021

@author: limy
"""

import cv2
import numpy as np
import pandas as pd
import os


def on_mouse1(event, x, y, flags, param):    
    if event == cv2.EVENT_LBUTTONDOWN:
        p = [x, y]
        cv2.circle(ref_win, (x, y), 4, (0, 0, 255), -1)
        cv2.imshow("jizhun", ref_win)
        imagePoints1.append(p)
        print('基准坐标:', p)


def on_mouse2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        p = [x, y]
        cv2.circle(src_win, (x, y), 4, (0, 0, 255), -1)
        cv2.imshow("daipeizhun", src_win)
        imagePoints2.append(p)
        print('目标坐标:', p)



def annotion_state():
    cv2.namedWindow("daipeizhun")
    cv2.namedWindow("jizhun")
    cv2.imshow("daipeizhun", src_win)
    cv2.imshow("jizhun", ref_win)

    cv2.setMouseCallback("jizhun", on_mouse1)
    cv2.setMouseCallback("daipeizhun", on_mouse2)
 
    print('标注结束后请在标注窗口按esc退出！')
    cv2.waitKey() 
    input_str = input("确认标注结束?请输入y确认标注，输入n重新标注，输入q放弃标注。\n")
    if input_str == 'y':
        print('标注结束')
        cv2.destroyAllWindows()
        cv2.waitKey(1) 
        print('基准图像总标注点坐标:', imagePoints1)
        print('待配准图像总标注点坐标:', imagePoints2)
        state = 0

    elif input_str == 'n':
        cv2.destroyAllWindows()
        cv2.waitKey(1) 
        state = 1
        
    elif input_str == 'q':
        cv2.destroyAllWindows()
        cv2.waitKey(1) 
        state = 2

    else:
        state = 0
        print('输入非法字符，已回到初始标注界面。')

    return state    
        
        


if __name__ == '__main__':
    
    if not os.path.exists('data_info.csv'):
        print('请将data_info.csv文件放在程序根目录！')
    
    else:

        data_info = pd.read_csv('data_info.csv')
        
        # 检查csv表格是否异常
        if data_info['ori_image_path'].tolist() == [] or data_info['target_image_path'].tolist() == [] or data_info['output_path'].tolist() == [] or data_info['output_file_name'].tolist() == []:
            print('请检查data_info.csv文件中内容是否为空！')
            
        else:   
            ori_image_path = data_info['ori_image_path'].tolist()
           
            for num in range(len(ori_image_path)):
                ori_image_path = data_info['ori_image_path'].tolist()[num]
                target_image_path = data_info['target_image_path'].tolist()[num]
                output_file_path = os.path.join(data_info['output_path'].tolist()[num], data_info['output_file_name'].tolist()[num])

                print('您正在使用配准标注平台，请注意：标注时待配准图像和参考图像的标点顺序要一致，若顺序不一致则无法配准！同时每次标注时请标注4个关键点对，不要多也不要少，谢谢您的使用！')
                state = 1
                while(state):    
                    original_image = cv2.imread(ori_image_path)
                    ref_win = cv2.imread(ori_image_path)
                    target_image = cv2.imread(target_image_path)
                    src_win = cv2.imread(target_image_path)
                    
                    imagePoints1 = []
                    imagePoints2 = []
                    
                    state = annotion_state()
                    
                    if state == 2:
                        break
                    
                    elif state == 0:
                        if (len(imagePoints1) != len(imagePoints2)) or (len(imagePoints1) == 0 or len(imagePoints2) == 0):
                            print('标注点对数量不一致请重新标注!')
                            print('参考图像标注点数量：', len(imagePoints1))
                            print('待配准图像标注点数量：', len(imagePoints2))
                            state = 1
                        elif len(imagePoints1) != 4 or len(imagePoints2) != 4:
                            print('两次标注点对数量不为4，请重新标注！')
                            print('参考图像标注点数量：', len(imagePoints1))
                            print('待配准图像标注点数量：', len(imagePoints2))
                            state = 1
                        
                        
                if len(imagePoints1)==4 and len(imagePoints2)==4:
                    src_points = np.array(imagePoints2, dtype=np.float32)
                    den_points = np.array(imagePoints1, dtype=np.float32)
                    # getPerspectiveTransform可以得到从点集src_points到点集den_points的透视变换矩阵
                    T = cv2.getPerspectiveTransform(src_points, den_points)
                    # 进行透视变换
                    # 注意透视变换第三个参数为变换后图片大小，格式为（高度，宽度）
                    warp_imgae = cv2.warpPerspective(target_image, T, (original_image.shape[1], original_image.shape[0]), borderValue=[255, 255, 255])
                
                    cv2.imshow("transform", warp_imgae)
                    cv2.imshow("jizhun", ref_win)
                    cv2.imshow("daipeizhun", src_win)
                
                    cv2.imwrite(output_file_path, warp_imgae)
        #            cv2.imwrite("result.jpg", warp_imgae)
                    cv2.imwrite(os.path.join(data_info['output_path'].tolist()[0], "src_p.jpg"), src_win)
                    cv2.imwrite(os.path.join(data_info['output_path'].tolist()[0], "ref_p.jpg"), ref_win)
                    
                    print('图片已保存到输出目录，请查看！请点击标注窗口，按esc退出此次标注。')
                    print(output_file_path)
                    
                    cv2.waitKey() 
                    cv2.destroyAllWindows()
                
                else:
                    print('您已放弃标注，感谢您的使用！')
            
        
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

