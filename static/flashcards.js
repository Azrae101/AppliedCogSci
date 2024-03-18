document.getElementById("flipForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    
    var termElement = document.getElementById("term");
    var answerElement = document.getElementById("answer");

    // Toggle display property of term and answer elements
    if (termElement && answerElement) {
        if (termElement.style.display === "block" || termElement.style.display === "") {
            termElement.style.display = "none";
            answerElement.style.display = "block";
            termElement.textContent = ""; // Clear the term text content
            answerElement.textContent = "{{ list_of_answers[current_index] }}"; // Display answer content
        } else {
            termElement.style.display = "block";
            answerElement.style.display = "none";
            termElement.textContent = "{{ term }}"; // Display term content
            answerElement.textContent = ""; // Clear the answer text content
        }
    }
});
