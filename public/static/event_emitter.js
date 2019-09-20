class EventEmitter {
    constructor() {
        this.handles = {}
    }

    on(eventName, callback) {
        this.handles[eventName] = [
            ...(this.handles[eventName] || []),
            callback,
        ]
        return this
    }

    remove(eventName, callback) {
        let callbacks = this.handles[eventName]
        if (callbacks) {
            let i = callbacks.indexOf(callback)
            if (i > -1) {
                callbacks.splice(i, 1)
            }
        }
        return this
    }

    emit(eventName, ...payload) {
        let callbacks = this.handles[eventName]
        callbacks && callbacks.forEach((c) => c(...payload))
    }
}
