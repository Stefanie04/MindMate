$(async function () {
  const chatForm = document.querySelector(".chat-form");
  const chatInput = document.querySelector('input[type="text"]');
  const chatLogs = document.querySelector(".chatlogs");

  // Add event listener to chat form
  chatForm.addEventListener("submit", (e) => {
    // Prevent form from submitting
    e.preventDefault();

    // Create new chat message
    const newChat = document.createElement("div");
    newChat.classList.add("chat", "bot");
    newChat.innerHTML = `<div class="chat-photo"> <img src="static/icons/doctor.svg" class="icon-img" /> </div> <p class="chat-message">${chatInput.value}</p>`;

    // Append new chat message to chat logs
    chatLogs.appendChild(newChat);
    const data = { data: chatInput.value };
    $.ajax({
      type: "POST",
      url: "/predict",
      data: JSON.stringify(data),
      contentType: "application/json",
      success: function (res) {
        // do something with the received data
        console.log("res", res);
        const botChat = document.createElement("div");
        botChat.classList.add("chat", "user");
        const resposne = res;
        botChat.innerHTML = `<div class="user-photo"> <img src="static/icons/user-regular.svg" class="icon-img" /> </div> <p class="chat-message">${resposne.output}</p>`;
        // Append new chat message to chat logs
        chatLogs.appendChild(botChat);
        chatInput.value = '';
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
});
