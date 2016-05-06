
# Step by Step: Social programming

Social(Team) programming Practice based on : bootProcessInformation

The Prototype Project : Real-time Monitoring System for Thermal Power Plant

## Software

* **Version control with Git:** Github.com, EGIT

* **Development:** Eclipse CDT,PyDev,Markdown Editor, Github Flavored Markdown Viewer

##  Steps

 * **One:**  Fork source bootProcessInformation to your gitHub account

 * **Two:**  Clone forkd bootProcessInformation to your local repository

 * **Three:** Import bootProcessInformation from local repository to Eclipse Workspace

 * **Four:**  Coding your task in the local project

 * **Five:**  Push to GitHub and contribute to the source repository

 * **Six:**  Merge your branch to the source branch

* **Seven:** Synchronize your branch with the source branch

**NOTE: you may 
     
   * use any software tools， for example：Github Desktop for Git client,  PyCharm for code, Atom for document   
   
   * clone source branch to **your local repository**,push and synchronize your local branch with the source branch

## Step One:  Fork source bootProcessInformation to your gitHub account

* Fork source bootProcessInformation

 ![fork](./img/1_fork.png)

* Forked bootProcessInformation in your GitHub account

 ![forked](./img/1_forked.png)

## Step Two:  Clone forked branch  to your local  respository

* Start clone: git

 ![clone_1](./img/2_clone_1.png)

* copy url to clipboard

 ![clone_clipboard](./img/2_clone_clipboard.png)

* copy source to your local

 ![clone_source](./img/2_clone_source.png)

* Branch selection

 ![clone_branch](./img/2_clone_branch.png)

* cloned respository

 ![clone_localgit](./img/2_clone_localgit.png)

## Step Three: Import bootProcessInformation from local repository to Eclipse Workspace

* import project in the cloned respository to your workspace

  * File->import

  * general->Existing  Projects

  ![workspace](./img/3_workspace.png)

* choose your project

 ![workspace_project](./img/3_workspace_project.png)

* imported project

 ![3_workspace_imported](./img/3_workspace_imported.png)

## Step Four: Coding your task in the local project

### 4.1 your analysis_task package

* new python package : m300exair

   * /PrototypeRealTimeMonitoring/analysis_task/m300exair

   ![4_newpackage.png](./img/4_newpackage.png)

   ![4_newmodel](./img/4_newmodel.png)

* copy all files of  ``analysis_task/demo_turbine``` to your m300exair , rename to

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

   ![4_m300exair](./img/4_m300exair.png)


* then,coding:

#### 4.1.1 /analysis_task/__init__.py


```python
# TODO: add your package
from analysis_task.m300exair import *
```

####  4.1.2 pyexair.py

```python
def exaircoff(o2):
    return 21/(21-o2)
```

#### 4.1.3 tag about exair

* m300exair/task_exair_tag_in.txt

 ```
id	                       desc        	defaultvalue
DEMO.DCS2AI.2JZA2226	空预器进口烟气氧量	3.8375
```

* m300exair/task_exair_tag_out.txt

 ```
id                       	desc            defaultvalue
DEMO.DCS2AO.EXAIRCOFF  空预器进口过量空气系数     1.25
```
#### 4.1.4 exair_online_analysis

* m300exair/task_exair_online_analysis.py

 ```python
 from datetime import datetime
 import codecs

  from db.pyredis import TagDefToRedisHashKey, tagvalue_redis, SendToRedisHash
 from analysis_task.m300exair.pyexair import exaircoff

  class UnitExaircoff:

    def __init__(self, tagin, tagout):

        self.ailist = []
        file = codecs.open(tagin, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid})

        self.aolist = []
        file = codecs.open(tagout, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.aolist.append({'id':tagid, 'desc':desc, 'value':None, 'ts':None})

    def setouttag(self):
        TagDefToRedisHashKey(self.aolist)

    def Onlinecal(self):
        o2 = float(self.ailist[0]['value'])
        cur_exaircoff =exaircoff(o2)
        self.aolist[0]['value'] = cur_exaircoff

    def run(self):
        tagvalue_redis(self.ailist)
        self.Onlinecal()
        curtime = datetime.now()
        for tag in self.aolist:
            tag['ts'] = curtime

        SendToRedisHash(self.aolist)

        tagvalue_redis(self.aolist)

        for tag in self.aolist:
            print(tag['desc'], tag['value'])

 ```

#### 4.1.5 sampling simulation

* /m300exair/task_exair_sampling_simulation.py

 ```python
  class UnitExaircoffSimulation:

      def __init__(self, tagfile):

          self.ailist = []
        file = codecs.open(tagfile, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid, 'desc':desc, 'value':float(value)})

        self.o2base = self.ailist[0]['value']

      def settag(self):
          TagDefToRedisHashKey(self.ailist)

      def run(self):
          self.ailist[0]['value'] = self.o2base * (1 + random.random() * 0.005)

          curtime = datetime.now()
          for tag in self.ailist:
              tag['ts'] = curtime
          SendToRedisHash(self.ailist)

         print('UnitExaircoffSimulation sampling on ', self.ailist[0]['value'])

 ```

### 4.2 your analysis_task to analysis_thread

#### 4.2.1 /analysis_thread/sampling_simulation_thread_runner.py

* Add code

 ```python
 # TODO：add your module
from analysis_task.m300exair.task_exair_sampling_simulation import UnitExaircoffSimulation

    # add your task
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")

    Simulation = UnitExaircoffSimulation(taginfile)
    TaskList.append(Simulation)    
 ```

* Test Running

  /m300exair/task_exair_sampling_simulation.py

  ![4_simulation](./img/4_simulation.png)

#### 4.2.2 analysis_thread/online_analysis_thread_runner.py

* Add code

 ```python
# add your module
from analysis_task.m300exair.task_exair_online_analysis import UnitExaircoff

     # TODO: add your task
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")
    tagoutfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_out.txt")

    TaskExaircoff = UnitExaircoff(taginfile, tagoutfile)
    TaskList.append(TaskExaircoff)
  ```

* Test Running

  analysis_thread/online_analysis_thread_runner.py

  ![4_online_analysis](./img/4_online_analysis.png)


### 4.3 your page and handle to www

#### 4.3.1 page handler

* copy  demo files and rename to your task,then codeing

  * handler/m300exair_tag.txt

  ```
 desc	               id	               si
空预器进口烟气氧量	 DEMO.DCS2AI.2JZA2214   %
空预器进口过量空气系数	DEMO.DCS2AO.EXAIRCOFF	/
  ```

* handler/m300exair_handler.py

 ```python

  cur_tag=gentag("./handler/m300exair_tag.txt")

  class initHandler(tornado.web.RequestHandler):

        def get(self):

             title = '在线监视客户端： 过量空气系数'

            cur_tag.GetTagDefInfo()
            tagvalue = cur_tag.TagSnapshot(）
 ```

* modifing `www/__init__.py`

 ```python
   # TODO: add your handler
  from www.handler.m300exair_handler import *

 ```

#### 4.3.2 page template

* copy demo  template and rename for your task


* then modifying ```/templates/m300exair_ui.html``` contents

 ```javascript
 // TODO: your   websocket URL
 ws = new WebSocket("ws://" + window.location.host + "/m300exair_websocket");
 ```

#### 4.3.3 add your page template to web site

* /www/app.py

 ```python
   # TODO: import you handler
   import www.handler.m300exair_handler as m300exair

    def sendmsssage2allclient():

          # TODO: add your  task
          m300exair.cur_tag.sendmsssage2client()

   class Application(tornado.web.Application):   

         def __init__(self):
             handlers = [
                  (r"/", indexHandler),

                   # TODO: add your handler
                   (r"/m300exair/", m300exair.initHandler),
                   (r"/m300exair_websocket",m300exair.WebSocketHandler),
              ]  
```

* templates/index.html

 ```javascript
   <div class="container">
        <h3 class="offset3">分析任务 </h1>

        <ul class="pull-center">
	      <li><a href="/demo_tb/">示例：高压缸效率</a></li>

          <!-- add your link  -->
          <li><a href="/m300exair/">m300exair:过量空气系数</a></li>

        </ul>
  </div>
 ```

#### 4.3.4 Running

`/www/app.py`

* Home Page

  ![4_index](./img/4_index.png)

* your task page

  ![4_page_m300exair](./img/4_page_m300exair.png)

### 4.4 review your code

* **TODO** comment tag in your coding location,

   "Windows->Show View->Tasks" to review your code

    ![4_todo_tag_task](./img/4_todo_tag_task.png)

## Step Five:  Push to GitHub and contribute to the source repository

### 5.1 Commit and push local to your fored repository on github

* Commit

  ![5_commit_1](./img/5_commit_1.png)

  ![5_commit_2](./img/5_commit_2.png)

* check result on github

 ![5_commit_3](./img/5_commit_3.png)

### 5.2 Contribute to the source repository

* New pull requests to source repository

 ![5_pull_1](./img/5_pull_1.png)

* Create  pull request

   * source repository in the left , your repository in the right

   * request pull your repository (right) to source repository(left)

   ![5_pull_2](./img/5_pull_2.png)

* commit message

   ![5_pull_3](./img/5_pull_3.png)

## Step Six:  Merge your branch to the source branch

### 6.1 source: remote merge

* check pull requests:

  ![6_merge_1](./img/6_merge_1.png)

* merge pull requests:

  ![6_merge_2](./img/6_merge_2.png)

  ![6_merge_3](./img/6_merge_3.png)

### 6.2 source: pull remote  to  local

* pull remote  to  local

   ![6_source_pull_1](./img/6_source_pull_1.png)

   ![6_source_pull_2](./img/6_source_pull_2.png)

   ![6_source_pull_3](./img/6_source_pull_3.png)

* local after pull

  ![6_source_pull_4](./img/6_source_pull_4.png)

## Step Seven:  synchronize your branch with the source branch

* the source branch appended guide after your forked, synchronous action:

### 7.1 new pull request in your forked branch

* "New pull request"

  ![7_sync_1](./img/7_sync_1.png)

* after "New pull request"
   * base fork(left): the source branch

   * head fork(right): your forked branch：(yellow)

 ![7_sync_2](./img/7_sync_2.png)


* you need  **compare across forks** or **switching  the  base**

 change  base fork and head fork, so that:

   * **base fork(left)**: your forked branch：(yellow)

   *  head fork(right): the source branch:  

   ![7_sync_30](./img/7_sync_30.png)

* then, you can “Create pull request”:

   ![7_sync_3](./img/7_sync_3.png)

* you see all commits in source branch after you forked

   ![7_sync_31](./img/7_sync_31.png)

* pull request +1 :

  ![7_sync_4](./img/7_sync_4.png)

  ![7_sync_5](./img/7_sync_5.png)

### 7.2 merge pull request(source branch to your branch)

* merge source branch to your branch

 ![7_sync_6](./img/7_sync_6.png)

* synchronized branch

 ![7_sync_7](./img/7_sync_7.png)
