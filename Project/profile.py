import subprocess

def install(name):
    subprocess.call(['pip','install', name])
    
def kivyinstall(name):
    subprocess.call(['garden','install',name])

install("matplotlib")
install("kivy")
install("numpy")
install("pandas")
install("sklearn")
install("scipy")
install("shapely")
kivyinstall("matplotlib")
