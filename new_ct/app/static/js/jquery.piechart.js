(function($){

  $.fn.piechart = function(options){

    //default option
    var settings = $.extend({
      piedata : [],
      pievalue : [],
      piecolor : [],
      pieradius : 4,
      strokecolor : [],
      lineWidth : 1,
      label : "Caption",
      canvasSize : "450px"
    },options);

    //calculate total value
    var total = 0;
    for(var i =0 ; i < settings.pievalue.length ; i++){
      total += parseInt(settings.pievalue[i],10);
    }


    $elem = $(this);
    $elem.css('width','750px');
    //Create Table
    $elem.prepend('<canvas class="pie" width="'+settings.canvasSize+'" height="'+settings.canvasSize+'"></canvas>');
    $elem.append('<div class="pie-table"><table class="pie-label"></table></div>');
    $elem.find($('.pie-label')).prepend('<caption>'+settings.label+'</caption>');
    $elem.find($('.pie-label')).append('<tr><th>Color</th><th>Data</th><th>Value</th><th>Percentage</th></tr>');

    //create table
    for (var j = 0 ; j < settings.pievalue.length ; j++){
      var piepiece = parseInt(settings.pievalue[j],10)/total;
                var num = (piepiece * 100).toFixed(2);
                $elem.find($('.pie-label')).append('<tr></tr>');
                $elem.find($('.pie-label tr')).eq(j+1).prepend('<td></td>');
                $elem.find($('.pie-label tr')).eq(j+1).children('td').eq(0).css("background-color",settings.piecolor[j]);
                if(settings.piecolor == ''){
                  $elem.find($('.pie-label tr')).eq(j+1).children('td').eq(0).css("background-color",settings.strokecolor[j]);
                }
                $elem.find($('.pie-label tr')).eq(j+1).append('<td></td>');
                $elem.find($('.pie-label tr')).eq(j+1).children('td').eq(1).text(settings.piedata[j]);
                $elem.find($('.pie-label tr')).eq(j+1).append('<td></td>');
                $elem.find($('.pie-label tr')).eq(j+1).children('td').eq(2).text(settings.pievalue[j]);
                $elem.find($('.pie-label tr')).eq(j+1).append('<td></td>');
                $elem.find($('.pie-label tr')).eq(j+1).children('td').eq(3).text(num + '%');
      }
    //make canvas ready
    var canvas = $elem.find($('.pie'))[0];
    var ctx = canvas.getContext('2d');

    //set startangle,radius and position of pie
    var startangle = 0;
    var radius = canvas.height /settings.pieradius;
    var xpos = canvas.width / 2;
    var ypos = canvas.height / 2;

    //loop to create every pie piece
    for (var j = 0 ; j < settings.pievalue.length ; j++){
        (function(j){
            window.setTimeout(function(){
               
                var piepiece = parseInt(settings.pievalue[j],10)/total;
               
                var endangle = 2 * Math.PI * piepiece;
                var angle = startangle + endangle;
                ctx.beginPath();
                ctx.lineWidth = settings.lineWidth;
                ctx.arc(xpos, ypos, radius, startangle, angle , false);
                ctx.lineTo(xpos,ypos);
                ctx.closePath();
                if(settings.strokecolor == ''){
                  ctx.strokeStyle = 'none';
                }
                else if(settings.strokecolor == 'default'){
                   ctx.strokeStyle = 'black';
                }
                else{
                  ctx.strokeStyle = settings.strokecolor[j];
                }
                

                if(settings.piecolor == ''){
                    ctx.fillStyle = "none";
                }else{
                   ctx.fillStyle = settings.piecolor[j];
                }
                
                ctx.lineJoin= 'bevel';
                ctx.fill();    
                ctx.stroke(); 
                startangle += endangle;
          },j * 500);
      }(j));
    }


    

  };
})(jQuery);