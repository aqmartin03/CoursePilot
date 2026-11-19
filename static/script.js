console.log("script.js loaded");
const assignmentForm = document.querySelector("#assignment-form");
console.log("assignment form found:", assignmentForm);

const filterButtons = document.querySelectorAll("#assignment-filters button");
const assignments = document.querySelectorAll("#assignment-list li");

filterButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const selectedFilter = button.dataset.filter;
        assignments.forEach(function (assignment) {
            const isCompleted = assignment.dataset.completed === "1";
            const shouldShow = 
                selectedFilter === "all" ||
                (selectedFilter === "completed" && isCompleted) ||
                (selectedFilter === "incomplete" && !isCompleted);
            
                assignment.hidden = !shouldShow;
        });
    });
});

assignmentForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(assignmentForm);

    const assignment = {
        title: formData.get("assignment_title"),
        due_date: formData.get("assignment_due_date"),
        course_id: formData.get("assignment_course_id"),
        estimated_hours: formData.get("estimated_hours"),
        importance: formData.get("importance")
    };

    fetch("/api/assignments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(assignment)
    })
    .then(response => {
        return response.json().then(data => {
            if (!response.ok) {
                throw new Error(
                    data.error || "The assignment could not be created."
                );
            }
            return data;
        });
    })
    .then(data => {
        console.log(data);
        alert("Assignment created!");
        assignmentForm.reset();
        window.location.reload();
    })
    .catch(error => {
        console.error(error);
        alert(error.message);
    });
});