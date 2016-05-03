# bootProcessInformation

The Prototype Project ： Real-time Monitoring System for Thermal Power Plant 

Author:   Cheng Maohua

Email:    cmh@seu.edu.cn

## Dependencies

### Database

    Redis 3.*

### Analysis
	
	Python3.*  
	
	redis-py

	SEUIF97 
	
	https://github.com/Py03013052/SEUIF97

### Web Server

	Tornado 4.*

### Browser

	Support Websocket(HTML5)
	
### Run

	1. analysis_thread\sampling_simulation_thread_runner.py
	
	2. analysis_thread\online_task_thread_runner.py
	
	3. www\app.py
	
	4. http://127.0.0.1:8000

## Dir
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
        |---guide
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
 
# Step By Step : Your Task

https://github.com/Py03013052/bootProcessInformation/tree/s2016/guide
 
## License

MIT           