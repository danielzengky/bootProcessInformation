# bootProcessInformation

The Prototype Project ： Real-time Monitoring System for Thermal Power Plant

Author:   Cheng Maohua

Email:    cmh@seu.edu.cn

## Dependencies

* **Database**  

    * Redis 3.x: http://redis.io

* **Analysis**

   * Python3.x :  https://www.python.org/
   * redis-py  :  https://github.com/andymccurdy/redis-py
   * SEUIF97   :  https://github.com/Py03013052/SEUIF97

* **Web Server**

   * Tornado 4.X :  http://www.tornadoweb.org/

* **Browser**

   * Support Websocket(HTML5)

## Run

1. analysis_thread\sampling_simulation_thread_runner.py

2. analysis_thread\online_task_thread_runner.py

3. www\app.py

4. http://127.0.0.1:8000

## Directory
```
PrototypeRealTimeMonitoring
        |
        |---analysis_task :  Real-time  Monitoring task
        |         |
        |         |--demo_turbine : demo task
        |         |
        |         |--m300task: add your task
        |         |
        |
        |---analysis_thread:
        |         |
        |         |--sampling_simulation_thread_runner.py: sampling simulation
        |         |
        |         |--online_task_thread_runner.py : online analysis
        |
        |
        |---db: redis
        |
        |---doc: documents
        |
        |---guide： Social(Team) programming Practice
        |
        |---www: web server
             |
             |--handler
             |        |
             |        |--gen_taginfo.py：  general taginfo
             |        |
             |        |--*_handler.py :handler of  each task
             |        |
             |        |--*_tag.txt    : tag of  each task
             |        |
             |
             |--static
             |        |--css    
             |        |
             |        |--img
             |        |
             |        |-js  
             |
             |--templates
             |        |
             |        |--index.html: main page
             |        |
             |        |--*_ui.html : page of each task
             |
             |--app.py：： start web server
             |
 ```     

## Step By Step : Social(Team) programming Practice

https://github.com/Py03013052/bootProcessInformation/tree/s2016/guide


## TIPS

We highly recommend you practice coding whenever you have a few minutes.

Even if you are just modifying available code, it will be incredibly beneficial.

You **NEED** to

* use other resources,

* read codes,

*  **get your hands dirty** and **practice**

**教学做是一件事，不是三件事。我们要在做上教，在做上学。不在做上用功夫，教固不成为教，学也不成为学。——陶行知**

## License

MIT(see LICENSE.txt)     
