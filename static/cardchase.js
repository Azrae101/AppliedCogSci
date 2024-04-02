const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const userInput = document.getElementById('userInput');
const submitButton = document.getElementById('submitButton');
const questionAnswerContainer = document.getElementById('questionAnswerContainer');
let currentQuestion = {};
let movementSpeed = 1;
let blockY = 0;
let blockText = '';

function drawBlock(text, y) {
    ctx.fillStyle = "skyblue";
    ctx.fillRect(50, y, 200, 30);
    ctx.fillStyle = "black";
    ctx.font = "12px Arial";
    ctx.fillText(text, 150, y + 20);
}

function fetchQuestions() {
    return fetch('/cardchase')
       .then(response => response.json())
       .then(questions => {
            return questions;
        });
}

function updateQuestionAnswer() {
    if (Object.keys(currentQuestion).length > 0) {
        const question = currentQuestion.question;
        const answer = currentQuestion.answer;
        questionAnswerContainer.querySelector('#question').innerText = question;
        questionAnswerContainer.querySelector('#answer').innerText = answer;
    }
}

function animateBlock() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBlock(blockText, blockY);
    blockY += movementSpeed;
    if (blockY > canvas.height) {
        blockY = 0;
        fetchNextQuestion();
    }
    requestAnimationFrame(animateBlock);
}

function fetchNextQuestion() {
    fetchQuestions()
       .then(questions => {
            if (questions.length > 0) {
                currentQuestion = questions.shift();
                updateQuestionAnswer();
                blockText = currentQuestion.question;
                animateBlock();
            }
        });
}

function submitAnswer() {
    const userAnswer = userInput.value.toLowerCase();
    if (userAnswer === currentQuestion.answer.toLowerCase()) {
        fetchNextQuestion();
    }
    userInput.value = '';
}

fetchNextQuestion();

submitButton.addEventListener('click', submitAnswer);
