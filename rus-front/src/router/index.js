import Vue from "vue";
import VueRouter from "vue-router";
import Login from '@/views/Login.vue'
import About from '@/views/About'
import Start from '@/views/Start.vue'
import Timeline from '@/views/Timeline'
import TimelineDetail from '@/views/TimelineDetail'
import Analysis from '@/views/Analysis'
import Group from '@/views/Group'
import KakaoUrlPage from '@/views/KakaoUrlPage'

Vue.use(VueRouter);

// 인증되지 않은 사용자는 로그인 페이지로 보내기
const requireAuth = (to, from, next) => {
  if (localStorage.getItem('access-token')) {
    next()
  } else {
    next({
      path: "/login",
    })
  }
  
}

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/about",
    name: "About",
    component: About
  },
  {
    path: "/",
    name: "Start",
    component: Start,
    beforeEnter: requireAuth
  },
  {
    path: "/mypage/timeline",
    name: "Timeline",
    component: Timeline,
    beforeEnter: requireAuth
  },
  {
    path: "/mypage/timeline/detail",
    name: "TimelineDetail",
    component: TimelineDetail,
    beforeEnter: requireAuth
  },
  {
    path: "/mypage/analysis",
    name: "Analysis",
    component: Analysis,
    beforeEnter: requireAuth
  },
  {
    path: "/mypage/group",
    name: "Group",
    component: Group,
    beforeEnter: requireAuth
  },
  {
    path: "/kakaourlpage",
    name: "KakaoUrlPage",
    component: KakaoUrlPage
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
