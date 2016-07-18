var page = require('webpage').create(),
system = require('system'),
address;

if(system.args.length === 1){
	phantom.exit(1);
}else{
	address = system.args[1];
	page.open(address, function (status){
		if(status !== 'success'){
			phantom.exit();
		}else{
			var sc = page.evaluate(function(){
				//var t = Date.now();
				window.scrollTo(0,10000); //滚动到底部
				/*function sleep(d){
				  	while(Date.now - t <= d);
				} 
				sleep(100);*/
				//setTimeout(function (){
				return document.body.innerHTML;
				//},1000);
				
			});
			window.setTimeout(function (){
				console.log(sc);
				phantom.exit();
			},1000);
		}
	});
}