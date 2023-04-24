import numpy as np


#serial definitions
port = 'COM3'
baudrate = 115200

#Data as the program handles
SHperiod = np.uint32(100)
ICGperiod = np.uint32(100000)
AVGn = np.uint8([0, 1])
MCLK = 2000000
SHsent = SHperiod
ICGsent = ICGperiod
stopsignal = 0

#Data arrays for received bytes
#rxFullData8 = np.zeros((2, 7388), np.uint8)
rxFullData8 = [None, None]
rxFullData16 = np.zeros((2, 3694), np.uint16)
pltFullData16 = np.zeros((2, 3694), np.uint16)


#Arrays for data to transmit
txsh = np.uint8([0,0,0,0]) 
txicg = np.uint8([0,0,0,0])
txfull = np.uint8([0,0,0,0,0,0,0,0,0,0,0,0])

#Invert data
datainvert = 1
offset = 0
balanced = 0

#Oksanichenko_Fedor

#Vovchara&Arsenii prak

#E4_ampl_var = 1
#E4_delta_var = 2.1
#E4_smesch_var = 0
#E4_alpha_var = 1
#E4_l0_var = 10

E4_ampl_var = 500
E4_delta_var = 0.0003
E4_smesch_var = 0.006
E4_alpha_var = 0.01
E4_l0_var = 7*10**(-5)

E4_fun_arr = []
x_lim = [-1000, 5000]
is_plotting = False

#Info for cursor
push_down = False
updating_for_cursor = False
what_push = "none"
l_col = "r"
r_col = "r"
b_col = "r"
norm_val = 1
act_val = 2
l_lw = norm_val
r_lw = norm_val
b_lw = norm_val
crit_delta = 30



#Info for plot
already_started = False
already_started_left = False
already_started_right = False
already_started_bot = False
num_plots = 2
is_make_spec = 0
num_pixels = 3694

first_norm_pixel = 32

intence_x0 = 1000
intence_x1 = 3000
bottom_bound = 0
max_bottom_bound = 2000

curr_checking = 0

drawed_first = 0
drawed_second = 0
to_draw_divided = 0
num_divided = 0

data = [[], [], [[], []]]



number_saving = 0
number_loading = 0
number_collecting = 0
is_draw_second = 0
is_clever_cursor = 0
plot_width = 0.0
plot_height = 0.0

data_inv_axis = [0, 3694, -10, 2250]
data_not_inv_axis = [0, 3694, -10, 4095]

min_intens_value = 100
max_intens_div = 10.0

is_correct_spec_param = 0

pixels = np.array([100,200,300])
wave_lenghts = np.array([100,200,300])
k = 1.0
b = 0