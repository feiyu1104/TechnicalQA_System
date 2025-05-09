<template>
  <div class="chat-container">
    <!-- 聊天记录 -->
    <div class="chat-messages" ref="chatMessages">
      <div v-for="(message, index) in messages" :key="index"
           :class="['message', message.sender]">
        <span>{{ message.text }}</span>
      </div>
    </div>

    <!-- 输入框 -->
    <div class="chat-input">
      <input
        v-model="userInput"
        @keydown.enter="sendMessage"
        placeholder="输入消息..."
      />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 聊天记录
const messages = ref([
  { text: "你好！欢迎使用中国先进技术问答系统！请问有什么可以帮助你的？", sender: "bot" }
]);

// 用户输入
const userInput = ref("");

// 滚动到底部
const chatMessages = ref(null);
const scrollToBottom = () => {
  if (chatMessages.value) {
    chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
  }
};

// 发送消息到后端
const sendMessage = async () => {
  if (userInput.value.trim() === "") return;

  // 添加用户消息到聊天记录
  messages.value.push({ text: userInput.value, sender: "user" });
  const userMessage = userInput.value; // 保存用户消息
  userInput.value = "";
  scrollToBottom();

  try {
    // 向后端发送请求
    const response = await axios.post('http://localhost:5000/chat', {
      message: userMessage // 使用保存的用户消息
    });

    // 添加机器人回复到聊天记录
    messages.value.push({
      text: response.data.response,
      sender: "bot"
    });
    scrollToBottom();
  } catch (error) {
    console.error("Error communicating with backend:", error);
    messages.value.push({
      text: "抱歉，出现了一些问题，请稍后再试。",
      sender: "bot"
    });
    scrollToBottom();
  }
};

// 自动滚动到底部
onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #ccc;
  padding: 10px;
  width: 900px;
  margin: 20px auto;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
  overflow-y: auto;
  padding: 10px;
  background-color: #f9f9f9;
  flex-grow: 1;
}

.message {
  display: flex;
  align-items: center;
  word-break: break-word;
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 10px;
}

.message.user {
  align-self: flex-end; /* 修正后的属性 */
  background-color: #007bff;
  color: white;
}

.message.bot {
  align-self: flex-start;
  background-color: #e1e1e1;
}

.chat-input {
  display: flex;
  gap: 5px;
  margin-top: auto;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.chat-input button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>