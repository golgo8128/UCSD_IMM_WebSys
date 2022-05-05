
/* Example:

<html>
<head>
<title>Test Wait Dock</title>

<script type="text/javascript" src="WaitDocks1_9.js"></script>
<script type="text/javascript">
function start_WaitDocks(){
	wdock1 = new WaitDocks(function(){
		document.getElementById("procarea1").innerHTML = new Date();
	},
	function(){
		document.getElementById("message1").innerHTML = "Hello.";	
	}, function(){
		document.getElementById("message1").innerHTML = "Failed...";	
	},
	"waitdockloc1",
	5000, // proc_millisec
	250, // itimeintrv
	15000); // cmax_millisec
	wdock1.loop();
};
</script>

</head>
<body onLoad="start_WaitDocks()">
<div id="procarea1">
Process area.
</div>
<div id="waitdockloc1">
Dock spot.
</div>
<div id="message1">
Message will appear here at the end.
</div>

<input type="button" value="Press" onclick="wdock1.invoke_stop_sequence()"/>

</body>
</html>

*/

function WaitDocks(procfunc, stopfunc, toutfunc,
				   dockdiv, proc_millisec, itimeintrv, cmax_millisec){
	
	this.procfunc   = typeof procfunc   !== 'undefined' ? procfunc : function(){ };
	this.stopfunc   = typeof stopfunc   !== 'undefined' ? stopfunc : function(){ };
	this.toutfunc   = typeof toutfunc   !== 'undefined' ? toutfunc : function(){ };
	this.dockdiv    = typeof dockdiv    !== 'undefined' ? dockdiv : "waitdockloc";
	
	// Be careful of THE ORDER of these two parameters when calling the function - reversed.
	this.itimeintrv = typeof itimeintrv !== 'undefined' ? itimeintrv : 250;
	this.proc_count = typeof proc_millisec !== 'undefined' ? Math.ceil(proc_millisec / this.itimeintrv) : Math.ceil(5000 / this.itimeintrv);
	// This must be an integer.
	
	this.countmax   = typeof cmax_millisec !== 'undefined' ? Math.ceil(cmax_millisec / this.itimeintrv) : Math.ceil(180000 / this.itimeintrv);
	
	this.slashzero  = "END";
	this.dockstart  = 7;
	this.chararray1 = new Array(128);

	this.counter         = 0; // Starts at 0.
	this.countdown_start = 15;
	this.countdown       = this.countdown_start;
	
	this.loopcount = 1;
	this.dockedpos = null;

	this.pre_stop = false;
	this.stop     = false;
	
};

WaitDocks.prototype.invoke_stop_sequence = function(){

	this.pre_stop = true;
	
};

WaitDocks.prototype.get_stop = function(){
	
	return this.stop;
	
};

WaitDocks.prototype.loop = function(){

	if (!this.get_stop()){
		this.update();
		var that = this;
		setTimeout(function(){ that.loop(); }, that.itimeintrv);	
	};
	
};

WaitDocks.prototype.procfunc_timing = function(){
	
	return this.counter % this.proc_count == 0;
	
};

WaitDocks.prototype.update = function(){

	if (this.counter >= this.countmax){
		this.invoke_stop_sequence();
	} else if(this.procfunc_timing()){
		this.procfunc();
	}
	
	if (!this.get_stop()){
		this.countdown --;	
		// If called from this.loop, this is always executed.
	}; 

	if(this.countdown < 0){
		this.loopcount ++;
		this.countdown = this.countdown_start + Math.pow(2, this.loopcount);
		// New countdown value
	}

	this.calc_docks();
	this.display();
	
	this.counter ++;
	
};


WaitDocks.prototype.calc_docks = function(){

	for(var i = 0;i < this.loopcount;i ++){
		this.chararray1[i] = "*";
	}
	
	if(this.countdown <= this.dockstart){
		for(i = this.loopcount;i < this.loopcount + this.countdown;i ++){
			this.chararray1[i] = "&nbsp; ";
		}
		this.chararray1[this.loopcount + this.countdown] = "*";
		this.chararray1[this.loopcount + this.countdown + 1] = this.slashzero;
		if(this.countdown == 0 && !this.pre_stop){
			this.dockedpos = this.loopcount;
		} else {
			this.dockedpos = null;
		}
	} else {
		this.dockedpos = null;
		this.chararray1[this.loopcount] = this.slashzero;
		if(this.pre_stop){
			this.stop = true;
			if (this.counter >= this.countmax){
				this.toutfunc();
			} else {
				this.stopfunc(); // Final call.
			}
		}
	}
		
	if(this.countdown % 3 == 2 && !this.pre_stop){
		this.chararray1[this.loopcount-1] =  "&nbsp; ";
	}

};

WaitDocks.prototype.display = function(){

	
	var ostr = "";
	for(var i = 0;this.chararray1[i] != this.slashzero;i ++){
		if(i == this.dockedpos){
			ostr += '<font color="red">' + this.chararray1[i] + '</font>';
		} else {
			ostr += this.chararray1[i];			
		}
	}
	
	document.getElementById(this.dockdiv).innerHTML = ostr;

};



