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
    newChat.classList.add("chat", "user");
    newChat.innerHTML = `<div class="user-photo"> <img src="static/icons/user-regular.svg" class="icon-img" /> </div> <p class="chat-message">${chatInput.value}</p>`;

    // Append new chat message to chat logs
    chatLogs.appendChild(newChat);
    shouldScroll =
      chatLogs.scrollTop + chatLogs.clientHeight === chatLogs.scrollHeight;
    if (!shouldScroll) {
      scrollToBottom();
    }
    const data = { data: chatInput.value };
    $.ajax({
      type: "POST",
      url: "/predict", // /bert/predict
      data: JSON.stringify(data),
      contentType: "application/json",
      success: function (res) {
        const botChat = document.createElement("div");
        botChat.classList.add("chat", "bot");
        const resposne = res;
        botChat.innerHTML = `<div class="chat-photo"> <img src="static/icons/doctor.svg" class="icon-img" /> </div> <p class="chat-message">${resposne.output}</p>`;
        // Append new chat message to chat logs
        chatLogs.appendChild(botChat);
        // After getting your messages.
        shouldScroll =
        chatLogs.scrollTop + chatLogs.clientHeight === chatLogs.scrollHeight;
        if (!shouldScroll) {
          scrollToBottom();
        }
        chatInput.value = "";
      },
      error: function (error) {
        console.log(error);
      },
    });
  });

  function scrollToBottom() {
    chatLogs.scrollTop = chatLogs.scrollHeight;
  }

  scrollToBottom();
});
