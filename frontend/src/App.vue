<template>
  <div id="app">
    <h1 style="text-align: center; margin: 20px 0;">成果相关查询</h1>
    <button @click="showChat = true">打开聊天窗口</button>

    <!-- 弹窗容器 -->
    <div v-if="showChat" class="chat-popup" ref="popup">
      <div class="popup-header" @mousedown="startDrag">
        客服查询
        <span class="close-btn" @click="showChat = false">&times;</span>
      </div>
      <ChatBot />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ChatBot from './components/ChatBot.vue';

const showChat = ref(false);
const popup = ref(null);
let isDragging = false;
let offsetX = 0;
let offsetY = 0;

// 拖动逻辑
const startDrag = (e) => {
  isDragging = true;
  offsetX = e.clientX - popup.value.offsetLeft;
  offsetY = e.clientY - popup.value.offsetTop;
  document.addEventListener('mousemove', handleDrag);
  document.addEventListener('mouseup', stopDrag);
};

const handleDrag = (e) => {
  if (!isDragging) return;
  const x = e.clientX - offsetX;
  const y = e.clientY - offsetY;
  popup.value.style.left = `${x}px`;
  popup.value.style.top = `${y}px`;
};

const stopDrag = () => {
  isDragging = false;
  document.removeEventListener('mousemove', handleDrag);
  document.removeEventListener('mouseup', stopDrag);
};
</script>

<style scoped>
.chat-popup {
  position: fixed;
  top: 100px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  width: 950px;
  transition: all 0.3s ease;
}

.popup-header {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  cursor: move;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.close-btn {
  font-size: 1.2em;
  cursor: pointer;
  user-select: none;
}
</style>