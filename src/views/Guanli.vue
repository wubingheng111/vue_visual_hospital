<template>
  <el-container class="layout-container-demo">
    <el-aside width="200px" class="custom-aside">
      <el-scrollbar wrap-class="scrollbar-wrap">
        <el-menu :default-openeds="['1','2','3']" class="custom-menu">
          <!-- 用户管理 -->
          <el-sub-menu index="1">
            <template #title>
              <i class="el-icon-document"></i>用户管理
            </template>
            <el-menu-item-group>
              <router-link to="/guanli/controluser">
                <el-menu-item index="1-1">用户信息管理</el-menu-item>
              </router-link>
              <router-link to="/guanli/controlblack">
                <el-menu-item index="1-2">黑名单管理</el-menu-item>
              </router-link>
              <router-link to="/guanli/controlnews">
                <el-menu-item index="1-3">新闻管理</el-menu-item>
              </router-link>
              <router-link to="/guanli/controlzice">
              <el-menu-item index="1-4">自测管理</el-menu-item>
            </router-link>
            </el-menu-item-group>
          </el-sub-menu>

          <!-- 医生管理 -->
          <el-sub-menu index="2">
            <template #title>
              <i class="el-icon-suitcase"></i>医生管理
            </template>
            <el-menu-item-group>
              <router-link to="/guanli/controldoctor">
                <el-menu-item index="2-1">医生信息管理</el-menu-item>
              </router-link>
            </el-menu-item-group>
          </el-sub-menu>

          <el-sub-menu index="3">
            <template #title>
              <i class="el-icon-suitcase"></i>管理员信息
            </template>
            <el-menu-item-group>
              <router-link to="/guanli/manageself">
                <el-menu-item index="3-1">个人信息修改</el-menu-item>
              </router-link>
                <el-menu-item index="3-2" @click="Exit">退出登录</el-menu-item>
            </el-menu-item-group>
          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </el-aside>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

  <script setup>
  import { useLoginStore } from '@/stores/login';
  import { useRouter } from 'vue-router';
  const loginStore = useLoginStore();
  const router = useRouter();
  const Exit = () => {
  // 重置 person125Info
  loginStore.person125Info.role = '';  
  loginStore.person125Info.name = '';
  loginStore.person125Info.id = '';
  loginStore.person125Info.state = false;

  // 跳转到 /login
  router.push('/login');
};
  </script>
  
  <style scoped>
  .layout-container-demo {
    height: 100%;
    background-color: #f0f5ff;
  }
  
  .custom-aside {
    height: 100%;
    background-color: #c6e2ff;
  }
  
  .custom-menu {
    border-right: none;
  }
  
  .scrollbar-wrap {
    height: 100%;
  }
  
  /* // 根据实际需求调整图标样式 */
  .el-icon-document, .el-icon-suitcase, .el-icon-setting {
    font-size: 18px;
    margin-right: 10px;
  }
  </style>
  