
ofaudit.define('web.core', function (require) {
    "use strict";

    var Class = require('web.Class');
    var Registry = require('web.Registry');
    return {
        // core classes and functions
        Class: Class,
        // registries
        action_registry : new Registry(),
        list_widget_registry: new Registry(),
    };

});

