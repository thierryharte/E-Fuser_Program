
# efusing procedure addresses
FUSEBLOWADDH = 0x011e
FUSEBLOWADDL = 0x011f
FUSECONTROL = 0x0119
FUSEMAGIC = 0x0120
FUSECONTROL_FUSEBLOWPULSELENGTH_of = 4
FUSECONTROL_FUSEREAD_bm = 0x02
FUSECONTROL_FUSEBLOW_bm = 0x01
FUSEBLOWDATAA = 0x011a
FUSEBLOWDATAB = 0x011b
FUSEBLOWDATAC = 0x011c
FUSEBLOWDATAD = 0x011d
FUSE_MAGIC_NUMBER = 0xA3
FUSESTATUS = 0x01b1
FUSESTATUS_FUSEBLOWERROR_bm = 0x08
FUSESTATUS_FUSEDATAVALID_bm = 0x04
FUSESTATUS_FUSEBLOWDONE_bm = 0x02
FUSESTATUS_FUSEBLOWBUSY_bm = 0x01
FUSEVALUESA = 0x01b2
FUSEVALUESB = 0x01b3
FUSEVALUESC = 0x01b4
FUSEVALUESD = 0x01b5

PUSMSTATUS = 0x01c7

STATE_WAIT_POWER_GOOD = 7

I2CM0CONFIG = 0x00f0