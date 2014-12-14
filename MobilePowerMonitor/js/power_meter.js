var devices = [];
var selected_device = "";
var read_timer;

 /*--- power switch on/off---*/

$(document).ready(function () {
  var spin1 = new spinbutton('sb1', 'sb1_up', 'sb1_down', 50);  
  var spin2 = new spinbutton('sb2', 'sb2_up', 'sb2_down', 30);  
}); // end ready

function spinbutton(id, upID, downID, skipVal) {

  // define widget attributes
  this.$id = $('#' + id);

  this.upID = upID;
  this.$upButton = $('#' + upID);
  this.downID = downID;
  this.$downButton = $('#' + downID);
  this.skipVal = skipVal;

  this.valMin = parseInt(this.$id.attr('aria-valuemin'));
  this.valMax = parseInt(this.$id.attr('aria-valuemax'));
  this.valNow = parseInt(this.$id.attr('aria-valuenow'));

  this.keys = {
    pageup:   33,
    pagedown: 34,
    end:      35,
    home:     36,
    left:     37,
    up:       38,
    right:    39,
    down:     40 
  };
    
  // bind event handlers
  this.bindHandlers();
}
// Function bindHandlers() is a member function to bind event handlers for the spinbutton control
//
// @return N/A
//

spinbutton.prototype.bindHandlers = function() {

  var thisObj = this;

  //////// bind mouse event handlers to the up button //////////////
  this.$upButton.mousedown(function(e) {
    return thisObj.handleMouseDown(e, $(this)); 
  });

  this.$upButton.mouseup(function(e) {
    return thisObj.handleMouseUp(e, $(this)); 
  });

  this.$upButton.mouseenter(function(e) {
    return thisObj.handleMouseEnter(e, $(this)); 
  });

  this.$upButton.mouseout(function(e) {
    return thisObj.handleMouseOut(e, $(this)); 
  });

  this.$upButton.click(function(e) {
    return thisObj.handleClick(e, $(this)); 
  });

  //////// bind mouse event handlers to the down button //////////////
  this.$downButton.mousedown(function(e) {
    return thisObj.handleMouseDown(e, $(this)); 
  });

  this.$downButton.mouseup(function(e) {
    return thisObj.handleMouseUp(e, $(this)); 
  });

  this.$downButton.mouseenter(function(e) {
    return thisObj.handleMouseEnter(e, $(this)); 
  });

  this.$downButton.mouseout(function(e) {
    return thisObj.handleMouseOut(e, $(this)); 
  });

  this.$downButton.focus(function(e) {
    return thisObj.handleFocus(e, $(this)); 
  });

  this.$downButton.click(function(e) {
    return thisObj.handleClick(e, $(this)); 
  });

  //////// bind event handlers to the spinbutton //////////////
  this.$id.keydown(function(e) {
    return thisObj.handleKeyDown(e); 
  });

  this.$id.keypress(function(e) {
    return thisObj.handleKeyPress(e); 
  });

  this.$id.focus(function(e) {
    return thisObj.handleFocus(e); 
  });

  this.$id.blur(function(e) {
    return thisObj.handleBlur(e); 
  });

  this.$id.parent().focusout(function(e) {
    return thisObj.handleBlur(e); 
  });

} // end bindHandlers()

//
// Function handleClick() is a member function to handle click events for the control
// buttons
//
// @param (e object) e is the event object
//
// @param ($button object) $button is the jQuery object of the button clicked
//
// @return (boolean) Returns false
//

spinbutton.prototype.handleClick = function(e, $button) {

  if ($button.attr('id') == this.upID) {

    // if valuemax isn't met, increment valnow
    if (this.valNow < this.valMax) {
      this.valNow++;

      this.$id.text(this.valNow);
      this.$id.attr('aria-valuenow', this.valNow);
    }
  }
  else {

    // if valuemax isn't met, decrement valnow
    if (this.valNow > this.valMin) {
      this.valNow--;

      this.$id.text(this.valNow);
      this.$id.attr('aria-valuenow', this.valNow);
    }
  }

  // set focus on the spinbutton
  this.$id.focus();
    
  e.stopPropagation();
  return false;

} // end handleClick()

//
// Function handleKeyDown() is a member function to handle keydown events for the control.
//
// @param (e object) e is the event object
//
// @return (boolean) Returns false if consuming; true if propagating
//

spinbutton.prototype.handleKeyDown = function(e) {

  if (e.altKey || e.ctrlKey || e.shiftKey) {
    // do nothing
    return true;
  }

  switch(e.keyCode) {
    case this.keys.pageup: {

      if (this.valNow < this.valMax) {

        // if valnow is small enough, increase by the skipVal,
        // otherwise just set to valmax
        if (this.valNow < this.valMax - this.skipVal) {
          this.valNow += this.skipVal;
        }  
        else {
          this.valNow = this.valMax;
        }

        // update the control
        this.$id.attr('aria-valuenow', this.valNow);
        this.$id.html(this.valNow);
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.pagedown: {

      if (this.valNow > this.valMin) {

        // if valNow is big enough, decrease by the skipVal,
        // otherwise just set to valmin
        if (this.valNow > this.valMin + this.skipVal) {
          this.valNow -= this.skipVal;
        }  
        else {
          this.valNow = this.valMin;
        }

        // update the control
        this.$id.attr('aria-valuenow', this.valNow);
        this.$id.html(this.valNow);
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.home: {

      if (this.valNow < this.valMax) {
        this.valNow = this.valMax;
        this.$id.attr('aria-valuenow', this.valNow);
        this.$id.html(this.valNow);
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.end: {

      if (this.valNow > this.valMin) {
        this.valNow = this.valMin;
        this.$id.attr('aria-valuenow', this.valNow);
        this.$id.html(this.valNow);
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.right:
    case this.keys.up: {

      // if valuemin isn't met, increment valnow
      if (this.valNow < this.valMax) {
        this.valNow++;

        this.$id.text(this.valNow);
        this.$id.attr('aria-valuenow', this.valNow);
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.left:
    case this.keys.down: {

      // if valuemax isn't met, decrement valnow
      if (this.valNow > this.valMin) {
        this.valNow--;

        this.$id.text(this.valNow);
        this.$id.attr('aria-valuenow', this.valNow);
      }

      e.stopPropagation();
      return false;
    }
  }
  return true;

} // end handleKeyDown()

//
// Function handleKeyPress() is a member function to handle keypress events for the control.
// This function is required to prevent browser that manipulate the window on keypress (such as Opera)
// from performing unwanted scrolling.
//
// @param (e object) e is the event object
//
// @return (boolean) Returns false if consuming; true if propagating
//

spinbutton.prototype.handleKeyPress = function(e) {


  if (e.altKey || e.ctrlKey || e.shiftKey) {
    // do nothing
    return true;
  }

  switch(e.keyCode) {
    case this.keys.pageup:
    case this.keys.pagedown:
    case this.keys.home:
    case this.keys.end:
    case this.keys.left:
    case this.keys.up:
    case this.keys.right:
    case this.keys.down: {
      // consume the event
      e.stopPropagation();
      return false;
    }
  }
  return true;

} // end handleKeyPress()

//
// Function handleFocus() is a member function to handle focus events for the control.
//
// @param (e object) e is the event object
//
// @return (boolean) Returns true
//

spinbutton.prototype.handleFocus = function(e) {

  // add the focus styling class to the control
  this.$id.addClass('focus');

  return true;

} // end handleFocus()

//
// Function handleBlur() is a member function to handle blur events for the control.
//
// @param (e object) e is the event object
//
// @return (boolean) Returns true
//
spinbutton.prototype.handleBlur = function(e) {

  // Remove the focus styling class from the control
  this.$id.removeClass('focus');

  return true;

} // end handleBlur()

 
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
			temp = splitData[0].split('=');	I_r = temp[1];
			temp = splitData[1].split('=');	I_s = temp[1];			
			temp = splitData[2].split('=');	I_t = temp[1];
			temp = splitData[3].split('=');	V_r = temp[1];
			temp = splitData[4].split('=');	V_s = temp[1];
			temp = splitData[5].split('=');	V_t = temp[1];
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
			
			if( temp[0] == '0')
			    {
			    document.getElementById('lamp1').style.background='black';
			    }
			else
        		    {
			    document.getElementById('lamp1').style.background='red';
			    }
		        

			if( temp[0] == '0')
			    {
			    document.getElementById('lamp1').style.background='black';
			    }
			else
        		    {
			    document.getElementById('lamp1').style.background='red';
			    }
		        
			if( temp[1] == '0')
			    {
			    document.getElementById('lamp2').style.background='black';
			    }
			else
        		    {
			    document.getElementById('lamp2').style.background='red';
			    }
		        
			if( temp[2] == '0')
			    {
			    document.getElementById('lamp3').style.background='black';
			    }
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