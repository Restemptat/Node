1. Реализуйте класс OneIndexedList, который имитирует поведение списка,
 использующего индексацию начинающуюся с 1 (а не с 0, как в стандартном списке). 
 Используйте магические методы init, setitem, getitem

При инициализации класса без аргумента 
OneIndexedList()
класс должен использовать пустой список по умолчанию, 
поддерживающий такую индексацию



a = OneIndexedList([1,2,3])
a[1]
>>> 1

class OneIndexedList:
    def __init__(self, arr=None): 
        if arr is None:
            arr = []
        self.items = arr
    def __getitem__(self, key):
        return self.items[key - 1]
    def __setitem__(self, key, value):
        self.items[key - 1] = value
        print(key, value)

2.
Вам необходимо написать скрипт, в котором реализован класс FileReader.
Конструктор этого класса принимает один параметр: путь до файла на диске. 

В классе FileReader должен быть реализован метод read, возвращающий строку - содержимое файла,
путь к которому был указан при создании экземпляра класса, а так же метод write, который записывает некоторое содержимое в файл. 

Python модуль должен быть написан таким образом, чтобы импорт класса FileReader из него не вызвал ошибок. 
Например, при написании реализации метода read, вам нужно учитывать случай, когда при инициализации был передан путь к несуществующему файлу. 
Требуется обработать возникающее при этом исключение FileNotFoundError и вернуть из метода read пустую строку.

Также в классе должен реализован метод count, который возвращает количество строк и слов в файле (для токенизации используйте NLTK), 
а также записывает информацию в соответствующие атрибуты line_count и word_count.

Кроме того в классе необходимо переопределять следующие магические методы:
a. add: склеивает содержимое двух файлов, записывает в текущую директорию, возвращает объект класса FileReader
b. str: выводит путь до файла (или же использовать repr)



import nltk
 
class FileReader:
    def __init__(self, path):
        self.path = path
        self.word_count = 0
        self.line_count = 0
    def read(self):
        try:
            file = open(self.path, "r", encoding="utf-8")
            file_data = file.read()
            file.close()
            return file_data
        except FileNotFoundError:
            return ""
    def write(self, str_add):
        file = open(self.path, "w", encoding="utf-8")
        # file.write("\n")
        file.write(str_add)
        file.close()
 
    def count(self):
        data = self.read()
        words = nltk.word_tokenize(data)
        self.word_count = len(words)
        lines = nltk.line_tokenize(data)
        self.line_count = len(lines)
 
    def __add__(self, other):
        ff = self.path.split("/")
        ff = ff[:-1]
        string = "/".join(ff) 
        result = string + "/" + "result.txt"
        obj3 = FileReader(result)
        obj3.write(self.read() + "\n" + other.read())
        return obj3
    def __str__(self):
        return self.path