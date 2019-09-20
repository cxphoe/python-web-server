/**
 * api 封装
 */

const apis = {
    LOGIN: '/api/login',
    LOGOUT: '/api/logout',
    REGISTER: '/api/register',
    FETCH_TODO: '/api/todo',
    ADD_TODO: '/api/todo/add',
    UPDATE_TODO: '/api/todo/update',
    DELETE_TODO: '/api/todo/delete',
    COMPLETE_TODO: '/api/todo/complete',
}



const Api = {
    async addTodo(payload) {
        const { code, msg, data } = await http.request({
            url: apis.ADD_TODO,
            type: 'POST',
            data: payload,
        })
        if (code !== 0) {
            throw new Error(msg)
        }
        return data
    },
    async fetchTodo(userId) {
        const res = await http.request({
            url: apis.FETCH_TODO,
            type: 'GET',
            data: {
                userId,
            },
        })
        return res.data
    },
    async updateTodo(id, payload) {
        const { code, msg, data } = await http.request({
            url: apis.UPDATE_TODO,
            type: 'POST',
            data: {
                ...payload,
                id,
            },
        })
        if (code !== 0) {
            throw new Error('更新 todo 失败：' + msg)
        }
        return data
    },
    async deleteTodo(id) {
        const { code, msg, data } = await http.request({
            url: apis.DELETE_TODO,
            type: 'POST',
            data: {
                id,
            },
        })
        if (code !== 0) {
            throw new Error('删除 todo 失败：' + msg)
        }
        return data
    },

    async passportStatus() {
        const { code, msg, data } = await http.request({
            url: '/api/passport/status',
            type: 'get',
        })
        if (code !== 0) {
            throw new Error (`${code}: ${msg}`)
        }
        return data
    },
    async login(layout) {
        const {code, msg, data } = await http.request({
            url: apis.LOGIN,
            type: 'POST',
            data: layout,
        })
        if (code !== 0) {
            throw new Error(`${code}/${msg}`)
        }
        return data
    },
    async logout() {
        const { code, msg } = await http.request({
            url: apis.LOGOUT,
        })
    },
    async register(payload) {
        const { code, msg, data } = await http.request({
            url: apis.REGISTER,
            type: 'POST',
            data: payload,
        })
        if (code !== 0) {
            throw new Error(`${code}/${msg}`)
        }
        return data
    },
}
