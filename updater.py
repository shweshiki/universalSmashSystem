import requests
import json
import hashlib
import os
import settingsManager
import threading
import sys

def githash(data):
    s = hashlib.sha1()
    s.update("blob %u\0" % len(data))
    s.update(data)
    return s.hexdigest()

def files(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            if os.path.isfile(os.path.join(path, f)):
                yield f

def getDirectories(path):
    return [os.path.join(path,x) for x in next(os.walk(path))[1] if x.startswith('.') == False]


def getChangedList():
    changedList = []
    
    base_url = 'https://api.github.com/repos/digiholic/universalSmashSystem/contents/'
    upcomingDirs = ['']
    
    while upcomingDirs:
        directory = upcomingDirs[0]
        print(directory)
        r = requests.get(base_url+directory)
        json_content = json.loads(r.content)
        if isinstance(json_content, dict) and json_content.has_key('documentation_url'):
            print('Unable to update again. Due to API limitations, we can only allow one update check per hour. Please try again later.')
            return False
        
        for obj in json_content:
            if obj["type"] == "dir":
                upcomingDirs.append(directory+'/'+str(obj['name']))
                
            else:
                filepath = os.path.join(settingsManager.createPath(directory),obj['name'])
                try:
                    with open(filepath,'r') as f:
                        filesha = githash(f.read())
                except:
                    #We don't have a local copy of the file
                    filesha = ''
                print(filepath)
                print(filesha)
                print(obj['sha'])
                if not filesha == obj['sha']: 
                    changedList.append(directory+'/'+str(obj['name']))
        
        upcomingDirs.remove(directory)
    
    print(changedList)
    return changedList

def downloadUpdates(changedList):
    if not changedList:
        print('No updates available')
        return
    
    base_url = 'https://raw.githubusercontent.com/digiholic/universalSmashSystem/master/'
    base_dir = settingsManager.createPath('')
    
    for changedfile in changedList:
        print(changedfile)
        r = requests.get(base_url + changedfile)
        if r.status_code == 200:
            with open(base_dir+changedfile,'w') as f:
                f.seek(0)
                f.write(r.content)
                f.truncate()

def main():
    os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")
    changedList = getChangedList()
    if not changedList == False:
        downloadUpdates(changedList)
        
    print("update complete!")
    raw_input("Press any key to continue") #Pause to let user see that things ends
    
if __name__ == '__main__': main()


class UpdateThread(threading.Thread):
    def __init__(self,menu):
        threading.Thread.__init__(self)
        self.menu = menu
        self.running = False
        self.mode = 0
        
    def run(self):
        print("starting thread")
        self.running = True
        if self.mode == 0:
            changedList = self.getChangedList()
            
            if self.menu:
                self.menu.changedList = changedList
                self.menu.checkedList = True
        
        if self.mode == 1:
            if self.menu:
                self.menu.statusText.changeText('Downloading. Game will close when finished')
                self.menu.recenterStatus()
            
            self.downloadUpdates(self.changedList)    
            
            sys.exit()
            
        print("stopping thread")
        self.running = False
    
    def getChangedList(self):
        changedList = []
        
        base_url = 'https://api.github.com/repos/digiholic/universalSmashSystem/contents/'
        upcomingDirs = ['']
        
        while upcomingDirs:
            directory = upcomingDirs[0]
            if self.menu:
                self.menu.statusText.changeText(directory)
                self.menu.recenterStatus()
            r = requests.get(base_url+directory)
            json_content = json.loads(r.content)
            if isinstance(json_content, dict) and json_content.has_key('documentation_url'):
                return False
            
            for obj in json_content:
                if obj["type"] == "dir":
                    upcomingDirs.append(directory+'/'+str(obj['name']))
                    
                else:
                    filepath = os.path.join(settingsManager.createPath(directory),obj['name'])
                    try:
                        with open(filepath,'r') as f:
                            filesha = githash(f.read())
                    except:
                        #We don't have a local copy of the file
                        filesha = ''
                    print(filepath)
                    print(filesha)
                    print(obj['sha'])
                    if not filesha == obj['sha']: 
                        changedList.append(directory+'/'+str(obj['name']))
            
            upcomingDirs.remove(directory)
        
        print(changedList)
        return changedList

    def downloadUpdates(self,changedList):
        if not changedList:
            return
        
        base_url = 'https://raw.githubusercontent.com/digiholic/universalSmashSystem/master/'
        base_dir = settingsManager.createPath('')
        
        for changedfile in changedList:
            if self.menu:
                self.menu.statusText.changeText(changedfile)
                self.menu.recenterStatus()
            r = requests.get(base_url + changedfile)
            if r.status_code == 200:
                with open(base_dir+changedfile,'w') as f:
                    f.seek(0)
                    f.write(r.content)
                    f.truncate()