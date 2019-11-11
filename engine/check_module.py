#! encoding=utf-8
from tornado import gen
from data import dataCenter
from serial_enquiry import enquiry, modify_str
from parsor import generate
from loggers import elogger, rlogger, rlog, elog
from time import time

def check_module(ser, codes):
    "掉线了应该返回None. 同时返回(raw_a,b,c,用于判断是否有上下线。"
    code_a, code_b, code_c,code_d = codes
    t1=time()
    raw_a = enquiry(ser, code_a,79)
    t2=time()
    raw_b = enquiry(ser, code_b,221)
    t3=time()
    raw_c = enquiry(ser, code_c,53)
    t4=time()
    raw_d=enquiry(ser,code_d,113)
    t5=time()
    json_info = generate(raw_a, raw_b, raw_c,raw_d)
    print("time consumed respectively:",t2-t1,t3-t2,t4-t3,t5-t4)
    print("total time consumed:",t5-t1)

    return json_info
