var TagModel = Backbone.Model.extend({
	
	defaults: {
		name: ""
	},

	validation: {
        name: {
            maxLength: 40, // TODO get from model.tags.name length
            msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 40 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
            }
        }

});