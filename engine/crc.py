#coding=utf-8
'''
import crcmod
import binascii
import traceback

def caculate_crc( _data ):
    try:
        hexData = binascii.a2b_hex(_data)
        xorOut_ty=0x0000
        rev_ty=False
        initCrc_ty=0xffff
        xmodem_crc_func = crcmod.mkCrcFun(0x11021, rev=rev_ty, initCrc=initCrc_ty, xorOut=xorOut_ty)        
        return [ True,hex(xmodem_crc_func(hexData)) ]
    except Exception,e:
        print Exception,":",e
        traceback.print_exc()
        return [ False, None]
    
    
    '''

'''
aim='1ae3601401ae360'
hexData = binascii.a2b_hex(aim)
print aim,hexData
xorOut_ty=0x0000
rev_ty=False
initCrc_ty=0xffff
xmodem_crc_func = crcmod.mkCrcFun(0x11021, rev=rev_ty, initCrc=initCrc_ty, xorOut=xorOut_ty)
print rev_ty,hex(initCrc_ty),hex(xorOut_ty)
print aim,'\t',hex(xmodem_crc_func(hexData))

print caculate_crc("1ae3601401ae360")'''
    
    
'''
[ret,value] = caculate_crc("1ae3601401ae3600")
print value'''