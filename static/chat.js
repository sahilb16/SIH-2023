const chat_form = document.getElementById("chat");
const chatform = document.getElementById("chatbot")
const chatBtn = document.getElementById("chatbtn");
const closeBtn = document.getElementById("closebtn");
const chatbox = document.getElementById("chatbox");
const chatInput = document.getElementById("textArea");

let userMessage = null; // Variable to store user's message
const API_KEY = "PASTE-YOUR-API-KEY"; // Paste your API key here
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    const chatContent = className === "outgoing" ? `<div></div>` : `<i class="fa-solid fa-robot"></i><div></div>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("div").textContent = message;
    return chatLi;
}


const generateResponse = (chatElement, response) => {
    const messageElement = chatElement.querySelector("div");
    var answer=legal_lingo_model(chatElement)
    messageElement.textContent = "response"; // Set the response as chat content
}


const handleChat = () => {
    userMessage = chatInput.value.trim();

    if (!userMessage) return;

    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    const outgoingChatLi = createChatLi(userMessage, "outgoing");
    chatbox.appendChild(outgoingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);

    // Make an AJAX POST request to send the user message to Flask
    fetch('/model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `q=${encodeURIComponent(userMessage)}`,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Handle the response data as needed
        const incomingChatLi = createChatLi(data.message, "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

// function closepopup(){
//     if(document.getElementById('closebtn').clicked == true)
// {
//    alert("button was clicked");
// }
// }

chatBtn.addEventListener("click",()=> {
    chatform.style.display="block";
})

closeBtn.addEventListener("click",()=> {
    chatform.style.display="none";
})
if(document.getElementById('closebtn').clicked == true)
{
   alert("button was clicked");
}

const handlespeech = () => {
    fetch('/speechtext') // Replace with your Flask route URL
        .then(response => response.json())
        .then(data => {
            console.log(data.question)
            console.log(data.message); // Handle the response data as needed
            
            // Create an incoming chat message with the response
            const incomingChatLi = createChatLi(data.message, "incoming");
            const outgoingquestionli= createChatLi(data.question,"outgoing")


            const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
            // Append the incoming message to the chatbox
            chatbox.appendChild(outgoingquestionli)
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
            
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// const handlespeech = async function () {
//     fetch('/speechtext') // Replace with your Flask route URL
//         .then(response => response.json())
//         .then(data => {
//             console.log(data.question); // Log the question (for debugging)
//             console.log(data.answer);   // Log the answer (for debugging)

//             // Create outgoing and incoming chat messages for the question and answer
//             const outgoingQuestionLi = createChatLi(data.question, "outgoing");
//             console.log("Outgoing question:", outgoingQuestionLi);

//             // Append the outgoing question to the chatbox
//             chatbox.appendChild(outgoingQuestionLi);
//             console.log("Chatbox after outgoing question:", chatbox);

//             // Use async/await with setTimeout for a delay
//             const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
            
//             (async () => {
//                 await sleep(1000); // Delay for 1000 milliseconds (1 second)
//                 const incomingAnswerLi = createChatLi(data.answer, "incoming");
//                 console.log("Incoming answer:", incomingAnswerLi);
                
//                 // Append the incoming answer to the chatbox
//                 chatbox.appendChild(incomingAnswerLi);
//                 chatbox.scrollTo(0, chatbox.scrollHeight);
//                 console.log("Chatbox after incoming answer:", chatbox);
//             })();
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
// }

   
