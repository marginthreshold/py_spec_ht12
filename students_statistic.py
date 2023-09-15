import csv


class NameDescriptor:
    def __get__(self, instance, owner):
        return instance._name

    def __set__(self, instance, value):
        if not value.isalpha() or not value.istitle():
            raise ValueError("Фамилия должна содержать только буквы и начинаться с заглавной буквы.")
        instance._name = value


class SubjectDescriptor:
    def __get__(self, instance, owner):
        return instance._subjects

    def __set__(self, instance, value):
        valid_subjects = instance.load_subjects_from_csv("subjects.csv")
        if not set(value).issubset(valid_subjects):
            raise ValueError("Есть Недопустимый предмет.")
        instance._subjects = value


class Student:
    name = NameDescriptor()
    subjects = SubjectDescriptor()

    def __init__(self, name, subjects_scores):
        self.name = name
        self.subjects = subjects_scores

    def load_subjects_from_csv(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            subjects = [row[0] for row in reader]
        return subjects

    def average_scores_all_subjects(self):
        all_scores = [score for subject in self.subjects.values() for score in subject["scores"]]
        return sum(all_scores) / len(all_scores)

    def average_test_res_per_subj(self):
        average_test_results = {}
        for subject, test_result_data in self.subjects.items():
            test_results = test_result_data["test_results"]
            average_test_results[subject] = round(sum(test_results) / len(test_results), 2)
        return average_test_results


if __name__ == '__main__':
    subjects_scores = {
        "Math": {"scores": [4, 5, 3], "test_results": [80, 90, 75]},
        "English": {"scores": [5, 4, 5], "test_results": [95, 88, 92]},
        "Science": {"scores": [3, 4, 4], "test_results": [70, 85, 78]}
    }
    student = Student("Иванов", subjects_scores)
    print(f"Допустимые предметы: {set(student.subjects)}")
    print(f"Средний балл по всем предметам: {student.average_scores_all_subjects():.2f}")
    print(f"Средний балл по тестам по предмету: {student.average_test_res_per_subj()}")
