var boxWidth = parseInt(d3.select('.chart').style('width').replace('px', '')), boxHeight = 400;
var margin = {top: 30, right: 0, bottom: 10, left: 40},
    width = boxWidth - margin.left - margin.right,
    height = boxHeight - margin.top - margin.bottom;

var svg = d3.select('.chart').append('svg').attr({
    'viewBox': '0 0 ' + boxWidth + ' ' + boxHeight,
    'preserveAspectRatio': 'xMinYMin',
    'width': '100%',
    'height': '100%',
}).append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
svg.append("g").attr("class", "x axis").attr("transform", "translate(0,-5)");
svg.append("g").attr("class", "y axis");

var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);
var xAxis = d3.svg.axis().scale(x).orient("top");
var yAxis = d3.svg.axis().scale(y).orient("left");
var format = d3.time.format("%m/%d/%Y %I:%M %p");
var colors = d3.scale.category10();
var data = [];

function drawChart(root, resolution, keys) {
    var extent = d3.extent(data, function(d) { return d[0]; });
    
    x.domain(extent).nice(d3.time.hour);
    y.domain([0, d3.max(data, function(d) {
        var m = 0;
        keys.forEach(function(k) {
            if(d[1] && d[1][k] > m) {
                m = d[1][k];
            }
        });
        return m;
    })]);
    root.select(".x.axis").transition().call(xAxis);
    root.select(".y.axis").transition().call(yAxis);
    
    d3.selectAll('path.line').remove();
    d3.selectAll('line.grid').remove();
    
    var grid = root.selectAll('.grid').data(y.ticks());
    grid.enter().append('line').attr({
        'class': 'grid',
        'x1': 0,
        'x2': width,
        'y1': function(d) { return y(d); },
        'y2': function(d) { return y(d); }
    });
    
    /*
    var area = d3.svg.area().interpolate('step-before')
        .x(function(d) { return x(d[0]); })
        .y0(function(d) { return height; })
        .y1(function(d) { return y(d[1] ? d[1].count : 0); });
    root.append("path")
        .datum(data)
        .attr("class", "area")
        .attr("d", area);
    */
    
    var int = $('select.toggle').val();
    keys.forEach(function(k) {
        var line = d3.svg.line().interpolate(int)
            .x(function(d) { return x(d[0]); })
            .y(function(d) { return y(d[1] ? d[1][k] : 0); });
        root.append("path")
            .datum(data)
            .attr("class", "line")
            .attr("stroke", function(d) { return colors(k); })
            .attr("d", line);
    });
}

function redraw() {
    var keys = [];
    $('input.toggle:checked').each(function() {
        keys.push($(this).val());
    });
    drawChart(svg, data, keys);
}

$(function() {
    var url = $('.chart').data('url');
    var res = $('.chart').data('resolution');
    $.getJSON(url, function(chartData) {
        data = chartData;
        data.forEach(function(d) { d[0] = new Date(d[0] * 1000); });
        redraw();
    });
    $('.toggle').change(function() {
        redraw();
    });
});
