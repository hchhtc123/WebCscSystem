# 智纠——Web端多格式纠错系统

# 一.项目介绍：

​    基于PaddlePaddle的Web端多格式纠错系统，前后端分离式部署，支持文本、文档及图片的多格式智能纠错！同时支持对修正的错误字进行标记提示和结果的保存。

**技术栈：**  后端：FastAPI + PaddleNLP + PaddleHub；前端：Vue+ ElementUI。

**项目教程：**  https://aistudio.baidu.com/aistudio/projectdetail/4145528

喜欢的小伙伴希望可以送个Fork、喜欢和关注❤！

# 二.  项目目录结构说明：

```
├── 项目说明文档.txt             // 介绍项目环境相关配置操作，项目必看！
├── backend                     // 后端API服务模块
│   └── main.py                 // API服务主程序
│   └── sutil.py                // 所需工具函数
│   └── resource                // 存放上传的文件资源
├── frontend                    // 纠错系统web前端界面模块
│   └── src/router/index.js     // 定义界面路由
│   └── src/views/              // 搭建的web新界面
```

# 三.项目演示：

**项目演示视频：**  https://www.bilibili.com/video/BV1tB4y1X7u2/

**文本纠错界面演示：**

![文本纠错界面.png](https://ai-studio-static-online.cdn.bcebos.com/fbe2584b7b2b40a2b0044659079d711513fae861682f4214aff18b792b9e7093)

**文档纠错界面演示：**

![文档纠错界面.png](https://ai-studio-static-online.cdn.bcebos.com/5f75f48b94d042d880ef3888ef8efeda390fb9c9110644368760eda47f7fa8a9)

**图片纠错界面演示：**

![图片纠错界面.png](https://ai-studio-static-online.cdn.bcebos.com/b802a4ff09d342a3b800d0217ad32f644ae647ed522743d9b65d3f5565b384af)

# 四.相关文档

1. FastAPI官方文档：https://fastapi.tiangolo.com/zh/
2. Postman使用教程：https://mp.weixin.qq.com/s/IoseF-2Ma8mH2gdQLn1rUA
3. Vue官方文档：https://v3.cn.vuejs.org/
4. ElementUI文档：https://v3.cn.vuejs.org/
5. Vue-admin-template：https://github.com/PanJiaChen/vue-admin-template

# 五.联系作者：
​     项目运行过程中遇到问题欢迎提交Issue，也可以qq联系**1075558916**，注意提供完整报错信息和截图便于定位和解决问题。
