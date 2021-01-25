
class Person:
    def __init__(self, first_name, last_name, birth_date, job, working_years, salary, country, city, gender='unknown'):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.job = job
        self.working_years = working_years
        self.salary = salary
        self.country = country
        self.city = city
        self.gender = gender

    def name(self):
        return self.first_name + " " + self.last_name

    def age(self):
        day = self.birth_date[:2]
        month = self.birth_date[3:5]
        return 2018 - int(self.birth_date[-4:]) - (1 if (month != '01' and day != '01') else 0)

    def work(self):
        is_he_she_it = 'Is a '
        if self.gender == 'male':
            is_he_she_it = 'He is a '
        elif self.gender == 'female':
            is_he_she_it = 'She is a '

        return is_he_she_it + self.job

    def home(self):
        return f'Lives in {self.city}, {self.country}'

    def money(self):
        x = self.salary*12*self.working_years
        return '{0:,}'.format(x).replace(',', ' ')


p1 = Person("John", "Smith", "19.09.1979", "welder", 15, 3600, "Canada", "Vancouver", "male")
p2 = Person("Hanna Rose", "May", "05.12.1995", "designer", 2.2, 2150, "Austria", "Vienna")
assert p1.name() == "John Smith", "Name"
assert p1.age() == 38, "Age"
assert p2.work() == "Is a designer", "Job"
assert p1.money() == "648 000", "Money"
assert p2.home() == "Lives in Vienna, Austria", "Home"
