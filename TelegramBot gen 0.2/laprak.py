import random
from gendocx import ralat_to_docx

def ralat(DATA, n, nol_blkng_koma):
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
        delta_x1 = n * (n - 1)
        delta_x = (sum_x_min_x_bar_2 / delta_x1)**0.5
    else:
        delta_x = 0.5
    
    # Calculate relative error percentage rn and its complement rk
    rn1 = (delta_x / x_bar)
    rn =  rn1 * 100 if x_bar != 0 else 0
    rk = 100 - rn
    
    # Format all results to the specified number of decimal places
    x_bar = f'{x_bar:.{u}f}'
    x_min_x_bar = [f'{x:.{u}f}' for x in x_min_x_bar]
    x_min_x_bar_2 = [f'{x:.{u}f}' for x in x_min_x_bar_2]
    sum_x_min_x_bar_2 = f'{sum_x_min_x_bar_2:.{u}f}'
    delta_x1 = f'{delta_x1:.{u}f}'
    delta_x = f'{delta_x:.{u}f}'
    rn1 = f'{rn1:.{u}f}'
    rn = f'{rn:.{u}f}'
    rk = f'{rk:.{u}f}'
    
    return DATA, x_bar, x_min_x_bar, x_min_x_bar_2, sum_x_min_x_bar_2, delta_x1, delta_x, rn1, rn, rk


def generate_variations_rk(number, n, u):
    variations = []
    deviasi_standar = 0.045
    x = number
    for i in range(n):
        batas_bawah = x - deviasi_standar * x
        batas_atas= x + deviasi_standar * x
        acak_x = random.uniform(batas_bawah, batas_atas)
        variations.append(acak_x)
    variations = [f'{x:.{u}f}' for x in variations]
    
    return variations

if __name__ == "__main__":
    DATA = [24.68145694216038, 24.551216359356392, 21.701681561587936, 28.247245499732866, 23.371544937468304, 21.83023989460634, 26.81355034616428, 22.14730322503657, 23.88717167181798, 23.569082138645754]
    n = len(DATA)
    nol_blkng_koma = 4

    result = ralat(DATA, n, nol_blkng_koma)
    for label, value in zip(["DATA", "x_bar", "x_min_x_bar", "x_min_x_bar_2", "sum_x_min_x_bar_2", "delta_x1", "delta_x", "rn1", "rn", "rk"], result):
        print(f"{label}: {value}")