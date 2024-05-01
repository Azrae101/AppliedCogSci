// Function to split the question into smaller parts to fit within the flashcard width
function splitQuestion(questionText, maxWidth) {
    const words = questionText.split(' ');
    const lines = [];
    let currentLine = words[0];
    for (let i = 1; i < words.length; i++) {
        const word = words[i];
        const width = ctx.measureText(currentLine + ' ' + word).width;
        if (width < maxWidth - 40) { // Adjust 40 for padding
            currentLine += ' ' + word;
        } else {
            lines.push(currentLine);
            currentLine = word;
        }
    }
    lines.push(currentLine);
    return lines;
}

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

document.addEventListener("DOMContentLoaded", function() {
    const termElement = document.getElementById("term");
    if (termElement) {
        const termText = termElement.textContent;
        const maxWidth = termElement.offsetWidth; // Get the width of the term element
        const questionParts = splitQuestion(termText, maxWidth);
        termElement.innerHTML = ""; // Clear existing content
        for (const part of questionParts) {
            const p = document.createElement("p");
            p.textContent = part;
            termElement.appendChild(p);
        }
    }
});

