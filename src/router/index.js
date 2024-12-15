import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/LoginView.vue'
import DashView from '../views/MainChart.vue'
import { useLoginStore } from '@/stores/login';
import QuaryDoctor from '../views/Quary_doctor.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashView
    },
    {
      path: '/login',
      name: 'home',
      component: HomeView
    },
    {
      path: '/personal',
      name: 'personal',
      component: () => import('../views/Personal.vue')
    },
    {
      path: '/news',
      name: 'news',
      component: () => import('../views/NewsView.vue')
    },
    {
      path: '/quary-doctor',
      name: 'QuaryDoctor',
      component: QuaryDoctor
    },
    {
      path: '/newsdetail/:nid?',
      name: 'newsdetail',
      component: () => import('../views/NewsDetail.vue')
    },
    {
      path: '/guanli',
      name: 'guanli',
      component: () => import('../views/Guanli.vue'),
      children:[
        {
            path: '/guanli/controluser',
            name: 'controluser',
            component: () => import('../views/manage/ControlUser.vue')
        },
        {
          path: '/guanli/controlblack',
          name: 'controlblack',
          component: () => import('../views/manage/ControlBlack.vue')
      },
        {
          path: '/guanli/controlnews',
          name: 'controlnews',
          component: () => import('../views/manage/ControlNews.vue')
        },
        {
          path: '/guanli/manageself',
          name: 'manageself',
          component: () => import('../views/manage/ManageSelf.vue')
      },
      
      ]
    },

  ]
})
router.beforeEach((to, from, next) => {
  const loginStore = useLoginStore();
  const isLoggedIn = true; // 是否登录
  const userRole = loginStore.person125Info.role; // 用户角色

  // 打印当前导航信息
  console.log(`导航到路径: ${to.path}`);
  console.log(`用户登录状态: ${isLoggedIn}`);
  console.log(`用户角色: ${userRole}`);

  // 用户未登录，允许访问的公共页面路径
  const publicPaths = ['/login', '/news', '/newsdetail', '/'];

  if (!isLoggedIn) {
    if (publicPaths.includes(to.path) || to.path.startsWith('/newsdetail')) {
      console.log("未登录，允许访问公共页面");
      next(); // 允许访问公共页面
    } else {
      console.log("未登录，重定向到登录页面");
      next('/login'); // 未登录时跳转到登录页面
    }
  } else {
    // 用户已登录，根据角色判断访问权限
    if (userRole === 'user' && to.path.startsWith('/guanli')) {
      console.log("普通用户尝试访问管理页面，无权限，重定向到无权限页面");
      next('/noquan'); // 普通用户访问管理页面时，重定向到无权限页面
    } else if (userRole === 'admin' && to.path === '/personal') {
      console.log("管理员尝试访问个人信息页面，无权限，重定向到无权限页面");
      next('/noquan'); // 管理员访问用户页面时，跳转到无权限页面
    } else {
      console.log("正常访问页面");
      next(); // 其他情况正常访问
    }
  }
});



export default router
