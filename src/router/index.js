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
      name: 'login',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/noquan',
      name: 'noquan',
      component: () => import('../views/NoQuan.vue')
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
      path: '/intelligent-consultation',
      name: 'intelligent-consultation',
      component: () => import('../views/NewsView.vue')
    },
    {
      path: '/health-analytics',
      name: 'hospital-navigation',
      component: () => import('../views/HealthAnalytics.vue')
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
  // 检查用户是否真正登录（基于store中的state字段）
  const isLoggedIn = loginStore.person125Info.state;

  // 打印当前导航信息
  console.log(`导航到路径: ${to.path}`);
  console.log(`用户登录状态: ${isLoggedIn}`);

  // 游客允许访问的公共页面路径（只有可视化大屏、登录和注册）
  const publicPaths = ['/login', '/register', '/'];

  if (!isLoggedIn) {
    if (publicPaths.includes(to.path)) {
      console.log("游客访问公共页面");
      next(); // 允许访问公共页面
    } else {
      console.log("游客尝试访问受限页面，重定向到登录页面");
      next('/login'); // 未登录时跳转到登录页面
    }
  } else {
    // 用户已登录，可以访问所有页面
    console.log("已登录用户，允许访问所有页面");
    next(); // 登录用户可以访问所有页面
  }
});



export default router
