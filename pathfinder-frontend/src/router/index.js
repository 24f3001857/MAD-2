import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/admin-dashboard',
    name: 'admin-dashboard',
    component: () => import('../views/AdminDashboardView.vue')
  },
  {
    path: '/company-dashboard',
    name: 'company-dashboard',
    component: () => import('../views/CompanyDashboardView.vue')
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue')
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;