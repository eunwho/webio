$( document ).ready(function() {
/*-----*/
  var rePower      = new TimeSeries();
  var imPower      = new TimeSeries();
  var powerFactor  = new TimeSeries();
  
  setInterval(function() {
	
 	callMacro();		

	rePower.append(new Date().getTime(), Watt);
	imPower.append(new Date().getTime(), Var);
	powerFactor.append( new Date().getTime(), Pf);	
  }, 1000);

  var powerData = new SmoothieChart({ grid: { strokeStyle: 'rgb(125, 0, 0)', fillStyle: 'rgb(60, 0, 0)', lineWidth: 1, millisPerLine: 250, verticalSections: 6 } });
  
  powerData.addTimeSeries(rePower, { strokeStyle: 'rgb(  0, 255,   0)', fillStyle: 'rgba(  0, 255,   0, 0.4)', lineWidth: 3 });
  powerData.addTimeSeries(imPower, { strokeStyle: 'rgb(255,   0,   0)', fillStyle: 'rgba(255,   0,   0, 0.4)', lineWidth: 3 });
  powerData.addTimeSeries(powerFactor, { strokeStyle: 'rgb(  0,   0, 255)', fillStyle: 'rgba(  0,   0, 255, 0.4)', lineWidth: 3 });

  powerData.streamTo(document.getElementById("powerConsole"), 1000);

  // Volt data
  var rVolt = new TimeSeries();
  var sVolt = new TimeSeries();
  var tVolt = new TimeSeries();
  
  setInterval(function() {
	rVolt.append(new Date().getTime(),V_r);
	sVolt.append(new Date().getTime(),V_s);
	tVolt.append(new Date().getTime(),V_t);
	
  }, 1000);

  var voltData = new SmoothieChart({ grid: { strokeStyle: 'rgb(125, 0, 0)', fillStyle: 'rgb(60, 0, 0)', lineWidth: 1, millisPerLine: 250, verticalSections: 6 } });
  
  voltData.addTimeSeries(rVolt, { strokeStyle: 'rgb(  0, 255,   0)', fillStyle: 'rgba(  0, 255,   0, 0.4)', lineWidth: 3 });
  voltData.addTimeSeries(sVolt, { strokeStyle: 'rgb(255,   0,   0)', fillStyle: 'rgba(255,   0,   0, 0.4)', lineWidth: 3 });
  voltData.addTimeSeries(tVolt, { strokeStyle: 'rgb(  0,   0, 255)', fillStyle: 'rgba(  0,   0, 255, 0.4)', lineWidth: 3 });

  voltData.streamTo(document.getElementById("voltConsole"), 1000);


  // Ampere data
  var rAmpere = new TimeSeries();
  var sAmpere = new TimeSeries();
  var tAmpere = new TimeSeries();
  
  setInterval(function() {
	rAmpere.append(new Date().getTime(),I_r);
	sAmpere.append(new Date().getTime(),I_s);
	tAmpere.append(new Date().getTime(),I_t);
	
  }, 1000);

  var ampereData = new SmoothieChart({ grid: { strokeStyle: 'rgb(125, 0, 0)', fillStyle: 'rgb(60, 0, 0)', lineWidth: 1, millisPerLine: 250, verticalSections: 6 } });
  
  ampereData.addTimeSeries(rAmpere, { strokeStyle: 'rgb(  0, 255,   0)', fillStyle: 'rgba(  0, 255,   0, 0.4)', lineWidth: 3 });
  ampereData.addTimeSeries(sAmpere, { strokeStyle: 'rgb(255,   0,   0)', fillStyle: 'rgba(255,   0,   0, 0.4)', lineWidth: 3 });
  ampereData.addTimeSeries(tAmpere, { strokeStyle: 'rgb(  0,   0, 255)', fillStyle: 'rgba(  0,   0, 255, 0.4)', lineWidth: 3 });

  ampereData.streamTo(document.getElementById("ampereConsole"), 1000);

 /*--- power switch on/off---*/

});
