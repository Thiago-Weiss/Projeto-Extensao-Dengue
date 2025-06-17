import datetime
import PathManager




def write_log(mensagem):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(PathManager.log_file, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {mensagem}\n')

