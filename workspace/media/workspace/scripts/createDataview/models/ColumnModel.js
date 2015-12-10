var ColumnModel = Backbone.Model.extend({
    defaults: {
        column: undefined,
        type: 'TEXT',
        originPattern: undefined,
        customPattern: undefined,

        separatorType: 'symbol',
        thousandSeparator: undefined,
        decimalSeparator: undefined,
    },

    validation: {
        column: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],
        originPattern: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],

        customPattern: function(value, attr) {
            if (this.get('originPattern') === 'custom') {
                if(_.isUndefined(value)) {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            } 
        },

        thousandSeparator: function(value, attr) {
            if (this.get('separatorType') === 'symbol') {
                if(_.isUndefined(value)) {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            } 
        },

        decimalSeparator: function(value, attr) {
            if (this.get('separatorType') === 'symbol') {
                if(_.isUndefined(value)) {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            } 
        }
    },

});