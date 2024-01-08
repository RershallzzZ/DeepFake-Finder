import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'



/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
    {
        path: '/redirect',
        component: Layout,
        hidden: true,
        children: [
            {
                path: '/redirect/:path(.*)',
                component: () => import('@/views/redirect/index'),
            },
        ],
    },
    {
        path: '/login',
        component: () => import('@/views/login/index'),
        hidden: true,
    },
    {
        path: '/auth-redirect',
        component: () => import('@/views/login/auth-redirect'),
        hidden: true,
    },
    {
        path: '/404',
        component: () => import('@/views/error-page/404'),
        hidden: true,
    },
    {
        path: '/401',
        component: () => import('@/views/error-page/401'),
        hidden: true,
    },
    {
        path: '/',
        component: Layout,
        redirect: '/dashboard',
        children: [
            {
                path: 'dashboard',
                component: () => import('@/views/dashboard/index'),
                name: 'Dashboard',
                meta: { title: '系统首页', icon: 'home', affix: true, noCache: true },
            },
        ],
    },
    {
        path: '/download',
        component: Layout,
        children: [
            {
                path: 'index',
                component: () => import('@/views/download'),
                name: 'Download',
                meta: { title: '视频采集展示', icon: 'download' },
            },
        ],
    },
    {
        path: '/detectshow',
        component: Layout,
        children: [
            {
                path: 'index',
                component: () => import('@/views/detectresult'),
                name: 'Detectresult',
                meta: { title: '检测结果展示', icon: 'detectshow' },
            },
        ],
    },
    {
        path: '/resultanalysis',
        component: Layout,
        children: [
            {
                path: 'index',
                component: () => import('@/views/resultanalysis'),
                name: 'ResultAnalysis',
                meta: { title: '结果综合分析', icon: 'resultanalysis' },
            },
        ],
    },
    {
        path: '/earlywarning',
        component: Layout,
        redirect: '/earlywarning/index',
        alwaysShow: true, // will always show the root menu
        name: 'EarlyWarning',
        meta: {
            title: '系统预警提示',
            icon: 'earlywarning',
        },
        children: [
            {
                path: 'index',
                component: () => import('@/views/earlywarning'),
                name: 'EarlyWarningShow',
                meta: {
                    title: '系统预警展示',
                    icon: 'warningshow'
                    // roles: ['admin'] // or you can only set roles in sub nav
                },
            },
            {
                path: 'config',
                component: () => import('@/views/earlywarning/config'),
                name: 'EarlyWarningConfig',
                meta: {
                    title: '系统预警配置',
                    icon: 'config'
                    // if do not set roles, means: this page does not require permission
                },
            },
        ],
    },
    {
        path: '/monitor-engine',
        component: Layout,
        redirect: '/monitor-engine/crawler',
        alwaysShow: true, // will always show the root menu
        name: 'MonitorEngine',
        meta: {
            title: '监控引擎管理',
            icon: 'edit',
        },
        children: [
            {
                path: 'crawler',
                component: () => import('@/views/monitor-engine/crawler'),
                name: 'CrawlerConfiguration',
                meta: {
                    title: '爬虫引擎管理',
                    icon: 'bug'
                    // roles: ['admin'] // or you can only set roles in sub nav
                },
            },
            {
                path: 'detection',
                component: () => import('@/views/monitor-engine/detection'),
                name: 'DetectionConfiguration',
                meta: {
                    title: '检测引擎管理',
                    icon: 'eye-open'
                    // if do not set roles, means: this page does not require permission
                },
            },
        ],
    },
    {
        path: '/uploadvideo',
        component: Layout,
        children: [
            {
                path: 'index',
                component: () => import('@/views/uploadvideo/index'),
                name: 'UploadVideo',
                meta: { title: '上传视频检测', icon: 'upload' },
            },
        ],
    },
]

const createRouter = () =>
    new Router({
        // mode: 'history', // require service support
        scrollBehavior: () => ({ y: 0 }),
        routes: constantRoutes,
    })

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher // reset router
}

export default router
