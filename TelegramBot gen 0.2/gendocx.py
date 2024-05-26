from docxtpl import DocxTemplate

def ralat_to_docx(title, n_ralat, data, x_bar, x_min_x_bar, x_min_x_bar_2, sum_x_min_x_bar_2, delta_x1, delta_x, rn1, rn, rk):
    # Data untuk diisi ke dalam template
    context = {
        'title' : title,
        'n_ralat': n_ralat,
        'n_data': data,
        'data': data,
        'x_bar': x_bar,  # Contoh nilai rata-rata
        'x_min_x_bar': x_min_x_bar,
        'x_min_x_bar_2': x_min_x_bar_2,
        'sum_x_min_x_bar_2': sum_x_min_x_bar_2,
        'delta_x1': delta_x1,
        'delta_x': delta_x,
        'rn1': rn1,
        'rn': rn,
        'rk': rk
    }

    # Membaca template
    template = DocxTemplate('./template.docx')

    # Mengisi template dengan data
    template.render(context)

    # Menyimpan dokumen yang telah diisi
    template.save(f'{title}.docx')