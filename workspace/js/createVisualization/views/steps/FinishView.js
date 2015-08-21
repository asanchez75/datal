var FinishView = StepViewSPA.extend({

	initialize: function(){

		// Right way to extend events without overriding the parent ones
		var eventsObject = {}
		eventsObject['click a.backButton'] = 'onPreviousButtonClicked';
		eventsObject['click a.finishButton'] = 'onFinishButtonClicked';
		this.addEvents(eventsObject);

		// Bind model validation to view
		//Backbone.Validation.bind(this);

		this.render();

	}, 

	render: function(){

		var self = this;
		
		return this;
	},

	onPreviousButtonClicked: function(){
		this.previous();
	},

	onFinishButtonClicked: function(){		

		console.log(this.model.getSettings());
		this.model.save();
		alert('TODO: save! & redirect!');

	}

});