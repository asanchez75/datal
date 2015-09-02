/**
 * Backbone View for charts and maps
 */
var viewChartView = Backbone.View.extend({
    el : "body",
    chartContainer: "#id_visualizationResult",
    initialize : function() {
        this.listenTo(this.model, "change", this.render);

        this.chartsFactory = new charts.ChartsFactory();

        this.setupChart();
        this.render();
    },
    setupChart: function () {
        this.chartOptions = JSON.parse(this.model.get('chartJson')).chart;

        var chartSettings = this.chartsFactory.create(this.chartOptions.type,this.chartOptions.lib);

        this.ChartViewClass = chartSettings.Class;
        this.ChartModelClass = charts.models.Chart;
    },
    render: function () {
        this.initializeChart();
        return this;
    },
    initializeChart: function () {
        if(typeof this.chartInstance === 'undefined'){
            this.createChartInstance();
        }
    },
    createChartInstance: function () {
        this.setChartContainerHeight();

        var chartModelInstance = new this.ChartModelClass({
            type: this.model.get('chart.type'),
            resourceUrl: 'http://data.cityofsacramento.org/visualizations/invoke',
            resourceIdAttribute: 'visualization_revision_id',
            resourceID: 6741,
            options: {
                zoom: parseInt(this.chartOptions.zoom, 10),
                center: {
                    lat: this.chartOptions.center.lat,
                    long: this.chartOptions.center.long
                }
            }
        });

        this.chartInstance = new this.ChartViewClass({
            el: this.chartContainer,
            model: chartModelInstance
        });
    },
    setLoading: function () {
        
    },
    setHeights : function(theContainer, theHeight) {
        if (typeof theHeight == 'undefined') {theHeight = 0;}

        var heightContainer = String(theContainer);
        var tabsHeight = parseFloat($('.tabs').height());
        var otherHeight = theHeight;
        var minHeight = tabsHeight - otherHeight;

        $(heightContainer).css('min-height', minHeight + 'px');

        $(window).resize(function() {
            var height = parseFloat($(window).height())
                - parseFloat(otherHeight)
                - parseFloat($('.brandingHeader').height())
                - parseFloat($('.content').css('padding-top').split('px')[0])
                - parseFloat($('.content').css('padding-bottom').split('px')[0])
                // - parseFloat($('.brandingFooter').height() )
                - parseFloat($('.miniFooterJunar').height());
            $(heightContainer).height(height);
        }).resize();

    },
    setChartContainerHeight:function(){
        var otherHeights =
              parseFloat( $('.dataTable header').height() )
            + parseFloat( $('.dataTable header').css('padding-top').split('px')[0] )
            + parseFloat( $('.dataTable header').css('padding-bottom').split('px')[0] )
            + parseFloat( $('.dataTable header').css('border-bottom-width').split('px')[0] )
            + 2;// Fix to perfection;

        this.setHeights( this.chartContainer, otherHeights );

        $(this.chartContainer).css({
            overflow: 'auto'
        })

    },
});