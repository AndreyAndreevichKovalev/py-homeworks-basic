class PersonWithGrades:
    def average_grade(self):
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return total / count if count != 0 else 0

    def __lt__(self, other):
        if not isinstance(other, PersonWithGrades):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Student(PersonWithGrades):
    def __init__(self, name, surname, gender):
        self.name: str = name
        self.surname: str = surname
        self.gender: str = gender
        self.finished_courses: list = []
        self.courses_in_progress: list = []
        self.grades: dict = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer, course, grade):
        if (
                isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached
        ):
            if 1 <= grade <= 10:
                if course in lecturer.grades:
                    lecturer.grades[course] += [grade]
                else:
                    lecturer.grades[course] = [grade]
            else:
                return 'Ошибка: Оценка должна быть в диапазоне от 1 до 10'
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = self.average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg_grade}\n"
            f"Курсы в процессе изучения: {courses_in_progress}\n"
            f"Завершенные курсы: {finished_courses}"
        )


class Mentor:
    def __init__(self, name, surname):
        self.name: str = name
        self.surname: str = surname
        self.courses_attached: list = []


class Lecturer(Mentor, PersonWithGrades):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades: dict = {}

    def __str__(self):
        avg_grade = self.average_grade()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg_grade}"
        )


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (
                isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}"
        )


student1 = Student('Ruoy', 'Eman', 'female')
student2 = Student('John', 'Doe', 'male')

lecturer1 = Lecturer('Alan', 'Smith')
lecturer2 = Lecturer('Andrew', 'Johnson')

reviewer1 = Reviewer('Brad', 'Pitt')
reviewer2 = Reviewer('Bradley', 'Cooper')

student1.courses_in_progress += ['Python']
student2.courses_in_progress += ['Python']

lecturer1.courses_attached += ['Python']
lecturer2.courses_attached += ['Python']

reviewer1.courses_attached += ['Python']
reviewer2.courses_attached += ['Python']

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student2, 'Python', 7)

student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer2, 'Python', 8)
student2.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer2, 'Python', 9)

print(lecturer1 < lecturer2)
print(student1 < student2)

print(lecturer1 > lecturer2)
print(student1 > student2)

print(student1)
print(student2)

print(lecturer1)
print(lecturer2)

print(reviewer1)
print(reviewer2)


def average_grade_homework(students, course):
    total = 0
    count = 0
    for student in students:
        if course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return total / count if count != 0 else 0


def average_grade_lectures(lecturers, course):
    total = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return total / count if count != 0 else 0


print(
    f"Средняя оценка за домашние задания по курсу Python:"
    f"{average_grade_homework([student1, student2], 'Python')}"
)
print(
    f"Средняя оценка за лекции по курсу Python:"
    f"{average_grade_lectures([lecturer1, lecturer2], 'Python')}"
)
