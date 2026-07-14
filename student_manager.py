import json
import os
from typing import List, Optional, Dict, Any

DEFAULT_FILE = "students.json"


def load_students(file_path: str = DEFAULT_FILE) -> List[Dict[str, Any]]:
    """Load students from a JSON file if it exists."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            return []

    return []


def save_students(students: List[Dict[str, Any]], file_path: str = DEFAULT_FILE) -> None:
    """Save students to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=2)


def add_student(student_id: str, name: str, age: str, file_path: str = DEFAULT_FILE) -> Dict[str, Any]:
    """Add a new student if the ID does not already exist."""
    students = load_students(file_path)

    for student in students:
        if student.get("id") == student_id:
            raise ValueError(f"Student with ID {student_id} already exists")

    new_student = {"id": student_id, "name": name, "age": age}
    students.append(new_student)
    save_students(students, file_path)
    return new_student


def get_all_students(file_path: str = DEFAULT_FILE) -> List[Dict[str, Any]]:
    """Return all students."""
    return load_students(file_path)


def get_student_by_id(student_id: str, file_path: str = DEFAULT_FILE) -> Optional[Dict[str, Any]]:
    """Find a student by their ID."""
    students = load_students(file_path)
    for student in students:
        if student.get("id") == student_id:
            return student
    return None


def update_student(student_id: str, name: str, age: str, file_path: str = DEFAULT_FILE) -> bool:
    """Update a student's information."""
    students = load_students(file_path)
    for student in students:
        if student.get("id") == student_id:
            student["name"] = name
            student["age"] = age
            save_students(students, file_path)
            return True
    return False


def delete_student(student_id: str, file_path: str = DEFAULT_FILE) -> bool:
    """Delete a student by ID."""
    students = load_students(file_path)
    updated_students = [student for student in students if student.get("id") != student_id]

    if len(updated_students) == len(students):
        return False

    save_students(updated_students, file_path)
    return True


def display_students(students: List[Dict[str, Any]]) -> None:
    """Print students in a readable format."""
    if not students:
        print("No students found.")
        return

    print("\nStudents:")
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}, Age: {student['age']}")


def main() -> None:
    """Run the interactive command-line student management system."""
    file_path = DEFAULT_FILE

    while True:
        print("\nStudent Management System")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student by ID")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            student_id = input("Enter student ID: ").strip()
            name = input("Enter student name: ").strip()
            age = input("Enter student age: ").strip()
            try:
                add_student(student_id, name, age, file_path)
                print("Student added successfully.")
            except ValueError as error:
                print(error)

        elif choice == "2":
            display_students(get_all_students(file_path))

        elif choice == "3":
            student_id = input("Enter student ID: ").strip()
            student = get_student_by_id(student_id, file_path)
            if student:
                print(f"Student found: ID: {student['id']}, Name: {student['name']}, Age: {student['age']}")
            else:
                print("Student not found.")

        elif choice == "4":
            student_id = input("Enter student ID to update: ").strip()
            name = input("Enter new name: ").strip()
            age = input("Enter new age: ").strip()
            if update_student(student_id, name, age, file_path):
                print("Student updated successfully.")
            else:
                print("Student not found.")

        elif choice == "5":
            student_id = input("Enter student ID to delete: ").strip()
            if delete_student(student_id, file_path):
                print("Student deleted successfully.")
            else:
                print("Student not found.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
