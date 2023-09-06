import time

from command_analyzer.analyzer import CommandAnalyzer
from command_executor.executor import CommandExecutor
from receiver.rx import Receiver
from transmitter.tx import Transmitter

import subprocess
import platform
import os


class Manager:
    def __init__(self):
        print("Thread Manager Class Constructor")

        self.receiver = Receiver()
        self.transmitter = Transmitter()
        self.command_analyzer = CommandAnalyzer()
        self.command_executor = CommandExecutor()

    def start_all_threads(self):
        self.receiver.start_rx_thread()
        self.transmitter.start_tx_thread()
        self.command_analyzer.start_analyzer_thread()
        self.command_executor.start_executor_thread()

    def stop_all_threads(self):
        self.receiver.stop_rx_thread()
        self.transmitter.stop_tx_thread()
        self.command_analyzer.stop_analyzer_thread()
        self.command_executor.stop_executor_thread()

    def get_thread_pid(self, thread_name):
        current_os = platform.system()
        if current_os == 'Linux':
            return self.get_thread_pid_linux(thread_name)
        elif current_os == 'Windows':
            return self.get_thread_pid_windows(thread_name)
        else:
            raise NotImplementedError(f"Unsupported OS: {current_os}")

    def get_thread_pid_linux(self, thread_name):
        cmd = f"pgrep -f {thread_name}"
        result = os.popen(cmd).read()
        return int(result.strip()) if result else None

    def get_thread_pid_windows(self, thread_name):
        import psutil
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] == 'python.exe' and thread_name in proc.info['cmdline']:
                return proc.info['pid']


if __name__ == "__main__":
    manager = Manager()
    manager.start_all_threads()

    # print(f"Receiver PID: {manager.get_thread_pid('ReceiverThread')}")
    time.sleep(100)

    #print(f"Analyzer PID: {manager.get_thread_pid('AnalyzerThread')}")
    #print(f"Executor PID: {manager.get_thread_pid('ExecutorThread')}")
