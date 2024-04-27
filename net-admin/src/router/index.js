import { createRouter, createWebHashHistory } from 'vue-router';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import pinia from '/@/stores/index';
import { storeToRefs } from 'pinia';
import { useKeepALiveNames } from '/@/stores/keepAliveNames';
import { useRoutesList } from '/@/stores/routesList';
import { useThemeConfig } from '/@/stores/themeConfig';
import { Session } from '/@/utils/storage';
import { staticRoutes, notFoundAndNoPower } from '/@/router/route';
import { initFrontEndControlRoutes } from '/@/router/frontEnd';
import { initBackEndControlRoutes } from '/@/router/backEnd';

/**
 * 1、前端控制路由时：isRequestRoutes 为 false，需要写 roles，需要走 setFilterRoute 方法。
 * 2、后端控制路由时：isRequestRoutes 为 true，不需要写 roles，不需要走 setFilterRoute 方法），
 * 相关方法已拆解到对应的 `backEnd.ts` 与 `frontEnd.ts`（他们互不影响，不需要同时改 2 个文件）。
 * 特别说明：
 * 1、前端控制：路由菜单由前端去写（无菜单管理界面，有角色管理界面），角色管理中有 roles 属性，需返回到 userInfo 中。
 * 2、后端控制：路由菜单由后端返回（有菜单管理界面、有角色管理界面）
 */

// 读取 `/src/stores/themeConfig.ts` 是否开启后端控制路由配置
const storesThemeConfig = useThemeConfig(pinia);
const { themeConfig } = storeToRefs(storesThemeConfig);
const { isRequestRoutes } = themeConfig.value;

/**
 * 创建一个可以被 Vue 应用程序使用的路由实例
 * @method createRouter(options: RouterOptions): Router
 * @link 参考：https://next.router.vuejs.org/zh/api/#createrouter
 */
export const router = createRouter({
	history: createWebHashHistory(),
	/**
	 * 说明：
	 * 1、notFoundAndNoPower 默认添加 404、401 界面，防止一直提示 No match found for location with path 'xxx'
	 * 2、backEnd.ts(后端控制路由)、frontEnd.ts(前端控制路由) 中也需要加 notFoundAndNoPower 404、401 界面。
	 *    防止 404、401 不在 layout 布局中，不设置的话，404、401 界面将全屏显示
	 */
	routes: [...notFoundAndNoPower, ...staticRoutes],
});

/**
 * 路由多级嵌套数组处理成一维数组
 * @param arr 传入路由菜单数据数组
 * @returns 返回处理后的一维路由菜单数组
 */
// export function formatFlatteningRoutes(arr) {
// 	if (arr.length <= 0) return false;
// 	for (let i = 0; i < arr.length; i++) {
// 		if (arr[i].children) {
// 			arr = arr.slice(0, i + 1).concat(arr[i].children, arr.slice(i + 1));
// 		}
// 	}
// 	return arr;
// }
export function formatFlatteningRoutes(arr) {
	// 如果数组为空，则返回空数组  
	if (arr.length === 0) return [];

	let flattened = []; // 用于存储扁平化后的路由数组  

	// 递归函数，用于展开children  
	function flatten(routes) {
		routes.forEach(route => {
			flattened.push(route); // 将当前路由添加到扁平化数组中  
			if (route.children) {
				flatten(route.children); // 递归处理子路由  
			}
		});
	}

	flatten(arr); // 从顶层路由开始展开  
	return flattened; // 返回扁平化后的路由数组  
}


/**
 * 一维数组处理成多级嵌套数组（只保留二级：也就是二级以上全部处理成只有二级，keep-alive 支持二级缓存）
 * @description isKeepAlive 处理 `name` 值，进行缓存。顶级关闭，全部不缓存
 * @link 参考：https://v3.cn.vuejs.org/api/built-in-components.html#keep-alive
 * @param arr 处理后的一维路由菜单数组
 * @returns 返回将一维数组重新处理成 `定义动态路由（dynamicRoutes）` 的格式
 */
// export function formatTwoStageRoutes(arr) {
// 	if (arr.length <= 0) return false;
// 	const newArr = [];
// 	const cacheList = [];
// 	arr.forEach((v) => {
// 		if (v.path === '/') {
// 			newArr.push({ component: v.component, name: v.name, path: v.path, redirect: v.redirect, meta: v.meta, children: [] });
// 		} else {
// 			// 判断是否是动态路由（xx/:id/:name），用于 tagsView 等中使用
// 			// 修复：https://gitee.com/lyt-top/vue-next-admin/issues/I3YX6G
// 			if (v.path.indexOf('/:') > -1) {
// 				v.meta['isDynamic'] = true;
// 				v.meta['isDynamicPath'] = v.path;
// 			}
// 			newArr[0].children.push({ ...v });
// 			// 存 name 值，keep-alive 中 include 使用，实现路由的缓存
// 			// 路径：/@/layout/routerView/parent.vue
// 			if (newArr[0].meta.isKeepAlive && v.meta.isKeepAlive) {
// 				cacheList.push(v.name);
// 				const stores = useKeepALiveNames(pinia);
// 				stores.setCacheKeepAlive(cacheList);
// 			}
// 		}
// 	});
// 	return newArr;
// }
export function formatTwoStageRoutes(arr) {
	if (arr.length === 0) return []; // 返回空数组而不是 false  

	const newArr = [];
	const cacheList = [];

	// 假设我们只有一个顶层路由，即 path 为 '/' 的路由  
	let topRoute = null;

	arr.forEach((route) => {
		if (route.path === '/') {
			topRoute = { ...route, children: [] }; // 复制顶层路由并初始化 children 为空数组  
			newArr.push(topRoute);
		} else {
			// 判断是否是动态路由  
			if (route.path.includes('/:')) { // 使用 includes 替代 indexOf 来检测动态路径  
				route.meta = route.meta || {}; // 确保 meta 存在  
				route.meta.isDynamic = true;
				route.meta.isDynamicPath = route.path;
			}

			// 将当前路由添加到顶层路由的 children 中  
			if (topRoute) {
				topRoute.children.push({ ...route });
			}

			// 缓存逻辑  
			if (topRoute.meta?.isKeepAlive && route.meta?.isKeepAlive) {
				cacheList.push(route.name);
				// 假设 useKeepALiveNames 和 setCacheKeepAlive 是在外部定义的  
				// 你需要确保它们可用，或者将相关的逻辑移到这个函数之外  
				// const stores = useKeepALiveNames(pinia); // 如果需要 pinia，请作为参数传入  
				// stores.setCacheKeepAlive(cacheList);  
			}
		}
	});

	// 如果需要处理缓存逻辑，请在这里处理 cacheList  

	return newArr;
}


// 路由加载前
router.beforeEach(async (to, from, next) => {
	NProgress.configure({ showSpinner: false });
	if (to.meta.title) NProgress.start();
	const token = Session.get('token');
	if (to.path === '/login' && !token) {
		next();
		NProgress.done();
	} else {
		if (!token) {
			next(`/login?redirect=${to.path}&params=${JSON.stringify(to.query ? to.query : to.params)}`);
			Session.clear();
			NProgress.done();
		} else if (token && to.path === '/login') {
			next('/home');
			NProgress.done();
		} else {
			const storesRoutesList = useRoutesList(pinia);
			const { routesList } = storeToRefs(storesRoutesList);
			if (routesList.value.length === 0) {
				if (isRequestRoutes) {
					// 后端控制路由：路由数据初始化，防止刷新时丢失
					await initBackEndControlRoutes();
					// 解决刷新时，一直跳 404 页面问题，关联问题 No match found for location with path 'xxx'
					// to.query 防止页面刷新时，普通路由带参数时，参数丢失。动态路由（xxx/:id/:name"）isDynamic 无需处理
					next({ path: to.path, query: to.query });
				} else {
					// https://gitee.com/lyt-top/vue-next-admin/issues/I5F1HP
					await initFrontEndControlRoutes();
					next({ path: to.path, query: to.query });
				}
			} else {
				next();
			}
		}
	}
});

// 路由加载后
router.afterEach(() => {
	NProgress.done();
});

// 导出路由
export default router;
