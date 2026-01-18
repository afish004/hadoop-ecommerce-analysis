import { createRouter, createWebHistory } from 'vue-router'

// 导入布局组件
import MainLayout from '@/layout/MainLayout.vue'

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { 
      requiresAuth: false,
      title: '登录'
    }
  },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { 
          title: '综合驾驶舱',
          icon: 'Odometer'
        }
      },
      {
        path: 'conversion',
        name: 'Conversion',
        component: () => import('@/views/Conversion.vue'),
        meta: { 
          title: '流量与转化',
          icon: 'TrendCharts'
        }
      },
      {
        path: 'product',
        name: 'Product',
        component: () => import('@/views/Product.vue'),
        meta: { 
          title: '商品与品牌',
          icon: 'Goods'
        }
      },
      {
        path: 'user-insight',
        name: 'UserInsight',
        component: () => import('@/views/UserInsight.vue'),
        meta: { 
          title: '用户价值分层',
          icon: 'User'
        }
      },
      {
        path: 'prediction',
        name: 'Prediction',
        component: () => import('@/views/Prediction.vue'),
        meta: { 
          title: '趋势预测',
          icon: 'MagicStick'
        }
      }
    ]
  },
  {
    // 404 页面
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      requiresAuth: false,
      title: '页面不存在'
    }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫（路由拦截）
router.beforeEach((to, from, next) => {
  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      // 未登录，跳转到登录页
      next('/login')
    } else {
      next()
    }
  } else {
    // 不需要登录验证的页面
    if (to.path === '/login') {
      const token = localStorage.getItem('token')
      if (token) {
        // 已登录用户访问登录页，跳转到首页
        next('/dashboard')
      } else {
        next()
      }
    } else {
      next()
    }
  }
})

// 全局后置钩子（设置页面标题）
router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - Hadoop电商行为分析系统` : 'Hadoop电商行为分析系统'
})

export default router
