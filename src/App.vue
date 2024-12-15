<template>
  <Header></Header>
  <Footer></Footer>
</template>

<script setup>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

</script>

<style>

body {

  
  background-color: #f0f2f5; /* 设置背景颜色 */
  background-image: url('./components/images/bg3.jpg'); /* 设置背景图片路径 */
  background-size: cover; /* 背景图片铺满整个屏幕 */
  background-position: center; /* 居中显示背景图片 */
  background-repeat: no-repeat; /* 禁止背景图片重复 */
}
#app {
  font-family: Arial, sans-serif;
  text-align: center;
}
</style>