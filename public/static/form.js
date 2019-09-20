class SigninForm extends EventEmitter {
    constructor() {
        super()
        this.props = {
            username: '',
            password: '',
        }
        this.init()
    }

    init() {
        vModel('#main .signin-form .name-input', this.props, 'username')
        vModel('#main .signin-form .password-input', this.props, 'password')
        e('#main .signin-form').addEventListener('click', (ev) => {
            /** @type {HTMLElement} */
            const el = ev.target
            if (el.classList.contains('to-signup')) {
                this.emit('signup')
            } else if (el.classList.contains('signin')) {
                this.emit('submit', {
                    username: this.props.username,
                    password: this.props.password,
                })
            }
        })
    }

    show() {
        this.props.password = ''
        this.props.username = ''
        e('#main .signin-form').classList.remove('hide')
    }

    hide() {
        e('#main .signin-form').classList.add('hide')
    }
}

class SignupForm extends EventEmitter {
    constructor() {
        super()
        this.props = {
            username: '',
            password: '',
            recheck: '',
        }
        this.init()
    }

    init() {
        vModel('#main .signup-form .name-input', this.props, 'username')
        vModel('#main .signup-form .password-input', this.props, 'password')
        vModel('#main .signup-form .recheck-input', this.props, 'recheck')
        e('#main .signup-form').addEventListener('click', (ev) => {
            /** @type {HTMLElement} */
            const el = ev.target
            if (el.classList.contains('to-signin')) {
                this.emit('signin')
            } else if (el.classList.contains('signup')) {
                if (this.props.password !== this.props.recheck) {
                    return alert('两次输入的密码不一致')
                }
                this.emit('submit', {
                    username: this.props.username,
                    password: this.props.password,
                })
            }
        })
    }

    show() {
        this.props.password = ''
        this.props.username = ''
        this.props.recheck = ''
        e('#main .signup-form').classList.remove('hide')
    }

    hide() {
        e('#main .signup-form').classList.add('hide')
    }
}
