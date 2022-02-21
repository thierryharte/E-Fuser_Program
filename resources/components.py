# nested dictionary with all component and device addresses
# author: Roman Mueller

components = {
	### Optoboard V0s
	"optoboard_001": {
		"serial": "001",
		"optoboard_v": 0,
		"component_type": "lpGBT_master",
		"dev_addr": 0x7f
	},

	"optoboard_002": {
		"serial": "002",
		"optoboard_v": 0,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x7e,
		"efused": 0
	},

	"optoboard_003": {
		"serial": "003",
		"optoboard_v": 0,
		"component_type": "lpGBT_master",
		"dev_addr": 0x7d,
		"efused": 0
	},

	"optoboard_004": {
		"serial": "004",
		"optoboard_v": 0,
		"component_type": "lpGBT_master",
		"dev_addr": 0x7c,
		"efused": 0
	},

	"optoboard_005": {
		"serial": "005",
		"optoboard_v": 0,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x70,
		"efused": 0
	},

	"optoboard_006": {
		"serial": "006",
		"optoboard_v": 0,
		"component_type": "lpGBT_master",
		"dev_addr": 0x70,
		"efused": 0
	},

	"optoboard_007": {
		"serial": "007",
		"optoboard_v": 0,
		"component_type": "lpGBT_master",
		"dev_addr": 0x7f,
		"efused": 0
	},

	### Optoboard V1/V2 serials and their devices attached
	"1_1_001": {
		"optoboard_v": 1,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 0,
		"GBCR2": 0,
		"GBCR3": 0,
		"GBCR4": 0,
		"efused": 0
	},

	"1_1_002": {
		"optoboard_v": 1,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0
	},
	"1_1_003": {
		"optoboard_v": 1,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0
	},
	"1_1_004": {
		"optoboard_v": 1,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0
	},
	"1_1_005": {
		"optoboard_v": 1,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0
	},

	# components on Optoboard V2
	"08000000": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0
	},
	"524d0001": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 0,
		"lpGBT3": 0,
		"lpGBT4": 0,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0,
		"I2C_master": 0
	},
	"524d0002": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 0,
		"lpGBT3": 1,
		"lpGBT4": 0,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 1,
		"I2C_master": 0
	},
	"524d0003": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 0,
		"lpGBT3": 0,
		"lpGBT4": 0,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 1,

		"I2C_master": 2
	},
	"524d0004": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 0,
		"lpGBT3": 1,
		"lpGBT4": 0,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 1,
		"I2C_master": 2
	},
	"524d0005": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 0,
		"lpGBT3": 0,
		"lpGBT4": 0,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 1,
		"I2C_master": 0
	},
	"524d0006": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 0,
		"lpGBT3": 1,
		"lpGBT4": 0,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 1,
		"I2C_master": 2
	},
	"524d0007": {
		"optoboard_v": 2,
		"lpGBT1": 1,
		"lpGBT2": 0,
		"lpGBT3": 0,
		"lpGBT4": 0,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 1,
		"I2C_master": 2
	},

# components on Optoboard V21
	"20-U-PG-OB-2400000" : {
		"optoboard_v": 3,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0
	},

	"20-U-PG-OB-2400001" : {
		"optoboard_v": 3,
		"lpGBT1": 1,
		"lpGBT2": 1,
		"lpGBT3": 1,
		"lpGBT4": 1,
		"GBCR1": 1,
		"GBCR2": 1,
		"GBCR3": 1,
		"GBCR4": 1,
		"efused": 0
	},


# lpGBTs V1
	"V1_lpGBT1_master": {
		"optoboard_v":  1,
		"component_type": "lpGBT_master",
		"dev_addr": 0x74
	},
	"V1_lpGBT2_slave": {
		"optoboard_v":  1,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x75
	},
	"V1_lpGBT3_slave": {
		"optoboard_v":  1,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x76
	},
	"V1_lpGBT4_slave": {
		"optoboard_v":  1,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x77
	},

	# lpGBTs V2
	"V2_lpGBT1_master": {
		"optoboard_v":  2,
		"component_type": "lpGBT_master",
		"dev_addr": 0x70
	},
	"V2_lpGBT2_slave": {
		"optoboard_v":  2,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x75
	},
	"V2_lpGBT3_slave": {
		"optoboard_v":  2,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x76
	},
	"V2_lpGBT4_slave": {
		"optoboard_v":  2,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x77
	},

	# lpGBTs V21
	"V3_lpGBT1_master": {
		"optoboard_v":  3,
		"component_type": "lpGBT_master",
		"dev_addr": 0x74
	},
	"V3_lpGBT2_slave": {
		"optoboard_v":  3,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x75
	},
	"V3_lpGBT3_slave": {
		"optoboard_v":  3,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x76
	},
	"V3_lpGBT4_slave": {
		"optoboard_v":  3,
		"component_type": "lpGBT_slave",
		"dev_addr": 0x77
	},

	# GBCRs, dev_addr of components should be the same for all V1/V2
	"GBCR1": {
		"component_type": "GBCR",
		"dev_addr": 0x20
	},
	"GBCR2": {
		"component_type": "GBCR",
		"dev_addr": 0x21
	},
	"GBCR3": {
		"component_type": "GBCR",
		"dev_addr": 0x22
	},
	"GBCR4": {
		"component_type": "GBCR",
		"dev_addr": 0x23
	},

	# VTRx+
	"VTRxPlus": {
		"component_type": "VTRxPlus",
		"dev_addr": 0x50				# same for all
	}

}
