import datetime
class Ind:
    '''ставится в конец цикла и на вход принимает итерируемый объект для определения его длины'''
    i = 0
    def __init__(self, lst):
        if Ind.i == 0:
            Ind.start_time = datetime.datetime.now()
            Ind.length = len(lst)
        Ind.i += 1
        done = Ind.i
        total = Ind.length
        percent = (done / total * 100)
        time_diff = (datetime.datetime.now() - Ind.start_time).seconds
        time_dif = f"{time_diff // (60 * 60):03d} h {(time_diff - time_diff // (60 * 60) * 3600) // 60 :02d} min {time_diff % 60:02d} sec"

        total_bar = round((percent / 100) * 50) * '●' + (50 - round((percent / 100) * 50)) * '○'
        print(f'{total_bar} {percent:.2f}% {done}/{total} || {time_dif}', end='\r')
        if total == done:
            Ind.i = 0
            print('')