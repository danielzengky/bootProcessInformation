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
        |---www: web werver
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

## Analysis Server

#### 1 Add your task module 

reference: ``` /analysis_task/demo_turbine```  exactly

    set your task module name

    coding your task file.

for example your task:  m300exair

```
analysis_task
     |
     |--m300exair
         |
         |--readme.txt: your task introduction
         |
         |--__init__.py  :  package
         |
         |--pyexair.py : task analysis code
         |
         |--task_exair_tag_in.txt: input tag of your task (utf-8)
         |
         |--task_exair_tag_out.txt: input tag of your task (utf-8)
         |
         |--task_exair_sampling_simulation.py： sampling simulation on task_exair_tag_in.txt to redis
         |
         |--task_exair_online_analysis.py：
 
```
 
add your module to  `/analysis_task/__init__.py`
```python

# add your module here

from analysis_task.m300exair import *

```

#### 2  Add your task to Simulation and Analysis thread

for examle your task:  m300exair

`/analysis_thread/sampling_simulation_thread_runner.py`

```python
try:   
    from analysis_task.m300exair.task_exair_sampling_simulation import UnitExaircoffSimulation
except:
    import sys
    sys.path.append("..")
    from  analysis_task.m300exair.task_exair_sampling_simulation import  UnitExaircoffSimulation
 
  # add you tesk
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")
    
    Simulation = UnitExaircoffSimulation(taginfile)
    TaskList.append(Simulation)    
```

`/analysis_thread/online_analysis_thread_runner.py`

```python
# add your module 
try:
    from analysis_task.m300exair.task_exair_online_analysis import UnitExaircoff
except:
    import sys
    sys.path.append("..")
    from analysis_task.m300exair.task_exair_online_analysis import UnitExaircoff
    
     # add your task
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")
    tagoutfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_out.txt")
    
    TaskExaircoff = UnitExaircoff(taginfile, tagoutfile)
    TaskList.append(TaskExaircoff)
```  

#### 3 Running your task 
    
    3.1 Redis Server On
    
    3.2 sampling_simulation_thread_runner.py
    
    3.3 online_analysis_thread_runner.py

## WWW Server

Add your task page and handler

### 1  page handler: 

`www/handler/m300exair_handler.py`  
    
`www/handler/m300exair_tag.txt (utf-8)`
     

### 1  page template: 

 `www/templates/m300exair_ui.html `
  
 ```javascript 
 <script type="text/javascript"> 
     ws = new WebSocket("ws://" + window.location.host + "/m300exair_websocket");
 </script>
```    
   
 
### 3  WWW 

`www/__init__.py`
    
    from www.handler.m300exair_handler import *
  
`www/app.py`
    
 ```python  
     try:
        import www.handler.m300test_handler as m300test
     except:
        import handler.m300test_handler as m300test  
     
     handlers = [
           
            (r"/", indexHandler),
           
          # add your handler，： 
            (r"/m300exair/", m300exair.initHandler),
            (r"/m300exair_websocket",m300exair.WebSocketHandler),
            
            
        ]
```

`www/templates/index.html`

```
 <div class="container">
        <h3 class="offset3">分析任务 </h1>
        <ul class="pull-center">
	      <li><a href="/demo_tb/">示例:高压缸效率</a></li>
         
          <!-- add your link  --> 
          <li><a href="/m300exair/">m300exair:过量空气系数</a></li> 
    
        </ul>
 </div>
```         
 
## License

MIT           