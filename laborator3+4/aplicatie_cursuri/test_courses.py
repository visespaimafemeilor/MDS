import unittest
import json
import os
import tempfile


def load_courses(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_courses(filepath, courses):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)


def add_course(filepath, course):
    courses = load_courses(filepath)
    courses.append(course)
    save_courses(filepath, courses)
    return courses


def update_course(filepath, index, new_data):
    courses = load_courses(filepath)
    courses[index] = new_data
    save_courses(filepath, courses)
    return courses


def delete_course(filepath, index):
    courses = load_courses(filepath)
    del courses[index]
    save_courses(filepath, courses)
    return courses


class TestCourses(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.temp_dir.name, "courses.json")
        sample = [
            {"nume": "MDS", "profesor": "Andrei Horatiu Cheval", "credite": 4},
            {"nume": "AI", "profesor": "Mihai Popa", "credite": 5},
        ]
        save_courses(self.data_file, sample)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_course(self):
        add_course(self.data_file, {"nume": "POO", "profesor": "Ion Ionescu", "credite": 3})
        courses = load_courses(self.data_file)
        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[-1]["nume"], "POO")
        self.assertEqual(courses[-1]["profesor"], "Ion Ionescu")
        self.assertEqual(courses[-1]["credite"], 3)

    def test_add_course_increments_list(self):
        before = load_courses(self.data_file)
        add_course(self.data_file, {"nume": "BD", "profesor": "Maria Popescu", "credite": 6})
        after = load_courses(self.data_file)
        self.assertEqual(len(after), len(before) + 1)

    def test_update_course(self):
        new_data = {"nume": "MDS", "profesor": "Andrei H. Cheval", "credite": 5}
        update_course(self.data_file, 0, new_data)
        courses = load_courses(self.data_file)
        self.assertEqual(courses[0]["profesor"], "Andrei H. Cheval")
        self.assertEqual(courses[0]["credite"], 5)

    def test_update_course_does_not_affect_others(self):
        new_data = {"nume": "MDS", "profesor": "Updated", "credite": 10}
        update_course(self.data_file, 0, new_data)
        courses = load_courses(self.data_file)
        self.assertEqual(courses[1]["nume"], "AI")
        self.assertEqual(courses[1]["profesor"], "Mihai Popa")
        self.assertEqual(courses[1]["credite"], 5)

    def test_delete_course(self):
        delete_course(self.data_file, 0)
        courses = load_courses(self.data_file)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0]["nume"], "AI")

    def test_delete_course_reduces_list_correctly(self):
        before = load_courses(self.data_file)
        delete_course(self.data_file, 1)
        after = load_courses(self.data_file)
        self.assertEqual(len(after), len(before) - 1)
        self.assertEqual(after[0]["nume"], "MDS")

    def test_delete_last_course(self):
        delete_course(self.data_file, 0)
        delete_course(self.data_file, 0)
        courses = load_courses(self.data_file)
        self.assertEqual(courses, [])

    def test_load_nonexistent_file(self):
        missing = os.path.join(self.temp_dir.name, "nonexistent.json")
        courses = load_courses(missing)
        self.assertEqual(courses, [])

    def test_save_and_reload_preserves_data(self):
        original = load_courses(self.data_file)
        save_courses(self.data_file, original)
        reloaded = load_courses(self.data_file)
        self.assertEqual(original, reloaded)

    def test_add_course_with_romanian_chars(self):
        course = {"nume": "Calcul numeric", "profesor": "Ștefan Andrei", "credite": 4}
        add_course(self.data_file, course)
        courses = load_courses(self.data_file)
        self.assertIn(course, courses)


if __name__ == "__main__":
    unittest.main()
