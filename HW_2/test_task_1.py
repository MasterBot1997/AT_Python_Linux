import pytest
import task_1

pwd = f'cd /home/{task_1.user_name}/shared/AT_Python_Linux/HW_2/'

#Тест выполненый на семинаре
def test_step_zip():
    assert task_1.func(f'{pwd}fold_1; 7z a ../fold_2/arch_fold_1', 'Everything is Ok'), 'Не пройдена проверка архивирования'

def test_step_zip_h():
    assert task_1.func(f'{pwd}fold_2; 7z h', '1 file, 265 bytes (1 KiB)'), 'Не пройдена проверка информации о архивах в папке'

def test_step_unzip():
    assert task_1.func(f'{pwd}fold_2; 7z e arch_fold_1.7z ', 'Everything is Ok'), 'Не пройдена проверка разархивации файлов'
    # Для повторных запусков очищаем папку куда архивируем и разархивируем файлы
    task_1.func_del_arh(f'{pwd}fold_2; rm ./arch_fold_1.7z')
    for i in range(1, 5):
        task_1.func_del_arh(f'{pwd}fold_2; rm ./file_{i}.txt')


if __name__ == '__main__':
    pytest.main(['-vv'])