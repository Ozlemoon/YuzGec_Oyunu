import cx_Freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('yuzgec.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "Yüz-Geç App",
    options = {"build_exe" : 
        {"packages" : ["pygame"], "include_files" : ['C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/background.gif',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/background3.webp',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/background23.jpg',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/bag.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/food.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/heart.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/high_score.txt',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/message.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/sprite_0.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/sprite_1.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/sprite_2.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/sprite_3.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/sprite_4.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/sprite_5.png',
                                                     'C:/Users/melik/OneDrive/Masaüstü/Yuz-Geç_Melike_Ozlem/sprite_6.png'
                                                     ]}},
    executables = executables
)