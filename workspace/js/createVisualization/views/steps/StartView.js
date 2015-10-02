var StartView = StepViewSPA.extend({

	initialize: function(){

		// Right way to extend events without overriding the parent ones
		this.addEvents({
			'click .chart-type':'onChooseType',
			'click .map-type':'onChooseMap'
		});

		// Bind model validation to view
		//Backbone.Validation.bind(this);

		this.nav();
		this.render();
	}, 

	onChooseType: function (e) {
		e.stopPropagation();
		var $target = $(e.currentTarget),
			type = $target.data('type');
		this.model.set('isMap', false);
		this.model.set('type', type);
		this.setFlow('charts');
		this.next();
	},

	onChooseMap: function (e) {
		e.stopPropagation();
		var $target = $(e.currentTarget),
			type = $target.data('type');
		this.model.set('isMap', true);
		this.model.set('type', type);
		this.setFlow('maps');
		this.next();
	},

	nav: function(){
		var nav = $('.navCreator'),
			navLi = $('.navCreator li'),
			navPicker = $('.navCreatorPicker');

		nav.find('.navCreatorPicker:first').show();
		
		navLi.not('.heading').click(function() {
			nav.find('.active').removeClass('active');
			$(this).addClass('active');
			navPicker.hide();
			$(this).find(navPicker).show();
		});
	},

	start: function(){
		this.constructor.__super__.start.apply(this);
		this.setFlow(null);

		if(this.model.get('isEdit')){
			this.model.set('type', this.model.get('type'));
			if(this.model.get('type')=='mapchart'){
	            this.model.set('isMap', true);
	            this.setFlow('maps');
	        }else{
	            this.model.set('isMap', false);
	            this.setFlow('charts');
        	}
			this.next();
        }
	}

});