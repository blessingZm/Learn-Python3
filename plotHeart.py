# -*- coding: utf-8 -*-
"""
Created on Sun May 20 19:28:30 2018

@author: ZM
"""

import numpy as np
from matplotlib import pyplot as plt
import random
from wxpy import Bot
import os


def plot_heart(cmap, img_name):
    x_coords = np.linspace(-100, 100, 500)
    y_coords = np.linspace(-100, 100, 500)
    x_points, y_points = [], []
    for y in y_coords:
        for x in x_coords:
            xx = x * 0.03
            yy = y * 0.03
            xy = (xx ** 2 + yy ** 2 - 1) ** 3 - xx ** 2 * yy ** 3
            if xy <= 0:
                x_points.append(x)
                y_points.append(y)

    plt.scatter(x_points, y_points, s=15, alpha=1,
                c=range(len(x_points)), cmap=cmap)
    plt.savefig(img_name)


if __name__ == "__main__":
    cmaps = ['autumn', 'cool', 'magma', 'rainbow', 'Reds', 'spring', 'viridis',
             'gist_rainbow']
    # 微信登陆
    bot = Bot()
    # 找出需要的好友
    dy = bot.friends().search('杜裕')[0]
    imgName = '1.jpg'
    for i in range(6):
        plot_heart(random.choice(cmaps), img_name=imgName)
        # 给好友发图片
        dy.send_image(imgName)
        # 给好友发消息
# =============================================================================
#         dy.send(content)
# =============================================================================
        os.remove(imgName)
    bot.logout()
