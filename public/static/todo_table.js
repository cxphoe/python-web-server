class TodoTable {
    constructor() {
        this.todos = []
        this.props = {
            content: '',
        }
        this.userId = undefined
        this.init()
    }

    init() {
        vModel('#todo-list .add-todo-input', this.props, 'content')
        let todoList = e('#todo-list')
        todoList.addEventListener('click', (ev) => {
            /** @type {HTMLElement} */
            let el = ev.target
            if (el.classList.contains('add')) {
                let value = this.props.content
                if (value) {
                    Api.addTodo({
                        title: value,
                    })
                        .then(() => {
                            this.fetchTodos()
                            this.props.content = ''
                        })
                        .catch(alert)
                }
            } else if (el.classList.contains('check-todo')) {
                let p = el.parentElement
                this.updateTodo(parseInt(p.parentElement.dataset.id), {
                    completed: p.classList.contains('checked') ? 0 : 1,
                })
            } else if (el.classList.contains('btn') && el.closest('.todo-info')) {
                console.log(el)
                let $ctn = el.parentElement.parentElement.parentElement
                if (el.classList.contains('edit')) {
                    $ctn.classList.add('editable')
                } else if (el.classList.contains('delete')) {
                    this.deleteTodo($ctn.dataset.id)
                }
            } else if (el.classList.contains('btn') && el.closest('.edit-todo')) {
                let $ctn = el.parentElement.parentElement
                if (el.classList.contains('cancel')) {
                    // 取消编辑
                    $ctn.classList.remove('editable')
                } else {
                    // 提交编辑
                    let content = el.parentElement.querySelector('input').value
                    let todoId = $ctn.dataset.id
                    this.updateTodo(todoId, {
                        title: content,
                    })
                }
            }
        })

        let todoItems = e('#todo-items')
        let prevActiveItem = null
        todoItems.addEventListener('mouseover', (ev) => {
            /** @type {HTMLElement} */
            let el = ev.target
            if (el.dataset.id !== undefined) {
                if (prevActiveItem) {
                    prevActiveItem.classList.add('hide')
                }
                prevActiveItem = el.querySelector('.operation')
                prevActiveItem.classList.remove('hide')
            }
        })
        todoItems.addEventListener('mouseleave', (ev) => {
            if (prevActiveItem) {
                prevActiveItem.classList.add('hide')
                prevActiveItem = null
            }
        })
    }

    fetchTodos(userId) {
        if (userId === undefined) {
            this.userId !== undefined && (userId = this.userId)
        } else {
            this.userId = userId
        }

        Api.fetchTodo(userId)
            .then((userInfo) => this.updateTodos(userInfo))
            .catch(alert)
    }

    async updateTodo(id, payload) {
        id = Number(id)
        Api.updateTodo(id, payload)
            .then(() => this.fetchTodos())
            .catch(alert)
    }

    async deleteTodo(id) {
        id = Number(id)
        Api.deleteTodo(id)
            .then(() => this.fetchTodos())
            .catch(alert)
    }

    updateTodos(todos) {
        e('#todo-items').innerHTML = todos
            .map((t) => `
                <tr>
                    <td data-id=${t.id}>
                        <span class="todo-info ${t.completed ? 'checked' : ''}">
                            <i class="rs-icon check-todo">&#xe617;</i>
                            <span class="content">${t.title}</span>
                            <span class="operation hide">
                                <a class="btn edit">编辑</a>
                                <a class="btn delete">删除</a>
                            </span>
                        </span>
                        <span class="edit-todo">
                            <input value="${t.title}"/>
                            <a class="btn">提交</a>
                            <a class="btn cancel">取消</a>
                        </span>
                    </td>
                </tr>
            `)
            .join('')
    }

    hide() {
        e('#main .todo-list-ctn').classList.add('hide')
    }

    show() {
        e('#main .todo-list-ctn').classList.remove('hide')
    }
}
