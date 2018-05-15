from watchdog.observers import Observer
from watchdog.events import *
import time

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            return "文件夹从{0}移动到{1}".format(event.src_path, event.dest_path)
        else:
            return "文件从{0}移到{1}".format(event.src_path, event.dest_path)

    def on_created(self, event):
        if event.is_directory:
            return "文件夹创建路径：{0}".format(event.src_path)
        else:
            return "文件创建路径：{0}".format(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return "文件夹已删除：{0}".format(event.src_path)
        else:
            return "文件已删除：{0}".format(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return "文件夹已修改：{0}".format(event.src_path)
        else:
            return "文件已修改：{0}".format(event.src_path)

if __name__ == '__main__':
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,
                      "/Users/chuxiaoyi/python/练习/code/毕设/design/spider_spider/log_spider",
                      True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()