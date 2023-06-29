const chatMessages = document.getElementById('chat-messages');
const questionInput = document.getElementById('question-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);
questionInput.addEventListener('keydown', handleKeyDown);

function handleKeyDown(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}

function sendMessage() {
    const question = questionInput.value.trim();

    if (question === '') {
        return;
    }

    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container';

    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = question;

    messageContainer.appendChild(userMessage);
    chatMessages.appendChild(messageContainer);

    questionInput.value = '';

    // Send the question to the backend API
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        const answer = data.answer;

        const messageContainer = document.createElement('div');
        messageContainer.className = 'message-container';

        const botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.textContent = answer;

        messageContainer.appendChild(botMessage);
        chatMessages.appendChild(messageContainer);

        // Scroll to the bottom of the chat messages
        chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
