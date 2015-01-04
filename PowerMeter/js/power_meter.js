var devices = [];
var selected_device = "";
var read_timer;

 /*--- power switch on/off---*/

$(document).ready(function () {

}); // end ready

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

	$('.sw60').click(function() {
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
	if( data.length > 37)
	{
	    var splitData = data.split(':');		
	    temp = splitData[0].split('=');	V_r = temp[1];
	    temp = splitData[1].split('=');	V_s = temp[1];			
	    temp = splitData[2].split('=');	V_t = temp[1];
	    temp = splitData[3].split('=');	I_r = temp[1];
	    temp = splitData[4].split('=');	I_s = temp[1];
	    temp = splitData[5].split('=');	I_t = temp[1];
	    temp = splitData[6].split('=');	Watt = temp[1];
	    temp = splitData[7].split('=');	Var = temp[1];
	    temp = splitData[8].split('=');	Pf = temp[1];
	    temp = splitData[10].split('='); Total = temp[1];

	    $('#i_a').val(I_r);	
	    $('#i_b').val(I_s);	
	    $('#i_c').val(I_t);	
	    $('#v_a').val(V_r);	
	    $('#v_b').val(V_s);	
	    $('#v_c').val(V_t);	
	    $('#watt').val(Watt);	
	    $('#var').val(Var);	
	    $('#pf').val(Pf);	
	    $('#total').val(Total);	

            temp = splitData[12];
        }
        else{
            temp = data;
	    I_r = I_s = I_t = 0;			
	    V_r = V_s = V_t = 0;			
	    Watt = Var = Pf = 0;			
        }
        
        if( temp[0] == '0'){document.getElementById('lamp1').style.background='black';}
	else{ document.getElementById('lamp1').style.background='red';}
	if( temp[1] == '0'){ document.getElementById('lamp2').style.background='black';	}
	else{   document.getElementById('lamp2').style.background='red';}
	if( temp[2] == '0'){ document.getElementById('lamp3').style.background='black';	}
	else
        {
	    document.getElementById('lamp3').style.background='red';
	}
	if( temp[3] == '0')
        {
	    document.getElementById('lamp4').style.background='black';
	}
	else
        {
	    document.getElementById('lamp4').style.background='red';
	}
	if( temp[4] == '0')
        {
	    document.getElementById('lamp5').style.background='black';
	}
	else
        {
	    document.getElementById('lamp5').style.background='red';
	}
	if( temp[5] == '0')
        {
	    document.getElementById('lamp6').style.background='black';
	}
	else
        {
	    document.getElementById('lamp6').style.background='red';
	}
	if( temp[6] == '0')
        {
	    document.getElementById('lamp7').style.background='black';
	}
	else
        {
	    document.getElementById('lamp7').style.background='red';
	}
	if( temp[7] == '0')
        {
	    document.getElementById('lamp8').style.background='black';
	}
	else
        {
	    document.getElementById('lamp8').style.background='red';
	}
    }


function realtimeClock() {
  setTimeout('realtimeClock()', 5000);
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
	
	// read_timer = setTimeout(readData, 2000);
}