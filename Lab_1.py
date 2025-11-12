class Painter:
    def __init__(self, name, age, genre, paintings, price):
        self.name = name
        self.age = age
        self.genre = genre
        self.paintings = paintings
        self.price = price

    def total_value(self):
        return self.paintings * self.price

    def display_info(self):
        print(f"Ім'я: {self.name}, Вік: {self.age}, Жанр: {self.genre}, Кількість картин: {self.paintings}, Ціна: {self.price}, Загальна вартість: {self.total_value()}")

    def save_to_file(self, filename):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{self.name},{self.age},{self.genre},{self.paintings},{self.price}\n")

    @staticmethod
    def load_from_file(filename):
        painters = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                name, age, genre, paintings, price = line.strip().split(',')
                painters.append(Painter(name, int(age), genre, int(paintings), float(price)))
        return painters

# Демонстрація
if __name__ == "__main__":
    p1 = Painter("Іван Петров", 35, "Пейзаж", 12, 500)
    p2 = Painter("Олег Коваль", 42, "Портрет", 8, 800)

    p1.save_to_file('painters.txt')
    p2.save_to_file('painters.txt')

    loaded = Painter.load_from_file('painters.txt')
    for painter in loaded:
        painter.display_info()
