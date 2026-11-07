semester_input = "1"
error_message = None
semester_id = None

try:
    semester_id = int(semester_input)
except ValueError:
    error_message = "Please select a valid semester."

if error_message is None:
    print("Semester ID is valid!")
else:
    print(error_message)