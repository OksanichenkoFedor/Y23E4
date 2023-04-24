import numpy as np
import scipy.special as sc
import config


def count_wave():
    count_pure()
    X = config.pixels
    Y = config.wave_lenghts
    X2 = X * X
    XY = X * Y
    k = (XY.mean() - (X.mean()) * (Y.mean())) / (X2.mean() - X.mean() ** 2)
    b = Y.mean() - k * (X.mean())
    config.k = k
    config.b = b

    for i in range(3):
        for j in range(len(config.data[i][0])):
            config.data[i][0][j] = k*config.data[i][0][j] + b


def count_pure():
    for i in range(2):
        config.data[i] = [[], []]
        for j in range(len(config.pltFullData16[i])):
            if j>config.first_norm_pixel:
                curr_val = config.pltFullData16[i][j]
                if config.pltFullData16[i][j] > 2200:
                    curr_val=0
                config.data[i][0].append(j)
                config.data[i][1].append(curr_val)
    if config.to_draw_divided == 1:
        if config.num_divided == 0:
            co_one_two()
        else:
            co_two_one()

def co_one_two():
    config.num_divided = 0
    x = []
    y = []
    ind1 = 0
    ind2 = 0
    cont = True
    while cont:
        if config.data[0][0][ind1] < config.data[1][0][ind2]:
            ind1 += 1
            if ind1 >= len(config.data[0][0]):
                cont = False
        elif config.data[0][0][ind1] > config.data[1][0][ind2]:
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
        else:
            new_y = (1.0 * config.data[0][1][ind1]) / (1.0 * config.data[1][1][ind2])
            if ((1.0 * config.data[1][1][ind2]) >= config.min_intens_value) and (new_y<config.max_intens_div):
                x.append(config.data[0][0][ind1])
                y.append(new_y)
            ind1 += 1
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
            if ind1 >= len(config.data[0][0]):
                cont = False

    config.data[2] = [x, y]
    config.to_draw_divided = 1

def count_intence():
    res = 0
    for i in range(len(config.data[0][0])):
        if config.data[0][0][i] > config.intence_x0 and config.data[0][0][i] < config.intence_x1 and config.data[0][1][i] > config.bottom_bound:
            res+=config.data[0][1][i]-config.bottom_bound
    return str(round(res/10000.0, 3))

def co_two_one():
    config.num_divided = 1
    x = []
    y = []
    ind1 = 0
    ind2 = 0
    cont = True
    while cont:
        if config.data[0][0][ind1] < config.data[1][0][ind2]:
            ind1 += 1
            if ind1 >= len(config.data[0][0]):
                cont = False
        elif config.data[0][0][ind1] > config.data[1][0][ind2]:
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
        else:
            new_y = (1.0 * config.data[1][1][ind2]) / (1.0 * config.data[0][1][ind1])
            if ((1.0 * config.data[0][1][ind1]) >= config.min_intens_value) and (new_y<config.max_intens_div):
                x.append(config.data[0][0][ind1])
                y.append(new_y)
            ind1 += 1
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
            if ind1 >= len(config.data[0][0]):
                cont = False

    config.data[2] = [x, y]
    config.to_draw_divided = 1

def make_fun_arr(curr_fun):
    config.E4_fun_arr = [[], []]
    config.E4_fun_arr[0] = np.arange(config.x_lim[0],config.x_lim[1]+1)

    config.E4_fun_arr[1] = curr_fun(config.E4_ampl_var, config.E4_delta_var, config.E4_smesch_var,
                                    config.E4_alpha_var, config.E4_l0_var, config.E4_fun_arr[0])
    #print(config.E4_fun_arr[1])
    #print(config.E4_ampl_var)
    #print(config.E4_delta_var)
    #print(config.E4_smesch_var)
    #print(config.E4_alpha_var)
    #print(config.E4_l0_var)


def frenel_fun(A,d,y_0,alpha,L0,i):
    return (A*1000*np.sin(i*alpha*0.01+y_0)**2)/d


def intensityCalculation(A, d, y0, alpha, L0, pixelArray):
    coordArray = pixelArray*(0.038/3700)
    argArray1 = ((2/np.pi)**0.5/L0) *(d + alpha*y0) -((2/np.pi)**0.5/L0)*alpha*coordArray
    argArray2 = ((2/np.pi)**0.5/L0)*alpha*y0 - ((2/np.pi)**0.5/L0)*alpha*coordArray
    S1, C1 = sc.fresnel(argArray1)
    S2, C2 = sc.fresnel(argArray2)
    S = np.square(S1 - S2)
    C = np.square(C1 - C2)
    return A*(S + C)
