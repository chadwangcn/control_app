#coding=utf-8

import crcmod
import binascii
import traceback

'''
32bit align value:
1a -- >  0000001a
'''
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
Ts(start)  -- > Te(end)  ---> S1(Sloop)  ---> T (Hold Time)


import crcmod
import binascii
aim='0000000A000000140000001E00000004000000140000001E0000001E000000040000001E000000280000001E00000004000000320000003C0000001E00000004'
hexData = binascii.a2b_hex(aim)
print aim,hexData
xorOut_ty=0x0000
rev_ty=False
initCrc_ty=0xffff
xmodem_crc_func = crcmod.mkCrcFun(0x11021, rev=rev_ty, initCrc=initCrc_ty, xorOut=xorOut_ty)
print rev_ty,hex(initCrc_ty),hex(xorOut_ty)
print aim,'\t',hex(xmodem_crc_func(hexData))

print caculate_crc(aim)
'''
