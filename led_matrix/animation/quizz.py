#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import json
import socket
import queue
from threading import Thread
import select

from led_matrix.fonts.font4x5 import Font4x5
from led_matrix.fonts.adafruit import *
from led_matrix.animation.animation import ScrollText,Application,ProgressBar,Bar


class Quizz(ScrollText):

    def __init__(self,conf,*args,**kargs):
        super().__init__(*args,**kargs)
        self.load_conf(conf)

    def load_conf(self,conf):
        with open(conf,"r") as f:
            self.quizz = json.load(f)

    def set_text(self):
        problem = random.choice(self.quizz)
        question = eval(problem["question"])
        return question


class NetworkThread(Thread):
    def __init__(self,queue,port=64241):
        super().__init__()
        self.port = port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.need_stop = False
        self.queue = queue

    def init(self):
        self.sock.bind(("0.0.0.0",self.port))

    def run(self):
        self.init()
        while not self.need_stop:
            ready = select.select([self.sock], [], [], 1)
            if ready[0]:
                data = self.sock.recv(4096)
                self.queue.put(data,False)

    def stop(self):
        self.need_stop = True


class NetQuizz(Application):
    def __init__(self,conf=None,port=64241,timeout=5,wait_timeout=True,max_size_answser=None,*args,**kargs):
        super().__init__(refresh=1,*args,**kargs)
        self.timeout = timeout
        self.queue = queue.Queue(maxsize=10)
        self.net_thread = NetworkThread(self.queue,port)
        self.net_thread.start()
        self.question = None
        self.max_size_answser = max_size_answser
        self.wait_timeout = wait_timeout
        self.question_screen = self.screen.extract_screen(0,0,22,self.screen.height)
        self.answer_screen = self.screen.extract_screen(22,0,10,self.screen.height)
        if conf:
            self.load_conf(conf)

    def load_conf(self,conf):
        with open(conf,"r") as f:
            self.quizz = json.load(f)

    def stop(self):
        super().stop()
        self.net_thread.stop()

    def print_text(self,text,screen,color=0xFFFFFF,render=True,font=Font4x5()):
        screen.fill(self.screen.DEFAULT_COLOR)
        screen.center_text(text,color,font=font)
        if render: screen.render()

    def clear_old_answer(self):
        while not self.queue.empty():
            try:
                self.queue.get(False)
            except queue.Empty:
                return
        return

    def set_question(self):
        self.question,self.answer = self.get_problem()
        self.print_text(self.question,self.question_screen,render=False)
        self.print_text("",self.answer_screen,render=False)
        self.clear_old_answer()
        self.screen.render()

    def validate_answer(self,answer):
        if self.is_valid_answer(answer):
            self.set_right()
        else:
            self.set_wrong()

    def is_valid_answer(self,answer):
        if type(self.answer) is int:
            try:
                answer = int(answer)
            except ValueError:
                return False
        return self.answer == answer

    def update(self):
        if not self.question:
            self.set_question()
        else:
            answer = self.get_answser()
            self.question = None
            self.validate_answer(answer)
            self.set_question()
        
    def get_problem(self):
        problem = random.choice(self.quizz)
        question = eval(problem["question"])
        answer = eval(problem["answer"]) if "answer" in problem else None
        return question,answer

    def get_answser(self):
        remaining_time = self.timeout
        answser = b""
        while True:
            try:
                start = time.time()
                ans = self.queue.get(timeout=remaining_time).strip()
            except queue.Empty:
                return answser
            else:
                answser += ans
                self.print_text(answser.decode("utf-8"),self.answer_screen,color=0xFF)
                if (not self.wait_timeout and self.is_valid_answer(answser)) or (self.max_size_answser and len(answser) == self.max_size_answser):
                    return answser
                remaining_time -= int(time.time()-start)

    def set_right(self):
        self.print_text("OK",self.screen,color=0xFF00,font=AdaFruit())
        time.sleep(1)

    def set_wrong(self):
        self.print_text("NOK",self.screen,color=0xFF0000,font=AdaFruit())
        time.sleep(1)


class Challenge(NetQuizz):
    def __init__(self,good_response=6,timeout=10,decrease=1,*args,**kargs):
        super().__init__(timeout=timeout,*args,**kargs)
        self.question_screen = self.screen.extract_screen(0,0,22,self.screen.height-2)
        self.answer_screen = self.screen.extract_screen(22,0,10,self.screen.height-2)
        self.bar_screen = self.screen.extract_screen(0,6,self.screen.width,2)
        self.progress_bar = ProgressBar(self.screen.extract_screen(3,6,16,1),good_response)
        self.bad_response_needed = 2
        self.error_bar = ProgressBar(self.screen.extract_screen(20,6,self.bad_response_needed-1,1),self.bad_response_needed,color=0xFF0000)
        self.level = 1
        self.lvl_bar = Bar(self.screen.extract_screen(22,6,10,1),color=0xFFFF00)
        self.lvl_bar.update(self.level)
        self.good_response_needed = good_response
        self.decrease = decrease
        self.reset_counter()

    def reset_counter(self):
        self.current_good = 0
        self.current_error = 0
        self.progress_bar.update(self.current_good)
        self.error_bar.update(self.current_error)

    def increase_level(self):
        self.level += 1
        self.timeout -= self.decrease
        self.print_text("LvL %u" % self.level,self.screen,color=0xFFFF00)
        self.lvl_bar.update(self.level)
        self.reset_counter()
        time.sleep(1)

    def decrease_level(self):
        self.level -= 1
        self.timeout += self.decrease
        self.print_text("LvL %u" % self.level,self.screen,color=0xFFFF00)
        self.lvl_bar.update(self.level)
        self.reset_counter()
        time.sleep(1)

    def refresh_bars(self):
        self.bar_screen.fill(0) # Needed because bars does not take full space
        self.progress_bar.update(self.current_good)
        self.error_bar.update(self.current_error)
        self.lvl_bar.update(self.level)

    def set_right(self):
        super().set_right()
        self.current_good += 1
        self.refresh_bars()
        if self.current_good == self.good_response_needed:
            time.sleep(1)
            self.increase_level()

    def set_wrong(self):
        super().set_wrong()
        self.current_error += 1
        self.refresh_bars()
        if self.current_error == self.bad_response_needed:
            time.sleep(1)
            self.decrease_level()

