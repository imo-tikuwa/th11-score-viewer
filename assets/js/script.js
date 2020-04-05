(function (w) {
    var isArray = Array.isArray;

    /**
     * オブジェクトや配列の特定のキーの値だけを取り出す
     * @param {Object|Array.<Object>} object
     * @param {string|Array.<string>} path
     * @returns {*}
     */
    function property(object, path) {
        if (object == null || typeof object != 'object') return;
        return (isArray(object)) ? object.map(createProcessFunction(path)) : createProcessFunction(path)(object);
    }

    function createProcessFunction(path) {
        if (typeof path == 'string') path = path.split('.');
        if (!isArray(path)) path = [path];

        return function (object) {
            var index = 0,
                length = path.length;

            while (index < length) {
                object = object[toString(path[index++])];
            }
            return (index && index == length) ? object : void 0;
        };
    }

    function toString(value) {
        if (value == null) return '';
        if (typeof value == 'string') return value;
        if (isArray(value)) return value.map(toString) + '';
        var result = value + '';
        return '0' == result && 1 / value == -(1 / 0) ? '-0' : result;
    }

    w.property = property;
})(window);