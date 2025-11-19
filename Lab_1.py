from abc import ABC, abstractmethod
import re

class Person(ABC):
    def __init__(self, firstname, lastname, birth_date):
        self.firstname = firstname
        self.lastname = lastname
        self.birth_date = birth_date

    @abstractmethod
    def info(self):
        pass


class ICanSwim(ABC):
    @abstractmethod
    def swim(self):
        pass


class Student(Person, ICanSwim):
    def __init__(self, firstname, lastname, course, student_id, birth_date):
        super().__init__(firstname, lastname, birth_date)
        self.course = course
        self.student_id = student_id

    def info(self):
        return f"Студент: {self.firstname} {self.lastname}, курс: {self.course}, ID: {self.student_id}, дата нар.: {self.birth_date}"

    def swim(self):
        return f"{self.firstname} {self.lastname} уміє плавати."


class Painter(Person):
    def info(self):
        return f"Художник: {self.firstname} {self.lastname}"

class Farmer(Person):
    def info(self):
        return f"Фермер: {self.firstname} {self.lastname}"


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def write_person(self, person):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f"{type(person).__name__} {person.firstname}{person.lastname}\n")
            f.write("{\n")
            for key, value in person.__dict__.items():
                f.write(f'   "{key}": "{value}",\n')
            f.write("}\n")

    def read_students(self):
        students = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("Student"):
                firstname, lastname = re.findall(r"Student\s+(\w+)(\w+)", lines[i])[0]
                attrs = {}
                i += 2
                while not lines[i].startswith("}"):
                    key, value = re.findall(r'"(.*?)":\s*"(.*?)"', lines[i])[0]
                    attrs[key] = value
                    i += 1
                student = Student(
                    attrs["firstname"],
                    attrs["lastname"],
                    int(attrs["course"]),
                    attrs["student_id"],
                    attrs["birth_date"]
                )
                students.append(student)
            i += 1
        return students


class ConsoleMenu:
    def __init__(self, file_handler):
        self.file_handler = file_handler

    def run(self):
        while True:
            print("\n1. Додати студента")
            print("2. Показати всіх студентів")
            print("3. Порахувати студентів 2-го курсу, які народилися взимку")
            print("4. Вихід")

            choice = input("Ваш вибір: ")
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.show_students()
            elif choice == "3":
                self.count_winter_students()
            elif choice == "4":
                break
            else:
                print("Невірний вибір!")

    def add_student(self):
        firstname = input("Ім'я: ")
        lastname = input("Прізвище: ")
        course = int(input("Курс: "))
        student_id = input("Номер студентського: ")
        birth_date = input("Дата народження (ДД.ММ.РРРР): ")
        if not re.match(r"\d{2}\.\d{2}\.\d{4}", birth_date):
            print("❌ Невірний формат дати.")
            return
        student = Student(firstname, lastname, course, student_id, birth_date)
        self.file_handler.write_person(student)
        print("✅ Дані збережено.")

    def show_students(self):
        for s in self.file_handler.read_students():
            print(s.info())

    def count_winter_students(self):
        count = 0
        for s in self.file_handler.read_students():
            month = int(s.birth_date.split(".")[1])
            if s.course == 2 and month in (12, 1, 2):
                count += 1
        print(f"👨‍🎓 Кількість студентів 2-го курсу, народжених взимку: {count}")


if __name__ == "__main__":
    fh = FileHandler("students.txt")
    menu = ConsoleMenu(fh)
    menu.run()
