import json	
import sys
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import subprocess
import json
import getopt

from functools import partial

sys.path.append('../')  

from resources.config import init_setup
from resources.control import * #many of these functions are imported for debug purposes.
from resources.utils import serFlush, reg_data_to_int
from resources.fuse_constants import *

ser_name = "/dev/ttyUSB0"
BAUD = 115200
component_name = "20-U-PG-OB-2400000"
lpGBT_list = []
# component_name = "optoboar"


# debug = False 

#Sets up the serial communication with the Arduino
# ser = init_setup(BAUD, ser_name)

#==========================================================

class Textbox:
	def __init__(self, frame, name, inittext, width):
		self.label = ttk.Label(frame,text=name, anchor='center')
		self.name_var = tk.StringVar(master=frame)
		self.entry = tk.Entry(master=frame,width=width, textvariable=self.name_var, font="liberation 9")
		self.entry.insert(0, inittext)

	def put(self,side='top'):
		self.label.pack(side=side,expand=1,fill='x')
		self.entry.pack(side=side,expand=1,pady='0.1i  ')

	def remove(self):
		self.label.pack_forget()
		self.entry.pack_forget()

	def write(self, text):
		self.entry.delete(0, 'end')
		self.entry.insert(0, text)

	def getEntry(self):
		return self.entry

	def getText(self):
		print(self.entry.get())
		return self.entry.get()

class Buttonbox:
	def __init__(self,frame, text, com):
		self.button = ttk.Button(
			master=frame,
			text=text,
			padding='0.1i',
    		command = com
		)
	def put(self,side='bottom'):
		self.button.pack(side= side,expand=1)

	def getButton(self):
		return self.button

class Dropdown:
	def __init__(self,frame,options):
		self.item = tk.StringVar(frame)
		self.item.set(options[0])
		self.opt_item = ttk.OptionMenu(frame, self.item, options[0], *options)
		self.opt_item.config(width=20)

	def getCurrent(self):
		return self.item

	def getElement(self):
		return self.opt_item

def createFrame(master):
	temp = ttk.Frame(master=master,padding='0.2i')
	return temp

#==========================================================

def main():
	global initiation
	global ser_name
	global component_name
	global lpGBT_list



	# lpGBT_list = load_lpGBT_list(component_name)

	main_panel = tk.Tk()

	s = ttk.Style()
	s.theme_use('alt') # select the Unix alt theme
	s.configure(style='TButton', background='green')
	s.configure(style='.', font=('fixed',9))
	s.configure(style='Head.TLabel', font=('fixed',12, 'underline'))
	# print(font.families())

	# Possible fonts for CentOS:
	# ('fixed', 'urw palladio l', 'courier 10 pitch', 'bitstream charter', 'nimbus roman no9 l', 'liberation sans', 'liberation sans narrow', 'nimbus sans l', 'urw gothic l', 'century schoolbook l', 'urw bookman l', 'utopia', 'liberation mono', 'liberation serif', 'nimbus mono l', 'dingbats', 'cursor', 'standard symbols l', 'urw chancery l')
	# Possible fonts for Ubuntu:
	# ('texgyretermes', 'fangsong ti', 'fixed', 'clearlyu alternate glyphs', 'latin modern roman', 'courier 10 pitch', 'open look glyph', 'texgyrechorus', 'latin modern typewriter', 'bitstream charter', 'song ti', 'open look cursor', 'newspaper', 'texgyrecursor', 'clearlyu ligature', 'mincho', 'clearlyu devangari extra', 'clearlyu pua', 'texgyreheros', 'texgyrebonum', 'clearlyu', 'texgyreschola', 'latin modern typewriter variable width', 'latin modern sans', 'texgyreadventor', 'clean', 'nil', 'clearlyu arabic', 'clearlyu devanagari', 'texgyrepagella', 'latin modern sansquotation', 'gothic', 'clearlyu arabic extra')

	
	main_panel.title("E-Fuse software")
	
	for row in range(2):
		main_panel.rowconfigure(row,weight=1)
	for col in range(3):
		main_panel.columnconfigure(col,weight=1)
	

	frm_init = createFrame(main_panel)
	frm_write_single = createFrame(main_panel)
	frm_readout_single = createFrame(main_panel)
	frm_readout_mult = createFrame(main_panel)
	frm_fuse_full = createFrame(main_panel)
	frm_powering = createFrame(main_panel)

	create_init_panel(frm_init,frm_write_single,frm_readout_single,frm_readout_mult,frm_fuse_full,frm_powering)

	main_panel.mainloop()

#==========================================================

def create_init_panel(frm_init,frm_write_single,frm_readout_single,frm_readout_mult,frm_fuse_full,frm_powering):
	for widget in frm_init.winfo_children():
		widget.destroy()

	header_init = ttk.Label(frm_init, text = "Initialisation panel", style='Head.TLabel')

	ent_ser = Textbox(frm_init,"Enter USB port name", "", 30)

	ent_comp = Textbox(frm_init,"Enter component name", "20-U-PG-OB-2400000", 30)

	var_ser = tk.IntVar()
	ck_ser = ttk.Checkbutton(frm_init, text="Manually enter USB port", variable=var_ser, onvalue=1, offvalue=0, command=partial(show_ent_ser, ent_ser, var_ser))

	header_init.pack(side='top',expand=1)
	ent_comp.put()
	ck_ser.pack(side='top',expand=1, pady='0.1i')
	frm_init.grid(row = 0, column = 0, sticky="NSEW")

	btn_connect = Buttonbox(frm_init,"initiate connection", com=partial(connect,ent_ser.getEntry(),ent_comp.getEntry(),frm_write_single,frm_readout_single,frm_readout_mult,frm_fuse_full,frm_powering))
	btn_connect.put()

def show_ent_ser(ent_ser,var_ser):
	print("Checkbox changed")
	if var_ser.get()==1:
		ent_ser.write("ttyUSB0")
		ent_ser.put()
	if var_ser.get()==0:
		ent_ser.write("")
		ent_ser.remove()


def connect(ser,comp,write_single,read_single,read_mult,fuse_full,powering):
	ser = ser.get()
	comp = comp.get()
	update(ser,comp)
	create_single_write_panel(write_single)
	create_single_readout_panel(read_single)
	create_mult_readout_panel(read_mult)
	create_fuse_panel(fuse_full)
	create_powering_panel(powering)
	print("setup complete")


def update(ser,comp):
	global ser_name
	global component_name
	global lpGBT_list

	print(ser)

	ser_name = "/dev/" + ser
	component_name = comp

	if ser=="":
		ser = init_setup(BAUD)
	else:
		ser = init_setup(BAUD, ser_name)

	lpGBT_list = load_lpGBT_list(comp)

#==========================================================

def create_single_readout_panel(frm_readout):
	for widget in frm_readout.winfo_children():
		widget.destroy()
	header_sr = ttk.Label(frm_readout, text = "Single register readout", style='Head.TLabel')
	drop_devices_read = Dropdown(frm_readout,lpGBT_list)
	ent_read_addr = Textbox(frm_readout,"Read specific addr: ", "0x1d7", 20)
	lbl_read_val = ttk.Label(master=frm_readout,text = "Value read: ")

	btn_read = Buttonbox(frm_readout,"read register", com=partial(read_execute, drop_devices_read.getCurrent(), ent_read_addr.getEntry(), lbl_read_val))

	header_sr.pack(side='top',expand=1)
	drop_devices_read.getElement().pack(side='top',expand=1)
	ent_read_addr.put()
	btn_read.put()
	lbl_read_val.pack(side='bottom',expand=1)

	frm_readout.grid(row=0,column=1,sticky="NSEW")

def read_execute(lpGBT, addr, value_lbl):
	lpGBT = lpGBT.get()
	addr = addr.get()
	value = read_reg(lpGBT,int(addr,0))
	print(value)
	value_lbl["text"] = "Value read: " + f"{hex(value)}"

#==========================================================
		
def create_mult_readout_panel(frm_readout_mult):
	for widget in frm_readout_mult.winfo_children():
		widget.destroy()
	header_mr = ttk.Label(master=frm_readout_mult, text = "Multiple register readout", style='Head.TLabel')
	drop_devices_read_mult = Dropdown(frm_readout_mult,lpGBT_list)
	ent_read_first = Textbox(frm_readout_mult,"Starting at register: ", "0x000", 20)
	ent_read_amount = Textbox(frm_readout_mult, "Amount of registers to read out", "20", 20)
	frm_results = ttk.Frame(master=frm_readout_mult)


	btn_start_readout = Buttonbox(frm_readout_mult,"read register", com=partial(read_execute_mult, drop_devices_read_mult.getCurrent(), ent_read_first.getEntry(), ent_read_amount.getEntry(), frm_results))

	header_mr.pack(side='top',expand=1)
	drop_devices_read_mult.getElement().pack(side='top',expand=1)
	ent_read_first.put()
	ent_read_amount.put()
	btn_start_readout.put()
	frm_results.pack(side='bottom',expand=1)

	frm_readout_mult.grid(row=1,column=1,sticky="NSEW")

def read_execute_mult(lpGBT,reg_first,reg_amount,frame):
	lpGBT = lpGBT.get()
	reg_first = reg_first.get()
	reg_amount = int(reg_amount.get(),0)
	for widget in frame.winfo_children():
		widget.destroy()
	start = int(reg_first,0)
	stop = int(reg_first,0)+reg_amount
	lbl_read_val = []
	
	canvas = tk.Canvas(frame, width=200)
	scroller = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
	subframe = ttk.Frame(master=canvas)
	subframe.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
	canvas.create_window((0,0), window=subframe, anchor="nw")
	canvas.configure(yscrollcommand=scroller.set)
	
	for reg in range(start,stop):
		value = read_reg(lpGBT,reg)
		print(value)
		lbl_read_val.append(ttk.Label(master=subframe,text = "Register: "+ f"{hex(reg)}" +" Value read: " + f"{hex(value)}",background='white', anchor='w'))
		lbl_read_val[reg-start].pack(fill='both')
	canvas.pack(side="left",fill="both", expand=1)
	scroller.pack(side="right", fill="y", expand=1)
	
		


#==========================================================

def create_single_write_panel(frm_write):
	for widget in frm_write.winfo_children():
		widget.destroy()
	header_sw = ttk.Label(master=frm_write, text = "Single register write", style='Head.TLabel')
	drop_devices_write = Dropdown(frm_write,lpGBT_list)
	ent_write_addr = Textbox(frm_write,"Write to Address: ", "0x000", 20)
	ent_write_val = Textbox(frm_write, "Write value: ", "0x00", 20)
	lbl_write_val = ttk.Label(master=frm_write,text = "Value readback: ")

	btn_write = Buttonbox(frm_write,"write register", com=partial(write_execute, drop_devices_write.getCurrent(), ent_write_addr.getEntry(), ent_write_val.getEntry(), lbl_write_val))

	header_sw.pack(side='top',expand=1)
	drop_devices_write.getElement().pack(side='top',expand=1)
	ent_write_addr.put()
	ent_write_val.put()
	btn_write.put()
	lbl_write_val.pack(side='bottom',expand=1)

	frm_write.grid(row=1,column=0,sticky="NSEW")

def write_execute(lpGBT, addr, write_val, value_lbl):
	lpGBT = lpGBT.get()
	addr = addr.get()
	write_val = write_val.get()
	value = write_read_reg_wrapper(lpGBT,int(addr,0),int(write_val,0))
	print(value)
	value_lbl["text"] = "Value readback: " + f"{hex(value)}"


#==========================================================

def create_fuse_panel(frm_fuse):
	for widget in frm_fuse.winfo_children():
		widget.destroy()
	header_f = ttk.Label(master=frm_fuse, text = "E-Fusing", style='Head.TLabel')
	ent_fuse_file = Textbox(frm_fuse, "Select Your fuse file \n(be sure to include the relative path to the file)", "/../script/",40)
	btn_fuse = Buttonbox(frm_fuse, "fuse on Optoboard", com=partial(fuse_full, lpGBT_list, ent_fuse_file.getEntry()))

	header_f.pack(side='top',expand=1)
	ent_fuse_file.put()
	btn_fuse.put()

	frm_fuse.grid(row=0,column=2,sticky="NSEW")

def fuse_full(lpGBT_list,fuse_path):
	with open(os.getcwd() + fuse_path.get()) as g:
		fuse_list = json.load(g)
	#print(lpGBT_list)
	#print(fuse_list)
	full_fuse(lpGBT_list,fuse_list)


#==========================================================

def togglePower(button):
    
    if button.config('text')[-1] == 'E-Fuser Power ON':
        button.config(text='E-Fuser Power OFF')
        switchPower('off')
    else:
        button.config(text='E-Fuser Power ON')
        switchPower('on')

def toggleBootCNF(button):
    
    if button.config('text')[-1] == 'BOOTCNF0 Power ON':
        button.config(text='BOOTCNF0 Power OFF')
        switchBootCNF('off')
    else:
        button.config(text='BOOTCNF0 Power ON')
        switchBootCNF('on')

def create_powering_panel(frm_powering):
	for widget in frm_powering.winfo_children():
		widget.destroy()
	header_f = ttk.Label(master=frm_powering, text = "Power Handling", style='Head.TLabel')

	btn_power = Buttonbox(frm_powering, "E-Fuser Power ON", com=None)
	btn_power.getButton().config(command=partial(togglePower,btn_power.getButton()))
	btn_bootcnf = Buttonbox(frm_powering, "BOOTCNF0 Power ON", com=None)
	btn_bootcnf.getButton().config(command=partial(toggleBootCNF,btn_bootcnf.getButton()))

	header_f.pack(side='top',expand=1)
	btn_power.put(side='top')
	btn_bootcnf.put(side='top')

	frm_powering.grid(row=1,column=2,sticky="NSEW")


main()



