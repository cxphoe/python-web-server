/**
 *
 * @param {string} sel
 * @returns {HTMLElement}
 */
const e = (sel) => document.querySelector(sel)
const eAll = (sel) => document.querySelectorAll(sel)

const hide = (sel) => {
    if (typeof sel === 'string') {
        sel = e(sel)
    }

    sel.style.display = 'none'
}

const show = (sel) => {
    if (typeof sel === 'string') {
        sel = e(sel)
    }

    sel.style.display = ''
}

/**
 * 模拟 vue 中的 v-model
 * @param {string} sel 选择器
 * @param {*} obj
 * @param {string} field 要设置的 obj 中的字段名
 */
const vModel = (sel, obj, field) => {
    /** @type {HTMLInputElement} */
    let el = e(sel)
    if (!el) {
        return console.error(`未找到选择器 \`${sel}\` 对应的元素`)
    }
    Object.defineProperty(obj, field, {
        set(v) {
            el.value = v
        },
        get() {
            return el.value
        },
    })
}

const getCookie = (field) => {
    let parts = document.cookie.split('; ')
    for (let p of parts) {
        let splitIndex = p.indexOf('=')
        let key
        let value
        if (splitIndex < 0) {
            [key, value] = [p, '']
        } else {
            [key, value] = [p.slice(0, splitIndex), p.slice(splitIndex + 1)]
        }
        if (key === field) {
            return value
        }
    }
    return ''
}

const urlWithQuery = (url, params) => {
    if (!params) {
        return url
    }
    let delimiter = url.indexOf('?') > -1 ? '&' : '?'
    let query = Object.keys(params).map((k) => `${k}=${params[k]}`).join('&')
    return url + delimiter + query
}

/** @typedef {'GET' | 'POST' | 'PUT' | 'DELETE' | 'HEAD' | 'OPTIONS'} RequestMethod */
/** @typedef {{url: string, type: RequestMethod, data: {}, headers: {}, timeout: number}} RequestOptions */


const http = {
    /**
     * @param {RequestOptions} options
     */
    async request(options) {
        // 初始化请求参数
        options = {
            url: '', // string
            type: 'GET', // string 'GET' 'POST' 'DELETE'
            data: null, // any 请求参数,data需要和请求头Content-Type对应
            headers: {}, // object 请求头
            timeout: 10000, // string 超时时间:0 表示不设置超时
            ...options,
        }
        // 参数验证
        if (!options.url || !options.type) {
            alert('参数有误')
            return
        }
        let xhr = new XMLHttpRequest()
        let method = options.type.toUpperCase()
        let useUrlParam = method === 'GET' || method === 'DELETE'
        // 如果是"简单"请求,则把data参数组装在url上
        if (useUrlParam) {
            options.url = urlWithQuery(options.url, options.data)
        }
        // 初始化请求
        xhr.open(options.type, options.url)
        // 设置 csrf-token
        xhr.setRequestHeader('x_csrf_token', getCookie('csrf_token'))

        // 设置请求头
        for (const key of Object.keys(options.headers)) {
            xhr.setRequestHeader(key, options.headers[key])
        }
        // 设置超时时间
        if (options.timeout) {
            xhr.timeout = options.timeout
        }

        return new Promise((resolve, reject) => {
            // 发送请求.如果是简单请求,请求参数应为null.否则,请求参数类型需要和请求头Content-Type对应
            xhr.send(useUrlParam ? null : http.getQueryData(options.data, xhr))
            // 请求成功回调函数
            xhr.onreadystatechange = (ev) => {
                if (xhr.readyState !== 4) {
                    return
                }

                const status = xhr.status
                if ((status >= 200 && status < 300) || status === 304) {
                    let res = xhr.response
                    try {
                        res = JSON.parse(res)
                    } catch {}
                    resolve(res)
                } else {
                    reject(`status: ${status}`)
                }
            }
            xhr.addEventListener('error', () => {
                reject(`status: ${xhr.status}`)
            })
            // 请求超时
            xhr.addEventListener('timeout', () => {
                reject('请求超时')
            })
        })
    },
    // 获取ajax请求参数
    getQueryData(data, xhr) {
        if (!data) {
            return null;
        }
        if (typeof data === 'string') {
            return data;
        }
        if (data instanceof FormData) {
            return data;
        }
        xhr.setRequestHeader('Content-type', 'application/json;charset=utf-8')
        return JSON.stringify(data)
    },
    // 把对象转为查询字符串
    getQueryString(data) {
        let paramsArr = [];
        if (data instanceof Object) {
            Object.keys(data).forEach(key => {
                let val = data[key];
                paramsArr.push(encodeURIComponent(key) + '=' + encodeURIComponent(val));
            });
        }
        return paramsArr.join('&');
    },
}
