import random

def ralat_typ1(DATA, n, nol_blkng_koma):
    u = int(nol_blkng_koma)
    # Calculate the mean of DATA
    x_bar = sum(DATA) / n
    
    # Calculate (DATA - x_bar) and (DATA - x_bar)^2
    x_min_x_bar = []
    x_min_x_bar_2 = []
    
    for i in range(n):
        x = DATA[i] - x_bar
        x_min_x_bar.append(x)
        x_min_x_bar_2.append(x**2)
    
    # Calculate the sum of (DATA - x_bar)^2
    sum_x_min_x_bar_2 = sum(x_min_x_bar_2)
    
    # Calculate the standard deviation (or error) delta_x
    if n > 1:
        delta_x = (sum_x_min_x_bar_2 / (n * (n - 1)))**0.5
    else:
        delta_x = 0.5
    
    # Calculate relative error percentage rn and its complement rk
    rn = (delta_x / x_bar) * 100 if x_bar != 0 else 0
    rk = 100 - rn
    
    # Format all results to the specified number of decimal places
    x_bar = f'{x_bar:.{u}f}'
    x_min_x_bar = [f'{x:.{u}f}' for x in x_min_x_bar]
    x_min_x_bar_2 = [f'{x:.{u}f}' for x in x_min_x_bar_2]
    sum_x_min_x_bar_2 = f'{sum_x_min_x_bar_2:.{u}f}'
    delta_x = f'{delta_x:.{u}f}'
    rn = f'{rn:.{u}f}'
    rk = f'{rk:.{u}f}'
    
    return DATA, x_bar, x_min_x_bar, x_min_x_bar_2, sum_x_min_x_bar_2, delta_x, rn, rk


def generate_variations_rk(number, n, u):
    variations = []
    deviasi_standar = 0.065
    x = number
    for i in range(n):
        batas_bawah = x - deviasi_standar * x
        batas_atas= x + deviasi_standar * x
        acak_x = random.uniform(batas_bawah, batas_atas)
        variations.append(acak_x)
    variations = [f'{x:.{u}f}' for x in variations]
    
    return variations

if __name__ == "__main__":
    x = generate_variations_rk(10, 8, 3)
    print(x)