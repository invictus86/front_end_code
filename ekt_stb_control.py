#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通过读取json文件的形式完成对机顶盒锁台的操作：
步骤：
①匹配当前app界面（是否需要按菜单键）
②解析json文件控制stb进行锁台操作
③锁台成功，退出锁台界面

按键：UP、DOWN、LEFT、RIGHT、OK、MENU、EXIT
图片匹配：stbt.match（）

json文件及图片使用tcp服务的形式
"""

