var devices = [];
var selected_device = "";
var read_timer;

 /*--- power switch on/off---*/
 

webiopi().ready(function() {
	realtimeClock();

	$('.cube-switch .switch').click(function() {
	    if ($('.cube-switch').hasClass('active')) {

		var args = ['OFF'];

		webiopi().callMacro('stopMonitor',args,function(msg) {
			console.log(msg);
		});

	        $('.cube-switch').removeClass('active');
	        $('#light-bulb2').css({'opacity': '0'});
	    } else {
		var args = ['ON'];

		webiopi().callMacro('startMonitor',args,function(msg) {
			console.log(msg);
		});

	        $('.cube-switch').addClass('active');

	        $('#light-bulb2').css({'opacity': '1'});
	    }
	});

	$('#check6').on('checked',(function() {
	    if ($('.sw60').hasClass('active')) {
		var args = ['OFF'];

		webiopi().callMacro('Relay3_Off',args,function(msg) {
			console.log(msg);
		});

	        $('.sw60').removeClass('active');

	    } else {
		var args = ['ON'];

		webiopi().callMacro('Relay3_On',args,function(msg) {
			console.log(msg);
		});

	        $('.sw60').addClass('active');

	    }
	});

	$('#coil_on').on('click', function() {
		callMacro();		
	});

	$('#coil_off').on('click', function() {
		var args = ['off'];
		webiopi().callMacro("CoilCtrl", args, function(msg){
			console.log(msg);
		});
	});
});



function callMacro() {
                var arg =['on'] // or whatever you want
                // call myMacro(arg)
                webiopi().callMacro("CoilCtrl", arg, macroCallback);
        }
        
        function macroCallback(macro, args, data) {
		console.log(data);
		var buf = data.split(':');
		console.log(buf);

		$('#i_a').val(buf[0]);	
		$('#i_b').val(buf[1]);	
		$('#i_c').val(buf[2]);	
		$('#v_a').val(buf[3]);	
		$('#v_b').val(buf[4]);	
		$('#v_c').val(buf[5]);	
		$('#watt').val(buf[6]);	
		$('#var').val(buf[7]);	
		$('#pf').val(buf[8]);	
		$('#total').val(buf[10]);	
            }


function realtimeClock() {
  refreshTime();
  setTimeout('realtimeClock()', 1000);
}


function refreshTime() { // 24시간제
  var d = new Date();

    $('#year').val(leadingZeros(d.getFullYear(), 4));
    $('#month').val(leadingZeros(d.getMonth() + 1, 2));
    $('#day').val(leadingZeros(d.getDate(), 2));
    $('#hour').val(leadingZeros(d.getHours(), 2));
    $('#min').val(leadingZeros(d.getMinutes(), 2));
}


function leadingZeros(n, digits) {
  var zero = '';
  n = n.toString();

  if (n.length < digits) {
    for (i = 0; i < digits - n.length; i++)
      zero += '0';
  }
  return zero + n;
}

function readData() {
	var args = [];
	webiopi().callMacro("ReadData", args, function(msg) {
		console.log(msg);
		var buf = msg.split(' ');
		$('#i_a').val(buf[0]);	
		$('#i_b').val(buf[1]);	
		$('#i_c').val(buf[2]);	
		$('#v_a').val(buf[3]);	
		$('#v_b').val(buf[4]);	
		$('#v_c').val(buf[5]);	
		$('#watt').val(buf[6]);	
		$('#var').val(buf[7]);	
		$('#pf').val(buf[8]);	
	});
	
	// read_timer = setTimeout(readData, 1000);
}