<template>
  <div id="app">
    <div class="form-container">
      <table>
        <tr>
          <td>姓名:</td>
          <td><input v-model="formData.name" placeholder="请输入您的姓名" /></td>
        </tr>
        <tr>
          <td>所在地:</td>
          <td><input v-model="formData.location" placeholder="请输入您的所在地" /></td>
        </tr>
        <tr>
          <td>问题:</td>
          <td><input v-model="formData.problem" placeholder="请输入您的问题" /></td>
        </tr>
      </table>
      <button @click="submitForm" class="submit-button">提交</button>
    </div>
    <div class="chat-container">
      <div class="input-container">
        <input v-model="message" placeholder="请输入您的消息" />
        <button @click="sendMessage" class="send-button">发送</button>
      </div>
      <div class="chat-history">
        <div v-for="(msg, index) in chatHistory" :key="index" class="chat-message">
          <p :class="{'user-message': msg.sender === 'You', 'bot-message': msg.sender === 'Bot'}">
            <strong>{{ msg.sender }}:</strong> <span v-html="msg.text"></span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      chatHistory: [],
      formData: {
        name: '',
        location: '',
        problem: ''
      }
    };
  },
  methods: {
    async sendMessage() {
      if (this.message.trim() === '') return;

      this.chatHistory.push({ sender: 'You', text: this.message });

      try {
        const response = await axios.post('http://127.0.0.1:8000/chat', {
          message: this.message,
          name: this.formData.name,
          location: this.formData.location,
          problem: this.formData.problem
        });
        await this.simulateStreamOutput(response.data.response);
      } catch (error) {
        console.error('Error sending message:', error);
      }

      this.message = '';
    },
    async simulateStreamOutput(text) {
      const botMessage = { sender: 'Bot', text: '' };
      this.chatHistory.push(botMessage);

      for (let i = 0; i < text.length; i++) {
        botMessage.text += text[i];
        await this.sleep(10); // 每10毫秒显示一个字符
      }
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    async submitForm() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/submit', this.formData);
        console.log('表单提交成功:', response.data);
      } catch (error) {
        console.error('表单提交失败:', error);
      }
    }
  }
};
</script>

<style scoped>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
  margin-top: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-container {
  margin-bottom: 20px;
}

table {
  margin: 0 auto;
  border-collapse: collapse;
}

td {
  padding: 10px;
  color: aliceblue;
}

input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  


}

.submit-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #45a049;
}

.chat-container {
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(238, 236, 236, 0.1);
}

.input-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

input {
  width: 80%;
  padding: 10px;

  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;

/* //字体楷体 */


}

.send-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #45a049;
}

.chat-history {
  max-height: 400px;
  overflow-y: auto;
  border-top: 1px solid #ccc;
  padding-top: 10px;
  border-radius: 5px;
  padding: 10px;
}

.chat-message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.user-message {
  text-align: right;
  color: #2ecc71;
}

.bot-message {
  text-align: left;
  color: #e74c3c;
}

.bot-message span {
  white-space: pre-wrap;
}
</style>