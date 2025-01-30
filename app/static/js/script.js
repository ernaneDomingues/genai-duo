const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

// Função para enviar a mensagem
function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        displayMessage(userMessage, 'user');
        getBotResponse(userMessage);
        userInput.value = '';
    }
}

// Função para exibir mensagens na interface
function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Função para a resposta do bot via API Flask
async function getBotResponse(userMessage) {
    try {
        // Enviando a mensagem do usuário para a API Flask (via POST)
        const response = await fetch('http://localhost:5000/ask', {  // Substitua com o URL correto da sua API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userMessage })
        });

        // Processa a resposta da API
        const data = await response.json();

        // Exibe a resposta do bot
        if (data && data.answer) {
            displayMessage(data.answer, 'bot');
        } else {
            displayMessage('Desculpe, não consegui entender a resposta.', 'bot');
        }
    } catch (error) {
        console.error('Erro ao obter resposta do bot:', error);
        displayMessage('Erro ao conectar com o servidor. Tente novamente mais tarde.', 'bot');
    }
}

// Permite enviar mensagem com "Enter"
userInput.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});