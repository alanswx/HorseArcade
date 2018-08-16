class Student:
        def __init__(self, name, grade, age):
                self.name = name
                self.grade = grade
                self.age = age
        def __repr__(self):
                return repr((self.name, self.grade, self.age))
        def weighted_grade(self):
                return 'CBA'.index(self.grade) / float(self.age)

student_objects = [
        Student('john', 'A', 12),
        Student('jane', 'B', 12),
        Student('dave', 'B', 10),
]
for student in student_objects:
   print(student.__dict__)

print(sorted(student_objects, key=lambda student: student.age))   # sort by age
new=sorted(student_objects, key=lambda student: (student.age,student.name))   # sort by age

for student in new:
   print(student.__dict__)
