class App {
    constructor() {
        this.activeEl = null
        this.signinForm = new SigninForm()
        this.signupForm = new SignupForm()
        this.table = new TodoTable()
        this.navLink = e('#main .main-nav .links')
        this.userState = null
        this.elMap = {
            signin: this.signinForm,
            signup: this.signupForm,
            todo: this.table,
        }
        this.init()
    }

    init() {
        this.navLink.addEventListener('click', (ev) => {
            /** @type {HTMLElement} */
            let el = ev.target

            if (el.classList.contains('logout')) {
                return this.logout()
            }

            for (let key of Object.keys(this.elMap)) {
                if (el.classList.contains(key)) {
                    this.switchEl(this.elMap[key])
                }
            }

        })

        this.signinForm
            .on('signup', () => {
                this.switchEl(this.signupForm)
            })
            .on('submit', (data) => {
                Api.login(data)
                    .then((data) => {
                        alert('登录成功')
                        this.updateUserState(data)
                    })
                    .catch((error) => {
                        alert('登录失败：', + error.message || '未知错误')
                    })
            })

        this.signupForm
            .on('signin', () => {
                this.switchEl(this.signinForm)
            })
            .on('submit', (data) => {
                Api.register(data)
                    .then(() => {
                        alert('注册成功')
                    })
                    .catch((error) => {
                        alert('注册失败：', + error.message || '未知错误')
                    })
            })

        console.log('App inited.')

        Api.passportStatus()
            .then((data) => this.updateUserState(data))
            .catch((error) => {
                alert(error)
                this.updateUserState(null)
            })
    }

    logout() {
        Api.logout()
            .then(() => {
                this.updateUserState(null)
                this.switchEl(this.signinForm)
            })
            .catch(alert)
    }

    switchEl(el) {
        if (el === this.activeEl) {
            return
        }

        el.show()
        this.activeEl && this.activeEl.hide()
        this.activeEl = el
        for (let key of Object.keys(this.elMap)) {
            if (el === this.elMap[key]) {
                for (let child of this.navLink.children) {
                    child.classList.remove('active')
                }
                this.navLink.querySelector('.' + key).classList.add('active')
            }
        }
    }

    updateUserState(data) {
        this.userState = data
        if (data && data.username) {
            e('#username').innerText = data.username
            show('#main .links .logout')
            hide('#main .links .signin')
            hide('#main .links .signup')
            this.table.fetchTodos(data.id)
            this.switchEl(this.table)
        } else {
            hide('#main .links .logout')
            show('#main .links .signin')
            show('#main .links .signup')
            e('#username').innerText = '游客'
            this.navLink.querySelector('.logout').style.display = 'none'
            this.switchEl(this.signinForm)
        }
    }
}

window.onload = () => {
    new App()
}
